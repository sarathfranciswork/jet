import { FC, useEffect } from "react";
import { observer } from "mobx-react-lite";
import { useMobxStore } from "lib/mobx/store-provider";
import { Loader } from "@jet/ui";
import { IGithubSyncLog } from "types";

type Props = {
  workspaceSlug: string;
  projectId: string;
};

const STATUS_COLORS: Record<string, string> = {
  success: "bg-green-500/20 text-green-500",
  failed: "bg-red-500/20 text-red-500",
  skipped: "bg-yellow-500/20 text-yellow-500",
};

const DIRECTION_LABELS: Record<string, string> = {
  github_to_jet: "GitHub → Jet",
  jet_to_github: "Jet → GitHub",
};

export const SyncLogList: FC<Props> = observer(
  ({ workspaceSlug, projectId }) => {
    const { githubSync } = useMobxStore();

    useEffect(() => {
      githubSync.fetchSyncLogs(workspaceSlug, projectId);
    }, [workspaceSlug, projectId, githubSync]);

    const logs = githubSync.syncLogs;

    if (!logs) {
      return <Loader className="space-y-3" />;
    }

    if (logs.length === 0) {
      return (
        <div className="text-sm text-custom-text-300 text-center py-6">
          No sync activity yet.
        </div>
      );
    }

    return (
      <div className="space-y-4">
        <h4 className="text-sm font-medium text-custom-text-100">
          Recent Sync Activity
        </h4>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-custom-border-200 text-left text-custom-text-300">
                <th className="pb-2 pr-4">Type</th>
                <th className="pb-2 pr-4">Direction</th>
                <th className="pb-2 pr-4">Status</th>
                <th className="pb-2 pr-4">Time</th>
                <th className="pb-2">Details</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log: IGithubSyncLog) => (
                <tr
                  key={log.id}
                  className="border-b border-custom-border-100"
                >
                  <td className="py-2 pr-4 text-custom-text-200 capitalize">
                    {log.entity_type.replace("_", " ")}
                  </td>
                  <td className="py-2 pr-4 text-custom-text-200">
                    {DIRECTION_LABELS[log.direction] || log.direction}
                  </td>
                  <td className="py-2 pr-4">
                    <span
                      className={`px-2 py-0.5 rounded-full text-xs ${
                        STATUS_COLORS[log.status] || ""
                      }`}
                    >
                      {log.status}
                    </span>
                  </td>
                  <td className="py-2 pr-4 text-custom-text-300">
                    {new Date(log.created_at).toLocaleString()}
                  </td>
                  <td className="py-2 text-custom-text-300 max-w-[200px] truncate">
                    {log.error_message || "-"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
);
