import { FC, useCallback } from "react";
import { useRouter } from "next/router";
import useSWR from "swr";
import { CustomSelect, StateGroupIcon } from "@jet/ui";
import { ProjectStateService } from "services/project";
import { STATES_LIST } from "constants/fetch-keys";
import { getStatesList } from "helpers/state.helper";

type Props = {
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

const projectStateService = new ProjectStateService();

export const PrStateMapping: FC<Props> = ({ prStateMapping, onChange }) => {
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
        {PR_STATES.map(({ key, label }) => {
          const selectedState = states?.find(
            (s) => s.id === prStateMapping[key]
          );

          return (
            <div
              key={key}
              className="flex items-center justify-between gap-4"
            >
              <div className="flex items-center gap-2 min-w-[160px]">
                <span className="text-sm text-custom-text-200">
                  PR: {label}
                </span>
              </div>
              <span className="text-xs text-custom-text-300">&rarr;</span>
              <div className="flex-1 max-w-[200px]">
                <CustomSelect
                  value={prStateMapping[key] || ""}
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
                      "No mapping"
                    )
                  }
                  buttonClassName="w-full"
                >
                  <CustomSelect.Option value="">
                    <span className="text-sm text-custom-text-300">
                      No mapping
                    </span>
                  </CustomSelect.Option>
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
