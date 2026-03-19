import { FC, useCallback } from "react";
import { useRouter } from "next/router";
import useSWR from "swr";
import { CustomSelect, StateGroupIcon } from "@jet/ui";
import { ProjectStateService } from "services/project";
import { STATES_LIST } from "constants/fetch-keys";
import { getStatesList } from "helpers/state.helper";

type Props = {
  stateMapping: Record<string, string>;
  onChange: (mapping: Record<string, string>) => void;
};

const GITHUB_STATES = [
  { key: "open", label: "Open" },
  { key: "closed", label: "Closed" },
];

const projectStateService = new ProjectStateService();

export const StateMapping: FC<Props> = ({ stateMapping, onChange }) => {
  const router = useRouter();
  const { workspaceSlug, projectId } = router.query;

  const { data: stateGroups } = useSWR(
    workspaceSlug && projectId ? STATES_LIST(projectId as string) : null,
    workspaceSlug && projectId
      ? () =>
          projectStateService.getStates(
            workspaceSlug as string,
            projectId as string
          )
      : null
  );
  const states = getStatesList(stateGroups);

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
        {GITHUB_STATES.map(({ key, label }) => {
          const selectedState = states?.find(
            (s) => s.id === stateMapping[key]
          );

          return (
            <div
              key={key}
              className="flex items-center justify-between gap-4"
            >
              <div className="flex items-center gap-2 min-w-[120px]">
                <span className="text-sm text-custom-text-200">
                  GitHub: {label}
                </span>
              </div>
              <span className="text-xs text-custom-text-300">&rarr;</span>
              <div className="flex-1 max-w-[200px]">
                <CustomSelect
                  value={stateMapping[key] || ""}
                  onChange={(val: string) => handleStateChange(key, val)}
                  label={
                    selectedState ? (
                      <div className="flex items-center gap-2">
                        <StateGroupIcon
                          stateGroup={selectedState.group}
                          color={selectedState.color}
                          height="14px"
                          width="14px"
                        />
                        <span>{selectedState.name}</span>
                      </div>
                    ) : (
                      "Select state"
                    )
                  }
                  buttonClassName="w-full"
                >
                  {states?.map((state) => (
                    <CustomSelect.Option key={state.id} value={state.id}>
                      <div className="flex items-center gap-2">
                        <StateGroupIcon
                          stateGroup={state.group}
                          color={state.color}
                          height="14px"
                          width="14px"
                        />
                        <span className="text-sm">{state.name}</span>
                      </div>
                    </CustomSelect.Option>
                  ))}
                </CustomSelect>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
