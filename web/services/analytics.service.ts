// services
import { APIService } from "services/api.service";
// types
import {
  IAnalyticsParams,
  IAnalyticsResponse,
  IBurndownResponse,
  IDefaultAnalyticsResponse,
  IExportAnalyticsFormData,
  IFlowResponse,
  ISaveAnalyticsFormData,
  IVelocityResponse,
  IWorkloadResponse,
} from "types";
// helpers
import { API_BASE_URL } from "helpers/common.helper";

export class AnalyticsService extends APIService {
  constructor() {
    super(API_BASE_URL);
  }

  async getAnalytics(workspaceSlug: string, params: IAnalyticsParams): Promise<IAnalyticsResponse> {
    return this.get(`/api/workspaces/${workspaceSlug}/analytics/`, {
      params: {
        ...params,
        project: params?.project ? params.project.toString() : null,
      },
    })
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async getDefaultAnalytics(
    workspaceSlug: string,
    params?: Partial<IAnalyticsParams>
  ): Promise<IDefaultAnalyticsResponse> {
    return this.get(`/api/workspaces/${workspaceSlug}/default-analytics/`, {
      params: {
        ...params,
        project: params?.project ? params.project.toString() : null,
      },
    })
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async saveAnalytics(workspaceSlug: string, data: ISaveAnalyticsFormData): Promise<any> {
    return this.post(`/api/workspaces/${workspaceSlug}/analytic-view/`, data)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async exportAnalytics(workspaceSlug: string, data: IExportAnalyticsFormData): Promise<any> {
    return this.post(`/api/workspaces/${workspaceSlug}/export-analytics/`, data)
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  // Project-level analytics
  async getProjectBurndown(
    workspaceSlug: string,
    projectId: string,
    params: { cycle_id: string; metric?: "count" | "points" }
  ): Promise<IBurndownResponse> {
    return this.get(
      `/api/workspaces/${workspaceSlug}/projects/${projectId}/analytics/burndown/`,
      { params }
    )
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async getProjectVelocity(
    workspaceSlug: string,
    projectId: string,
    params?: { last_n_cycles?: number }
  ): Promise<IVelocityResponse> {
    return this.get(
      `/api/workspaces/${workspaceSlug}/projects/${projectId}/analytics/velocity/`,
      { params }
    )
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async getProjectFlow(
    workspaceSlug: string,
    projectId: string,
    params: { start_date: string; end_date: string }
  ): Promise<IFlowResponse> {
    return this.get(
      `/api/workspaces/${workspaceSlug}/projects/${projectId}/analytics/flow/`,
      { params }
    )
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }

  async getProjectWorkload(
    workspaceSlug: string,
    projectId: string,
    params?: { cycle_id?: string }
  ): Promise<IWorkloadResponse> {
    return this.get(
      `/api/workspaces/${workspaceSlug}/projects/${projectId}/analytics/workload/`,
      { params }
    )
      .then((response) => response?.data)
      .catch((error) => {
        throw error?.response?.data;
      });
  }
}
