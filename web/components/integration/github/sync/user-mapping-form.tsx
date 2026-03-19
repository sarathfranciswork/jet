import { FC, useEffect, useState } from "react";
import { observer } from "mobx-react-lite";
import { Trash2 } from "lucide-react";
import { Button, Input } from "@jet/ui";
import { useMobxStore } from "lib/mobx/store-provider";
import { IGithubUserMapping } from "types";

type Props = {
  workspaceSlug: string;
};

export const UserMappingForm: FC<Props> = observer(({ workspaceSlug }) => {
  const { githubSync } = useMobxStore();
  const [githubUsername, setGithubUsername] = useState("");
  const [githubUserId, setGithubUserId] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    githubSync.fetchUserMappings(workspaceSlug);
  }, [workspaceSlug, githubSync]);

  const handleAdd = async () => {
    if (!githubUsername || !githubUserId) return;
    setIsSubmitting(true);
    try {
      await githubSync.createUserMapping(workspaceSlug, {
        github_username: githubUsername,
        github_user_id: parseInt(githubUserId, 10),
      });
      setGithubUsername("");
      setGithubUserId("");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (mappingId: string) => {
    await githubSync.deleteUserMapping(workspaceSlug, mappingId);
  };

  return (
    <div className="space-y-4">
      <div>
        <h4 className="text-sm font-medium text-custom-text-100">
          User Mappings
        </h4>
        <p className="text-xs text-custom-text-300 mt-0.5">
          Connect GitHub accounts to Jet users for assignee sync and comment
          attribution.
        </p>
      </div>

      {githubSync.userMappings.length > 0 && (
        <div className="space-y-2">
          {githubSync.userMappings.map((mapping: IGithubUserMapping) => (
            <div
              key={mapping.id}
              className="flex items-center justify-between rounded-md border border-custom-border-200 px-3 py-2"
            >
              <div className="flex items-center gap-3">
                <span className="text-sm text-custom-text-200">
                  @{mapping.github_username}
                </span>
                <span className="text-xs text-custom-text-300">
                  (ID: {mapping.github_user_id})
                </span>
              </div>
              <button
                onClick={() => handleDelete(mapping.id)}
                className="text-custom-text-300 hover:text-red-500 transition-colors"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
      )}

      <div className="flex items-end gap-3">
        <div className="flex-1">
          <label className="text-xs text-custom-text-300">
            GitHub Username
          </label>
          <Input
            value={githubUsername}
            onChange={(e) => setGithubUsername(e.target.value)}
            placeholder="octocat"
            className="mt-1"
          />
        </div>
        <div className="w-32">
          <label className="text-xs text-custom-text-300">GitHub User ID</label>
          <Input
            value={githubUserId}
            onChange={(e) => setGithubUserId(e.target.value)}
            placeholder="12345"
            className="mt-1"
          />
        </div>
        <Button onClick={handleAdd} loading={isSubmitting} variant="primary">
          Add
        </Button>
      </div>
    </div>
  );
});
