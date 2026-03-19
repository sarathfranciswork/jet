import { FC, useCallback } from "react";
import { observer } from "mobx-react-lite";
import { CustomSelect } from "@jet/ui";
import { useMobxStore } from "lib/mobx/store-provider";

type Props = {
  workspaceSlug: string;
  projectId: string;
  stateMapping: Record<string, string>;
  onChange: (mapping: Record<string, string>) => void;
};

const GITHUB_STATES = [
  { key: "open", label: "Open" },
  { key: "closed", label: "Closed" },
];

export const StateMapping: FC<Props> = observer(
  ({ workspaceSlug, projectId, stateMapping, onChange }) => {
    const { projectState } = useMobxStore();
    const states = projectState.states?.[projectId] || [];

    const handleStateChange = useCallback(
      (githubState: string, jetStateId: string) => {
        onChange({ ...stateMapping, [githubState]: jetStateId });
      },
      [stateMapping, onChange]
    );

    return (
      <div className="space-y-4">
        <div>
          <h4 className="text-sm font-medium text-custom-text-100">
            Issue State Mapping
          </h4>
          <p className="text-xs text-custom-text-300 mt-0.5">
            Map GitHub issue states to Jet states.
          </p>
        </div>

        <div className="space-y-3">
          {GITHUB_STATES.map(({ key, label }) => (
            <div
              key={key}
              className="flex items-center justify-between gap-4"
            >
              <div className="flex items-center gap-2 min-w-[120px]">
                <span className="text-sm text-custom-text-200">
                  GitHub: {label}
                </span>
              </div>
              <span className="text-xs text-custom-text-300">→</span>
              <div className="flex-1 max-w-[200px]">
                <CustomSelect
                  value={stateMapping[key] || ""}
                  onChange={(val: string) => handleStateChange(key, val)}
                  label={
                    states.find((s: any) => s.id === stateMapping[key])?.name ||
                    "Select state"
                  }
                  buttonClassName="w-full"
                >
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
