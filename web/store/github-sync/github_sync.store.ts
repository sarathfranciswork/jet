import { action, makeObservable, observable, runInAction } from "mobx";
import { RootStore } from "store/root";
import { GithubSyncService } from "services/integrations/github_sync.service";
import {
  IGithubSyncConfig,
  IGithubPullRequest,
  IGithubUserMapping,
  IGithubSyncLog,
} from "types";

export interface IGithubSyncStore {
  syncConfigs: Record<string, IGithubSyncConfig>;
  pullRequests: Record<string, IGithubPullRequest[]>;
  userMappings: IGithubUserMapping[];
  syncLogs: IGithubSyncLog[];
  isLoading: boolean;

  fetchSyncConfig: (
    workspaceSlug: string,
    projectId: string,
    repoSyncId: string
  ) => Promise<void>;
  createSyncConfig: (
    workspaceSlug: string,
    projectId: string,
    repoSyncId: string,
    data: Partial<IGithubSyncConfig>
  ) => Promise<IGithubSyncConfig>;
  updateSyncConfig: (
    workspaceSlug: string,
    projectId: string,
    repoSyncId: string,
    configId: string,
    data: Partial<IGithubSyncConfig>
  ) => Promise<IGithubSyncConfig>;
  toggleSyncActive: (
    workspaceSlug: string,
    projectId: string,
    repoSyncId: string,
    configId: string,
    activate: boolean
  ) => Promise<void>;
  fetchPullRequests: (
    workspaceSlug: string,
    projectId: string,
    issueId?: string
  ) => Promise<void>;
  fetchUserMappings: (workspaceSlug: string) => Promise<void>;
  createUserMapping: (
    workspaceSlug: string,
    data: Partial<IGithubUserMapping>
  ) => Promise<IGithubUserMapping>;
  deleteUserMapping: (
    workspaceSlug: string,
    mappingId: string
  ) => Promise<void>;
  fetchSyncLogs: (
    workspaceSlug: string,
    projectId: string
  ) => Promise<void>;
}

export class GithubSyncStore implements IGithubSyncStore {
  syncConfigs: Record<string, IGithubSyncConfig> = {};
  pullRequests: Record<string, IGithubPullRequest[]> = {};
  userMappings: IGithubUserMapping[] = [];
  syncLogs: IGithubSyncLog[] = [];
  isLoading = false;

  rootStore: RootStore;
  githubSyncService: GithubSyncService;

  constructor(_rootStore: RootStore) {
    makeObservable(this, {
      syncConfigs: observable.ref,
      pullRequests: observable.ref,
      userMappings: observable.ref,
      syncLogs: observable.ref,
      isLoading: observable,
      fetchSyncConfig: action,
      createSyncConfig: action,
      updateSyncConfig: action,
      toggleSyncActive: action,
      fetchPullRequests: action,
      fetchUserMappings: action,
      createUserMapping: action,
      deleteUserMapping: action,
      fetchSyncLogs: action,
    });

    this.rootStore = _rootStore;
    this.githubSyncService = new GithubSyncService();
  }

  fetchSyncConfig = async (
    workspaceSlug: string,
    projectId: string,
    repoSyncId: string
  ) => {
    this.isLoading = true;
    try {
      const configs = await this.githubSyncService.getSyncConfig(
        workspaceSlug,
        projectId,
        repoSyncId
      );
      runInAction(() => {
        if (configs && configs.length > 0) {
          this.syncConfigs = {
            ...this.syncConfigs,
            [repoSyncId]: configs[0],
          };
        }
        this.isLoading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.isLoading = false;
      });
      throw error;
    }
  };

  createSyncConfig = async (
    workspaceSlug: string,
    projectId: string,
    repoSyncId: string,
    data: Partial<IGithubSyncConfig>
  ): Promise<IGithubSyncConfig> => {
    const config = await this.githubSyncService.createSyncConfig(
      workspaceSlug,
      projectId,
      repoSyncId,
      data
    );
    runInAction(() => {
      this.syncConfigs = { ...this.syncConfigs, [repoSyncId]: config };
    });
    return config;
  };

  updateSyncConfig = async (
    workspaceSlug: string,
    projectId: string,
    repoSyncId: string,
    configId: string,
    data: Partial<IGithubSyncConfig>
  ): Promise<IGithubSyncConfig> => {
    const config = await this.githubSyncService.updateSyncConfig(
      workspaceSlug,
      projectId,
      repoSyncId,
      configId,
      data
    );
    runInAction(() => {
      this.syncConfigs = { ...this.syncConfigs, [repoSyncId]: config };
    });
    return config;
  };

  toggleSyncActive = async (
    workspaceSlug: string,
    projectId: string,
    repoSyncId: string,
    configId: string,
    activate: boolean
  ) => {
    const result = activate
      ? await this.githubSyncService.activateSyncConfig(
          workspaceSlug,
          projectId,
          repoSyncId,
          configId
        )
      : await this.githubSyncService.deactivateSyncConfig(
          workspaceSlug,
          projectId,
          repoSyncId,
          configId
        );
    runInAction(() => {
      this.syncConfigs = { ...this.syncConfigs, [repoSyncId]: result };
    });
  };

  fetchPullRequests = async (
    workspaceSlug: string,
    projectId: string,
    issueId?: string
  ) => {
    const prs = await this.githubSyncService.getPullRequests(
      workspaceSlug,
      projectId,
      issueId
    );
    runInAction(() => {
      const key = issueId || projectId;
      this.pullRequests = { ...this.pullRequests, [key]: prs };
    });
  };

  fetchUserMappings = async (workspaceSlug: string) => {
    const mappings = await this.githubSyncService.getUserMappings(workspaceSlug);
    runInAction(() => {
      this.userMappings = mappings;
    });
  };

  createUserMapping = async (
    workspaceSlug: string,
    data: Partial<IGithubUserMapping>
  ): Promise<IGithubUserMapping> => {
    const mapping = await this.githubSyncService.createUserMapping(
      workspaceSlug,
      data
    );
    runInAction(() => {
      this.userMappings = [...this.userMappings, mapping];
    });
    return mapping;
  };

  deleteUserMapping = async (workspaceSlug: string, mappingId: string) => {
    await this.githubSyncService.deleteUserMapping(workspaceSlug, mappingId);
    runInAction(() => {
      this.userMappings = this.userMappings.filter((m) => m.id !== mappingId);
    });
  };

  fetchSyncLogs = async (workspaceSlug: string, projectId: string) => {
    const logs = await this.githubSyncService.getSyncLogs(
      workspaceSlug,
      projectId
    );
    runInAction(() => {
      this.syncLogs = logs;
    });
  };
}
