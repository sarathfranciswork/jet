import { FC, useEffect } from "react";
import { observer } from "mobx-react-lite";
import { useMobxStore } from "lib/mobx/store-provider";
import { IGithubPullRequest } from "types";
import { PrBadge } from "./pr-badge";

type Props = {
  workspaceSlug: string;
  projectId: string;
  issueId?: string;
};

export const PrList: FC<Props> = observer(
  ({ workspaceSlug, projectId, issueId }) => {
    const { githubSync } = useMobxStore();

    useEffect(() => {
      githubSync.fetchPullRequests(workspaceSlug, projectId, issueId);
    }, [workspaceSlug, projectId, issueId, githubSync]);

    const key = issueId || projectId;
    const pullRequests = githubSync.pullRequests[key] || [];

    if (pullRequests.length === 0) {
      return null;
    }

    return (
      <div className="space-y-3">
        <h4 className="text-sm font-medium text-custom-text-100">
          Linked Pull Requests
        </h4>
        <div className="space-y-2">
          {pullRequests.map((pr: IGithubPullRequest) => (
            <div
              key={pr.id}
              className="flex items-center justify-between rounded-md border border-custom-border-200 px-3 py-2"
            >
              <div className="flex items-center gap-3 min-w-0">
                {pr.author_avatar_url && (
                  <img
                    src={pr.author_avatar_url}
                    alt={pr.author_login}
                    className="h-5 w-5 rounded-full flex-shrink-0"
                  />
                )}
                <div className="min-w-0">
                  <a
                    href={pr.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-custom-text-100 hover:text-custom-primary-100 truncate block"
                  >
                    {pr.title}
                  </a>
                  <span className="text-xs text-custom-text-300">
                    by @{pr.author_login}
                  </span>
                </div>
              </div>
              <div className="flex-shrink-0 ml-3">
                <PrBadge pullRequest={pr} />
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }
);
