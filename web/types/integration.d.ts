// All the app integrations that are available
export interface IAppIntegration {
  author: string;
  author: "";
  avatar_url: string | null;
  created_at: string;
  created_by: string | null;
  description: any;
  id: string;
  metadata: any;
  network: number;
  provider: string;
  redirect_url: string;
  title: string;
  updated_at: string;
  updated_by: string | null;
  verified: boolean;
  webhook_secret: string;
  webhook_url: string;
}

export interface IWorkspaceIntegration {
  actor: string;
  api_token: string;
  config: any;
  created_at: string;
  created_by: string;
  id: string;
  integration: string;
  integration_detail: IIntegrations;
  metadata: any;
  updated_at: string;
  updated_by: string;
  workspace: string;
}

// slack integration
export interface ISlackIntegration {
  id: string;
  created_at: string;
  updated_at: string;
  access_token: string;
  scopes: string;
  bot_user_id: string;
  webhook_url: string;
  data: ISlackIntegrationData;
  team_id: string;
  team_name: string;
  created_by: string;
  updated_by: string;
  project: string;
  workspace: string;
  workspace_integration: string;
}

// GitHub Sync Integration Types
export interface IGithubSyncConfig {
  id: string;
  repository_sync: string;
  sync_direction: "bidirectional" | "github_to_jet";
  github_trigger_label: string;
  jet_trigger_label: string | null;
  state_mapping: Record<string, string>;
  pr_state_mapping: Record<string, string>;
  sync_comments: boolean;
  sync_labels: boolean;
  sync_assignees: boolean;
  webhook_secret: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  project: string;
  workspace: string;
}

export interface IGithubPullRequest {
  id: string;
  pr_number: number;
  github_pr_id: number;
  title: string;
  url: string;
  state: "draft" | "open" | "closed" | "merged";
  is_draft: boolean;
  issue: string | null;
  repository_sync: string;
  triggers_automation: boolean;
  author_login: string;
  author_avatar_url: string;
  merged_at: string | null;
  closed_at: string | null;
  created_at: string;
  updated_at: string;
  project: string;
  workspace: string;
}

export interface IGithubUserMapping {
  id: string;
  workspace: string;
  user: string;
  github_user_id: number;
  github_username: string;
  github_access_token: string;
  created_at: string;
  updated_at: string;
}

export interface IGithubSyncLog {
  id: string;
  repository_sync: string;
  entity_type: "issue" | "comment" | "label" | "pull_request" | "state" | "assignee";
  entity_id: string;
  direction: "github_to_jet" | "jet_to_github";
  status: "success" | "failed" | "skipped";
  error_message: string;
  payload: Record<string, any>;
  created_at: string;
  project: string;
  workspace: string;
}

export interface ISlackIntegrationData {
  ok: boolean;
  team: {
    id: string;
    name: string;
  };
  scope: string;
  app_id: string;
  enterprise: any;
  token_type: string;
  authed_user: string;
  bot_user_id: string;
  access_token: string;
  incoming_webhook: {
    url: string;
    channel: string;
    channel_id: string;
    configuration_url: string;
  };
  is_enterprise_install: boolean;
}
