import { FC, useCallback } from "react";
import { observer } from "mobx-react-lite";
import { CustomSelect } from "@jet/ui";
import { useMobxStore } from "lib/mobx/store-provider";

type Props = {
  workspaceSlug: string;
  projectId: string;
  prStateMapping: Record<string, string>;
  onChange: (mapping: Record<string, string>) => void;
};

const PR_STATES = [
  { key: "draft", label: "Draft" },
  { key: "open", label: "Open" },
  { key: "approved", label: "Approved" },
  { key: "changes_requested", label: "Changes Requested" },
  { key: "merged", label: "Merged" },
  { key: "closed", label: "Closed" },
];

export const PrStateMapping: FC<Props> = observer(
  ({ workspaceSlug, projectId, prStateMapping, onChange }) => {
    const { projectState } = useMobxStore();
    const states = projectState.states?.[projectId] || [];

    const handleStateChange = useCallback(
      (prState: string, jetStateId: string) => {
        onChange({ ...prStateMapping, [prState]: jetStateId });
      },
      [prStateMapping, onChange]
    );

    return (
      <div className="space-y-4">
        <div>
          <h4 className="text-sm font-medium text-custom-text-100">
            PR State Mapping
          </h4>
          <p className="text-xs text-custom-text-300 mt-0.5">
            Map PR lifecycle states to Jet issue states. Use [PROJ-123] in PR
            titles to trigger state automation.
          </p>
        </div>

        <div className="space-y-3">
          {PR_STATES.map(({ key, label }) => (
            <div
              key={key}
              className="flex items-center justify-between gap-4"
            >
              <div className="flex items-center gap-2 min-w-[160px]">
                <span className="text-sm text-custom-text-200">
                  PR: {label}
                </span>
              </div>
              <span className="text-xs text-custom-text-300">→</span>
              <div className="flex-1 max-w-[200px]">
                <CustomSelect
                  value={prStateMapping[key] || ""}
                  onChange={(val: string) => handleStateChange(key, val)}
                  label={
                    states.find((s: any) => s.id === prStateMapping[key])
                      ?.name || "Select state"
                  }
                  buttonClassName="w-full"
                >
                  <CustomSelect.Option value="">
                    <span className="text-sm text-custom-text-300">
                      No mapping
                    </span>
                  </CustomSelect.Option>
                  {states.map((state: any) => (
                    <CustomSelect.Option key={state.id} value={state.id}>
                      <div className="flex items-center gap-2">
                        <span
                          className="h-3 w-3 rounded-full flex-shrink-0"
                          style={{ backgroundColor: state.color }}
                        />
                        <span className="text-sm">{state.name}</span>
                      </div>
                    </CustomSelect.Option>
                  ))}
                </CustomSelect>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }
);
