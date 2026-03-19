import { FC, useState } from "react";
import { Controller, useForm } from "react-hook-form";
import { observer } from "mobx-react-lite";
import { Button, ToggleSwitch } from "@jet/ui";
import { useMobxStore } from "lib/mobx/store-provider";
import { IGithubSyncConfig } from "types";

type Props = {
  workspaceSlug: string;
  projectId: string;
  repoSyncId: string;
  existingConfig?: IGithubSyncConfig;
  onSave?: (config: IGithubSyncConfig) => void;
};

type FormValues = {
  sync_direction: "bidirectional" | "github_to_jet";
  github_trigger_label: string;
  sync_comments: boolean;
  sync_labels: boolean;
  sync_assignees: boolean;
};

export const SyncConfigForm: FC<Props> = observer(
  ({ workspaceSlug, projectId, repoSyncId, existingConfig, onSave }) => {
    const { githubSync } = useMobxStore();
    const [isSubmitting, setIsSubmitting] = useState(false);

    const { handleSubmit, control } = useForm<FormValues>({
      defaultValues: {
        sync_direction: existingConfig?.sync_direction || "bidirectional",
        github_trigger_label: existingConfig?.github_trigger_label || "Jet",
        sync_comments: existingConfig?.sync_comments ?? true,
        sync_labels: existingConfig?.sync_labels ?? true,
        sync_assignees: existingConfig?.sync_assignees ?? true,
      },
    });

    const onSubmit = async (data: FormValues) => {
      setIsSubmitting(true);
      try {
        let config: IGithubSyncConfig;
        if (existingConfig) {
          config = await githubSync.updateSyncConfig(
            workspaceSlug,
            projectId,
            repoSyncId,
            existingConfig.id,
            data
          );
        } else {
          config = await githubSync.createSyncConfig(
            workspaceSlug,
            projectId,
            repoSyncId,
            data
          );
        }
        onSave?.(config);
      } finally {
        setIsSubmitting(false);
      }
    };

    return (
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div>
          <h3 className="text-lg font-medium text-custom-text-100">
            GitHub Sync Configuration
          </h3>
          <p className="text-sm text-custom-text-200 mt-1">
            Configure bidirectional sync between GitHub and Jet.
          </p>
        </div>

        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium text-custom-text-100">
              Sync Direction
            </label>
            <Controller
              control={control}
              name="sync_direction"
              render={({ field: { value, onChange } }) => (
                <div className="mt-2 flex gap-4">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      value="bidirectional"
                      checked={value === "bidirectional"}
                      onChange={() => onChange("bidirectional")}
                      className="text-custom-primary-100"
                    />
                    <span className="text-sm text-custom-text-200">
                      Bidirectional
                    </span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      value="github_to_jet"
                      checked={value === "github_to_jet"}
                      onChange={() => onChange("github_to_jet")}
                      className="text-custom-primary-100"
                    />
                    <span className="text-sm text-custom-text-200">
                      GitHub to Jet only
                    </span>
                  </label>
                </div>
              )}
            />
          </div>

          <div>
            <label className="text-sm font-medium text-custom-text-100">
              GitHub Trigger Label
            </label>
            <p className="text-xs text-custom-text-300 mt-0.5">
              Issues with this label on GitHub will be synced to Jet.
            </p>
            <Controller
              control={control}
              name="github_trigger_label"
              render={({ field: { value, onChange } }) => (
                <input
                  type="text"
                  value={value}
                  onChange={onChange}
                  className="mt-2 w-full rounded-md border border-custom-border-200 bg-custom-background-100 px-3 py-2 text-sm text-custom-text-100 focus:outline-none focus:border-custom-primary-100"
                  placeholder="Jet"
                />
              )}
            />
          </div>

          <div className="space-y-3">
            <label className="text-sm font-medium text-custom-text-100">
              Sync Options
            </label>

            <Controller
              control={control}
              name="sync_comments"
              render={({ field: { value, onChange } }) => (
                <div className="flex items-center justify-between">
                  <span className="text-sm text-custom-text-200">
                    Sync comments
                  </span>
                  <ToggleSwitch value={value} onChange={onChange} />
                </div>
              )}
            />

            <Controller
              control={control}
              name="sync_labels"
              render={({ field: { value, onChange } }) => (
                <div className="flex items-center justify-between">
                  <span className="text-sm text-custom-text-200">
                    Sync labels
                  </span>
                  <ToggleSwitch value={value} onChange={onChange} />
                </div>
              )}
            />

            <Controller
              control={control}
              name="sync_assignees"
              render={({ field: { value, onChange } }) => (
                <div className="flex items-center justify-between">
                  <span className="text-sm text-custom-text-200">
                    Sync assignees
                  </span>
                  <ToggleSwitch value={value} onChange={onChange} />
                </div>
              )}
            />
          </div>
        </div>

        <div className="flex justify-end gap-2">
          <Button type="submit" loading={isSubmitting}>
            {existingConfig ? "Update" : "Enable"} Sync
          </Button>
        </div>
      </form>
    );
  }
);
