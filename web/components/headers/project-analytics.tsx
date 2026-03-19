import { useRouter } from "next/router";
import { observer } from "mobx-react-lite";
import { BarChart2 } from "lucide-react";
// mobx store
import { useMobxStore } from "lib/mobx/store-provider";
// ui
import { Breadcrumbs } from "@plane/ui";
// helper
import { renderEmoji } from "helpers/emoji.helper";

export const ProjectAnalyticsHeader: React.FC = observer(() => {
  const router = useRouter();
  const { workspaceSlug } = router.query;

  const { project: projectStore } = useMobxStore();
  const { currentProjectDetails } = projectStore;

  return (
    <div className="relative flex w-full flex-shrink-0 flex-row z-10 items-center justify-between gap-x-2 gap-y-4 border-b border-custom-border-200 bg-custom-sidebar-background-100 p-4">
      <div className="flex items-center gap-2 flex-grow w-full whitespace-nowrap overflow-ellipsis">
        <div>
          <Breadcrumbs>
            <Breadcrumbs.BreadcrumbItem
              type="text"
              label={currentProjectDetails?.name ?? "Project"}
              icon={
                currentProjectDetails?.emoji ? (
                  renderEmoji(currentProjectDetails.emoji)
                ) : currentProjectDetails?.icon_prop ? (
                  renderEmoji(currentProjectDetails.icon_prop)
                ) : (
                  <BarChart2 className="h-4 w-4" />
                )
              }
              link={`/${workspaceSlug}/projects/${currentProjectDetails?.id}/issues`}
            />
            <Breadcrumbs.BreadcrumbItem type="text" label="Analytics" icon={<BarChart2 className="h-4 w-4" />} />
          </Breadcrumbs>
        </div>
      </div>
    </div>
  );
});
