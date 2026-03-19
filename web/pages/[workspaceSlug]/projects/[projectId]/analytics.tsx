import { Fragment, ReactElement } from "react";
import { useRouter } from "next/router";
import { observer } from "mobx-react-lite";
import { Tab } from "@headlessui/react";
import useSWR from "swr";
// mobx store
import { useMobxStore } from "lib/mobx/store-provider";
// layouts
import { AppLayout } from "layouts/app-layout";
// components
import { ProjectAnalyticsHeader } from "components/headers";
import { BurndownChart, VelocityChart, FlowDiagram, WorkloadHeatmap } from "components/analytics/project";
// types
import { NextPageWithLayout } from "types/app";

const PROJECT_ANALYTICS_TABS = [
  { key: "burndown", title: "Burndown" },
  { key: "velocity", title: "Velocity" },
  { key: "flow", title: "Flow" },
  { key: "workload", title: "Workload" },
];

const ProjectAnalyticsPage: NextPageWithLayout = observer(() => {
  const router = useRouter();
  const { workspaceSlug, projectId } = router.query as {
    workspaceSlug: string;
    projectId: string;
  };

  const { cycle: cycleStore, project: projectStore } = useMobxStore();

  // Fetch cycles for the project
  useSWR(
    workspaceSlug && projectId ? `PROJECT_CYCLES_FOR_ANALYTICS_${projectId}` : null,
    workspaceSlug && projectId ? () => cycleStore.fetchCycles(workspaceSlug, projectId, "all") : null
  );

  // Fetch project details
  useSWR(
    workspaceSlug && projectId ? `PROJECT_DETAILS_${projectId}` : null,
    workspaceSlug && projectId ? () => projectStore.fetchProjectDetails(workspaceSlug, projectId) : null
  );

  const cycles = cycleStore.cycles[projectId] ?? [];
  const cycleOptions = cycles.map((c) => ({ id: c.id, name: c.name }));

  return (
    <div className="h-full flex flex-col overflow-hidden bg-custom-background-100">
      <Tab.Group as={Fragment}>
        <Tab.List as="div" className="space-x-2 border-b border-custom-border-200 px-5 py-3">
          {PROJECT_ANALYTICS_TABS.map((tab) => (
            <Tab
              key={tab.key}
              className={({ selected }) =>
                `rounded-3xl border border-custom-border-200 px-4 py-2 text-xs hover:bg-custom-background-80 ${
                  selected ? "bg-custom-background-80" : ""
                }`
              }
            >
              {tab.title}
            </Tab>
          ))}
        </Tab.List>
        <Tab.Panels as={Fragment}>
          <Tab.Panel as="div" className="h-full overflow-y-auto p-5">
            <BurndownChart cycles={cycleOptions} />
          </Tab.Panel>
          <Tab.Panel as="div" className="h-full overflow-y-auto p-5">
            <VelocityChart />
          </Tab.Panel>
          <Tab.Panel as="div" className="h-full overflow-y-auto p-5">
            <FlowDiagram />
          </Tab.Panel>
          <Tab.Panel as="div" className="h-full overflow-y-auto p-5">
            <WorkloadHeatmap cycles={cycleOptions} />
          </Tab.Panel>
        </Tab.Panels>
      </Tab.Group>
    </div>
  );
});

ProjectAnalyticsPage.getLayout = function getLayout(page: ReactElement) {
  return (
    <AppLayout header={<ProjectAnalyticsHeader />} withProjectWrapper>
      {page}
    </AppLayout>
  );
};

export default ProjectAnalyticsPage;
