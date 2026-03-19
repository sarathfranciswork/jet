import { useRouter } from "next/router";
import useSWR from "swr";
import { useState } from "react";
// components
import { ProfileEmptyState } from "components/ui";
// services
import { AnalyticsService } from "services/analytics.service";
// image
import emptyGraph from "public/empty-state/empty_graph.svg";
// constants
import { PROJECT_WORKLOAD } from "constants/fetch-keys";

const analyticsService = new AnalyticsService();

type Props = {
  cycles: { id: string; name: string }[];
};

export const WorkloadHeatmap: React.FC<Props> = ({ cycles }) => {
  const router = useRouter();
  const { workspaceSlug, projectId } = router.query as {
    workspaceSlug: string;
    projectId: string;
  };

  const [selectedCycle, setSelectedCycle] = useState<string>("");

  const { data: workloadData } = useSWR(
    workspaceSlug && projectId
      ? PROJECT_WORKLOAD(workspaceSlug, projectId, selectedCycle || undefined)
      : null,
    workspaceSlug && projectId
      ? () =>
          analyticsService.getProjectWorkload(workspaceSlug, projectId, {
            cycle_id: selectedCycle || undefined,
          })
      : null
  );

  const getHeatColor = (count: number, maxCount: number) => {
    if (count === 0 || maxCount === 0) return "bg-custom-background-90";
    const intensity = count / maxCount;
    if (intensity > 0.75) return "bg-green-600";
    if (intensity > 0.5) return "bg-green-500";
    if (intensity > 0.25) return "bg-green-400";
    return "bg-green-300";
  };

  const maxCount = workloadData
    ? Math.max(
        ...workloadData.workload.flatMap((w) =>
          Object.values(w.days).map((v) => (typeof v === "number" ? v : 0))
        ),
        1
      )
    : 1;

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4 px-4">
        <div className="flex items-center gap-2">
          <label className="text-sm text-custom-text-200">Cycle:</label>
          <select
            value={selectedCycle}
            onChange={(e) => setSelectedCycle(e.target.value)}
            className="rounded-md border border-custom-border-200 bg-custom-background-100 px-3 py-1.5 text-sm"
          >
            <option value="">All time</option>
            {cycles.map((cycle) => (
              <option key={cycle.id} value={cycle.id}>
                {cycle.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {workloadData && workloadData.workload.length > 0 ? (
        <div className="border border-custom-border-200 rounded-[10px] p-3">
          <h3 className="px-3 text-base font-medium mb-4">Workload Distribution</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-custom-border-200">
                  <th className="px-3 py-2 text-left font-medium text-custom-text-200">Member</th>
                  {workloadData.days.map((day) => (
                    <th key={day} className="px-3 py-2 text-center font-medium text-custom-text-200">
                      {day}
                    </th>
                  ))}
                  <th className="px-3 py-2 text-center font-medium text-custom-text-200">Total</th>
                </tr>
              </thead>
              <tbody>
                {workloadData.workload.map((assignee) => (
                  <tr key={assignee.assignee_id} className="border-b border-custom-border-100">
                    <td className="px-3 py-2 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        {assignee.avatar ? (
                          <img
                            src={assignee.avatar}
                            alt={assignee.display_name}
                            className="h-5 w-5 rounded-full"
                          />
                        ) : (
                          <span className="flex h-5 w-5 items-center justify-center rounded-full bg-custom-primary-100 text-[10px] text-white capitalize">
                            {assignee.display_name?.[0]}
                          </span>
                        )}
                        <span>{assignee.display_name}</span>
                      </div>
                    </td>
                    {workloadData.days.map((day) => {
                      const count = assignee.days[day] || 0;
                      return (
                        <td key={day} className="px-3 py-2 text-center">
                          <div
                            className={`mx-auto flex h-8 w-8 items-center justify-center rounded text-xs font-medium ${getHeatColor(
                              count,
                              maxCount
                            )} ${count > 0 ? "text-white" : "text-custom-text-300"}`}
                            title={`${count} issues completed`}
                          >
                            {count}
                          </div>
                        </td>
                      );
                    })}
                    <td className="px-3 py-2 text-center font-medium">{assignee.total}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="flex items-center gap-2 px-3 mt-4 text-xs text-custom-text-300">
            <span>Less</span>
            <span className="h-4 w-4 rounded bg-custom-background-90" />
            <span className="h-4 w-4 rounded bg-green-300" />
            <span className="h-4 w-4 rounded bg-green-400" />
            <span className="h-4 w-4 rounded bg-green-500" />
            <span className="h-4 w-4 rounded bg-green-600" />
            <span>More</span>
          </div>
        </div>
      ) : (
        <div className="px-7 py-4">
          <ProfileEmptyState
            title="No workload data"
            description="Complete issues with assignees to view workload distribution."
            image={emptyGraph}
          />
        </div>
      )}
    </div>
  );
};
