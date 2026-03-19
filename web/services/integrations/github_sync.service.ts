import { APIService } from "services/api.service";
import { API_BASE_URL } from "helpers/common.helper";
import {
  IGithubSyncConfig,
  IGithubPullRequest,
  IGithubUserMapping,
  IGithubSyncLog,
} from "types";

export class GithubSyncService extends APIService {
  constructor() {
    super(API_BASE_URL);
  }

  // --- Sync Config ---

  async getSyncConfig(
    workspaceSlug: string,
    projectId: string,
    repoSyncId: string
  ): Promise<IGithubSyncConfig[]> {
    return this.get(
      `/api/workspaces/${workspaceSlug}/projects/${projectId}/github-repository-sync/${repoSyncId}/sync-config/`
    )
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async createSyncConfig(
    workspaceSlug: string,
    projectId: string,
    repoSyncId: string,
    data: Partial<IGithubSyncConfig>
  ): Promise<IGithubSyncConfig> {
    return this.post(
      `/api/workspaces/${workspaceSlug}/projects/${projectId}/github-repository-sync/${repoSyncId}/sync-config/`,
      data
    )
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async updateSyncConfig(
    workspaceSlug: string,
    projectId: string,
    repoSyncId: string,
    configId: string,
    data: Partial<IGithubSyncConfig>
  ): Promise<IGithubSyncConfig> {
    return this.patch(
      `/api/workspaces/${workspaceSlug}/projects/${projectId}/github-repository-sync/${repoSyncId}/sync-config/${configId}/`,
      data
    )
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async activateSyncConfig(
    workspaceSlug: string,
    projectId: string,
    repoSyncId: string,
    configId: string
  ): Promise<IGithubSyncConfig> {
    return this.post(
      `/api/workspaces/${workspaceSlug}/projects/${projectId}/github-repository-sync/${repoSyncId}/sync-config/${configId}/activate/`
    )
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async deactivateSyncConfig(
    workspaceSlug: string,
    projectId: string,
    repoSyncId: string,
    configId: string
  ): Promise<IGithubSyncConfig> {
    return this.post(
      `/api/workspaces/${workspaceSlug}/projects/${projectId}/github-repository-sync/${repoSyncId}/sync-config/${configId}/deactivate/`
    )
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async deleteSyncConfig(
    workspaceSlug: string,
    projectId: string,
    repoSyncId: string,
    configId: string
  ): Promise<void> {
    return this.delete(
      `/api/workspaces/${workspaceSlug}/projects/${projectId}/github-repository-sync/${repoSyncId}/sync-config/${configId}/`
    )
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  // --- User Mappings ---

  async getUserMappings(workspaceSlug: string): Promise<IGithubUserMapping[]> {
    return this.get(`/api/workspaces/${workspaceSlug}/github-user-mappings/`)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async createUserMapping(
    workspaceSlug: string,
    data: Partial<IGithubUserMapping>
  ): Promise<IGithubUserMapping> {
    return this.post(
      `/api/workspaces/${workspaceSlug}/github-user-mappings/`,
      data
    )
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async deleteUserMapping(
    workspaceSlug: string,
    mappingId: string
  ): Promise<void> {
    return this.delete(
      `/api/workspaces/${workspaceSlug}/github-user-mappings/${mappingId}/`
    )
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  // --- Pull Requests ---

  async getPullRequests(
    workspaceSlug: string,
    projectId: string,
    issueId?: string
  ): Promise<IGithubPullRequest[]> {
    const params = issueId ? `?issue_id=${issueId}` : "";
    return this.get(
      `/api/workspaces/${workspaceSlug}/projects/${projectId}/github-pull-requests/${params}`
    )
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  // --- Sync Logs ---

  async getSyncLogs(
    workspaceSlug: string,
    projectId: string
  ): Promise<IGithubSyncLog[]> {
    return this.get(
      `/api/workspaces/${workspaceSlug}/projects/${projectId}/github-sync-logs/`
    )
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }
}
