import { useRouter } from "next/router";
import useSWR from "swr";
import { useState, useMemo } from "react";
// components
import { ProfileEmptyState } from "components/ui";
import { LineGraph } from "components/ui";
// services
import { AnalyticsService } from "services/analytics.service";
// image
import emptyGraph from "public/empty-state/empty_graph.svg";
// constants
import { PROJECT_FLOW } from "constants/fetch-keys";

const analyticsService = new AnalyticsService();

const STATE_GROUP_COLORS: Record<string, string> = {
  backlog: "#bec2c8",
  unstarted: "#80838d",
  started: "#f59e0b",
  completed: "#16a34a",
  cancelled: "#ef4444",
};

export const FlowDiagram: React.FC = () => {
  const router = useRouter();
  const { workspaceSlug, projectId } = router.query as {
    workspaceSlug: string;
    projectId: string;
  };

  // Default to last 30 days
  const defaultEnd = new Date().toISOString().slice(0, 10);
  const defaultStart = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);

  const [startDate, setStartDate] = useState(defaultStart);
  const [endDate, setEndDate] = useState(defaultEnd);

  const { data: flowData } = useSWR(
    workspaceSlug && projectId && startDate && endDate
      ? PROJECT_FLOW(workspaceSlug, projectId, startDate, endDate)
      : null,
    workspaceSlug && projectId && startDate && endDate
      ? () =>
          analyticsService.getProjectFlow(workspaceSlug, projectId, {
            start_date: startDate,
            end_date: endDate,
          })
      : null
  );

  const lineData = useMemo(() => {
    if (!flowData || flowData.flow.length === 0) return [];

    return flowData.state_groups.map((group) => ({
      id: group.charAt(0).toUpperCase() + group.slice(1),
      color: STATE_GROUP_COLORS[group] || "#6b7280",
      data: flowData.flow.map((d) => ({
        x: d.date.slice(5), // MM-DD format
        y: (d as Record<string, number>)[group] || 0,
      })),
    }));
  }, [flowData]);

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4 px-4">
        <div className="flex items-center gap-2">
          <label className="text-sm text-custom-text-200">From:</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="rounded-md border border-custom-border-200 bg-custom-background-100 px-3 py-1.5 text-sm"
          />
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm text-custom-text-200">To:</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="rounded-md border border-custom-border-200 bg-custom-background-100 px-3 py-1.5 text-sm"
          />
        </div>
      </div>

      {lineData.length > 0 ? (
        <div className="border border-custom-border-200 rounded-[10px] p-3">
          <h3 className="px-3 text-base font-medium mb-2">Cumulative Flow</h3>
          <div className="flex items-center gap-4 px-3 mb-2 text-xs text-custom-text-200 flex-wrap">
            {flowData?.state_groups.map((group) => (
              <span key={group} className="flex items-center gap-1">
                <span
                  className="h-3 w-3 rounded-sm inline-block"
                  style={{ backgroundColor: STATE_GROUP_COLORS[group] }}
                />
                {group.charAt(0).toUpperCase() + group.slice(1)}
              </span>
            ))}
          </div>
          <LineGraph
            data={lineData}
            height="400px"
            colors={(datum) => datum.color}
            curve="monotoneX"
            margin={{ top: 20, bottom: 40, left: 50, right: 20 }}
            enableSlices="x"
            sliceTooltip={(datum) => (
              <div className="rounded-md border border-custom-border-200 bg-custom-background-80 p-2 text-xs">
                <div className="font-medium mb-1">{datum.slice.points[0].data.xFormatted}</div>
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
              tickRotation: lineData[0]?.data.length > 14 ? -45 : 0,
            }}
            enableArea
            areaOpacity={0.15}
          />
        </div>
      ) : (
        <div className="px-7 py-4">
          <ProfileEmptyState
            title="No flow data"
            description="Ensure your project has issues within the selected date range."
            image={emptyGraph}
          />
        </div>
      )}
    </div>
  );
};
