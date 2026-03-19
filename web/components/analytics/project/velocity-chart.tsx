import { useRouter } from "next/router";
import useSWR from "swr";
// components
import { BarGraph, LineGraph, ProfileEmptyState } from "components/ui";
// services
import { AnalyticsService } from "services/analytics.service";
// image
import emptyGraph from "public/empty-state/empty_graph.svg";
// constants
import { PROJECT_VELOCITY } from "constants/fetch-keys";

const analyticsService = new AnalyticsService();

export const VelocityChart: React.FC = () => {
  const router = useRouter();
  const { workspaceSlug, projectId } = router.query as {
    workspaceSlug: string;
    projectId: string;
  };

  const { data: velocityData } = useSWR(
    workspaceSlug && projectId ? PROJECT_VELOCITY(workspaceSlug, projectId, 6) : null,
    workspaceSlug && projectId
      ? () => analyticsService.getProjectVelocity(workspaceSlug, projectId, { last_n_cycles: 6 })
      : null
  );

  if (!velocityData || velocityData.velocity.length === 0) {
    return (
      <div className="px-7 py-4">
        <ProfileEmptyState
          title="No velocity data"
          description="Complete cycles with issues to view velocity trends."
          image={emptyGraph}
        />
      </div>
    );
  }

  const barData = velocityData.velocity.map((v) => ({
    cycle: v.cycle_name.length > 12 ? v.cycle_name.slice(0, 12) + "…" : v.cycle_name,
    "Completed Points": v.completed_points,
    "Committed Points": v.committed_points,
  }));

  const rollingAvgLineData = [
    {
      id: "Rolling Avg (Points)",
      color: "#f97316",
      data: velocityData.rolling_average.map((r) => ({
        x: r.cycle_name.length > 12 ? r.cycle_name.slice(0, 12) + "…" : r.cycle_name,
        y: r.avg_points,
      })),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="border border-custom-border-200 rounded-[10px] p-3">
        <h3 className="px-3 text-base font-medium mb-2">Velocity — Story Points per Cycle</h3>
        <div className="flex items-center gap-4 px-3 mb-2 text-xs text-custom-text-200">
          <span className="flex items-center gap-1">
            <span className="h-3 w-3 bg-custom-primary-100 inline-block rounded-sm" /> Completed
          </span>
          <span className="flex items-center gap-1">
            <span className="h-3 w-3 bg-custom-primary-100/30 inline-block rounded-sm" /> Committed
          </span>
        </div>
        <BarGraph
          data={barData}
          indexBy="cycle"
          keys={["Completed Points", "Committed Points"]}
          height="350px"
          colors={["rgb(var(--color-primary-100))", "rgba(var(--color-primary-100), 0.3)"]}
          groupMode="grouped"
          margin={{ top: 20, bottom: 50, left: 50, right: 20 }}
          axisBottom={{
            tickSize: 0,
            tickPadding: 10,
            tickRotation: barData.length > 4 ? -30 : 0,
          }}
          tooltip={({ id, value, indexValue }) => (
            <div className="rounded-md border border-custom-border-200 bg-custom-background-80 p-2 text-xs">
              <div className="font-medium">{indexValue}</div>
              <div>
                {id}: {value}
              </div>
            </div>
          )}
        />
      </div>

      <div className="border border-custom-border-200 rounded-[10px] p-3">
        <h3 className="px-3 text-base font-medium mb-2">Rolling Average (Last 4 Cycles)</h3>
        <LineGraph
          data={rollingAvgLineData}
          height="250px"
          colors={(datum) => datum.color}
          curve="monotoneX"
          margin={{ top: 20, bottom: 40, left: 50, right: 20 }}
          enableSlices="x"
          sliceTooltip={(datum) => (
            <div className="rounded-md border border-custom-border-200 bg-custom-background-80 p-2 text-xs">
              <div className="font-medium">{datum.slice.points[0].data.xFormatted}</div>
              <div>Avg points: {datum.slice.points[0].data.yFormatted}</div>
            </div>
          )}
          theme={{
            background: "rgb(var(--color-background-100))",
          }}
          enableArea
        />
      </div>

      <div className="border border-custom-border-200 rounded-[10px] p-3">
        <h3 className="px-3 text-base font-medium mb-4">Cycle Summary</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-custom-border-200 text-left text-custom-text-200">
                <th className="px-3 py-2 font-medium">Cycle</th>
                <th className="px-3 py-2 font-medium">Total</th>
                <th className="px-3 py-2 font-medium">Completed</th>
                <th className="px-3 py-2 font-medium">Points Committed</th>
                <th className="px-3 py-2 font-medium">Points Completed</th>
              </tr>
            </thead>
            <tbody>
              {velocityData.velocity.map((v) => (
                <tr key={v.cycle_id} className="border-b border-custom-border-100">
                  <td className="px-3 py-2">{v.cycle_name}</td>
                  <td className="px-3 py-2">{v.total_issues}</td>
                  <td className="px-3 py-2">{v.completed_issues}</td>
                  <td className="px-3 py-2">{v.committed_points}</td>
                  <td className="px-3 py-2">{v.completed_points}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
