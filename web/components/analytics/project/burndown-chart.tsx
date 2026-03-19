import { useRouter } from "next/router";
import useSWR from "swr";
import { useState } from "react";
// components
import { LineGraph, ProfileEmptyState } from "components/ui";
// services
import { AnalyticsService } from "services/analytics.service";
// image
import emptyGraph from "public/empty-state/empty_graph.svg";
// types
import { IBurndownResponse } from "types";
// constants
import { PROJECT_BURNDOWN } from "constants/fetch-keys";

const analyticsService = new AnalyticsService();

type Props = {
  cycles: { id: string; name: string }[];
};

export const BurndownChart: React.FC<Props> = ({ cycles }) => {
  const router = useRouter();
  const { workspaceSlug, projectId } = router.query as {
    workspaceSlug: string;
    projectId: string;
  };

  const [selectedCycle, setSelectedCycle] = useState<string>(cycles?.[0]?.id ?? "");
  const [metric, setMetric] = useState<"count" | "points">("count");

  const { data: burndownData } = useSWR(
    workspaceSlug && projectId && selectedCycle
      ? PROJECT_BURNDOWN(workspaceSlug, projectId, selectedCycle, metric)
      : null,
    workspaceSlug && projectId && selectedCycle
      ? () =>
          analyticsService.getProjectBurndown(workspaceSlug, projectId, {
            cycle_id: selectedCycle,
            metric,
          })
      : null
  );

  if (!cycles || cycles.length === 0) {
    return (
      <div className="px-7 py-4">
        <ProfileEmptyState
          title="No cycles found"
          description="Create cycles to view burndown charts."
          image={emptyGraph}
        />
      </div>
    );
  }

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
            {cycles.map((cycle) => (
              <option key={cycle.id} value={cycle.id}>
                {cycle.name}
              </option>
            ))}
          </select>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm text-custom-text-200">Metric:</label>
          <select
            value={metric}
            onChange={(e) => setMetric(e.target.value as "count" | "points")}
            className="rounded-md border border-custom-border-200 bg-custom-background-100 px-3 py-1.5 text-sm"
          >
            <option value="count">Issue Count</option>
            <option value="points">Story Points</option>
          </select>
        </div>
      </div>

      {burndownData && burndownData.ideal.length > 0 ? (
        <div className="border border-custom-border-200 rounded-[10px] p-3">
          <h3 className="px-3 text-base font-medium mb-2">
            Burndown — {burndownData.cycle.name}
          </h3>
          <div className="flex items-center gap-4 px-3 mb-2 text-xs text-custom-text-200">
            <span className="flex items-center gap-1">
              <span className="h-0.5 w-4 bg-custom-primary-100 inline-block" /> Ideal
            </span>
            <span className="flex items-center gap-1">
              <span className="h-0.5 w-4 bg-orange-500 inline-block" /> Actual
            </span>
            {burndownData.scope_changes.length > 0 && (
              <span className="flex items-center gap-1">
                <span className="h-2 w-2 bg-red-500 inline-block rounded-full" /> Scope change
              </span>
            )}
          </div>
          <LineGraph
            data={[
              {
                id: "ideal",
                color: "rgb(var(--color-primary-100))",
                data: burndownData.ideal.map((d) => ({
                  x: d.date.slice(5),
                  y: d.value,
                })),
              },
              {
                id: "actual",
                color: "#f97316",
                data: burndownData.actual.map((d) => ({
                  x: d.date.slice(5),
                  y: d.value,
                })),
              },
            ]}
            customYAxisTickValues={[
              ...burndownData.ideal.map((d) => d.value),
              ...burndownData.actual.map((d) => d.value),
            ]}
            height="400px"
            colors={(datum) => datum.color}
            curve="monotoneX"
            margin={{ top: 20, bottom: 40, left: 50, right: 20 }}
            enableSlices="x"
            sliceTooltip={(datum) => (
              <div className="rounded-md border border-custom-border-200 bg-custom-background-80 p-2 text-xs">
                <div className="font-medium">{datum.slice.points[0].data.xFormatted}</div>
                {datum.slice.points.map((point) => (
                  <div key={point.id} className="flex items-center gap-1">
                    <span
                      className="h-2 w-2 rounded-full"
                      style={{ backgroundColor: point.serieColor }}
                    />
                    {point.serieId}: {point.data.yFormatted}
                  </div>
                ))}
              </div>
            )}
            theme={{
              background: "rgb(var(--color-background-100))",
            }}
            axisBottom={{
              tickSize: 0,
              tickPadding: 10,
              tickRotation: burndownData.ideal.length > 14 ? -45 : 0,
            }}
            enableArea
          />
          <div className="px-3 text-xs text-custom-text-300">
            Total scope: {burndownData.total_scope} {metric === "points" ? "points" : "issues"}
            {burndownData.scope_changes.length > 0 &&
              ` · ${burndownData.scope_changes.length} scope change(s)`}
          </div>
        </div>
      ) : (
        <div className="px-7 py-4">
          <ProfileEmptyState
            title="No burndown data"
            description="Ensure the selected cycle has start and end dates with associated issues."
            image={emptyGraph}
          />
        </div>
      )}
    </div>
  );
};
