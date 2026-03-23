# Claude Conversation Log

Session ID: agent-a9366a0bc741a8d15
Date: 2026-03-19 04:11:53

---

## 👤 User

I need to understand the full GitHub App OAuth callback flow in the Jet codebase. Find and read:

1. `web/hooks/use-integration-popup.tsx` - the popup hook that opens the OAuth window
2. Search for any callback pages: `web/pages/**/callback*` or `web/pages/**/github*`
3. Search for any OAuth callback handling: grep for `installation_id` in web/ directory
4. Read `apiserver/jet/api/views/integration/base.py` - the WorkspaceIntegrationViewSet create method (full file)
5. Check the web API URLs: `web/pages/api/` directory for any API routes
6. Search for `GITHUB_APP_NAME` or `NEXT_PUBLIC_GITHUB` in any config files, .env files, or docker-compose files
7. Read `docker-compose.yml` to understand environment variable configuration
8. Read `deploy/selfhost/variables.env` for environment variable templates
9. Search for any callback URL patterns in the codebase related to GitHub

Be very thorough - I need to understand the complete OAuth flow end-to-end.

---

## 🤖 Claude

I'll conduct a thorough investigation of the GitHub App OAuth callback flow. Let me start with parallel searches to cover all the areas you mentioned.

---

## 🤖 Claude

Good start. Now let me search for installation_id and GitHub-related patterns:

---

## 🤖 Claude

Great! Found some key files. Now let me read all the critical files:

---

## 🤖 Claude

Now let me search for more callback-related code and check the service that handles the installation:

---

## 🤖 Claude

Let me read these critical files:

---

## 🤖 Claude

Let me check the API URLs and routing structure:

---

## 🤖 Claude

Now let me check for environment variable configuration and Next.js API routes:

---

## 🤖 Claude

Now let me check for the slack-redirect API endpoint since I saw it referenced:

---

## 🤖 Claude

Now let me check the deploy files and turbo.json for more environment variable details:

---

## 🤖 Claude

Let me search for how GitHub App configuration is set up - looking for app ID and private key:

---

## 🤖 Claude

Let me check the architecture documentation:

---

## 🤖 Claude

Let me check the importer.py file for more context:

---

## 🤖 Claude

Perfect! Now I have enough information. Let me create a comprehensive summary document of the OAuth flow:

## GitHub App OAuth Callback Flow - Complete Documentation

Based on my thorough investigation of the Jet codebase, here is the complete GitHub App OAuth callback flow end-to-end:

---

### 1. **Frontend OAuth Initiation**

**File:** `/Users/sarathfrancis/work/git/innovation_lab/jet/web/hooks/use-integration-popup.tsx`

The OAuth flow starts with a popup hook that opens the GitHub App authorization URL:

```typescript
const providerUrls: { [key: string]: string } = {
  github: `https://github.com/apps/${
    process.env.NEXT_PUBLIC_GITHUB_APP_NAME
  }/installations/new?state=${workspaceSlug?.toString()}`,
  // ...
};
```

Key details:
- Uses `NEXT_PUBLIC_GITHUB_APP_NAME` environment variable to construct the GitHub authorization URL
- Passes `state` parameter containing the workspace slug to maintain context
- Opens in a popup window (600x600) to GitHub's app installation endpoint

---

### 2. **User Authorizes on GitHub**

The user:
1. Is redirected to GitHub's app authorization page
2. Grants permissions to the GitHub App
3. GitHub generates an `installation_id` and authorization code

GitHub redirects back to: `https://your-domain/installations/[provider]/`

With query parameters:
- `installation_id` - GitHub's app installation identifier
- `setup_action` - Action taken (e.g., "install", "update")
- `state` - The workspace slug passed in step 1
- `provider` - The integration provider (e.g., "github")

---

### 3. **Callback Handling Page**

**File:** `/Users/sarathfrancis/work/git/innovation_lab/jet/web/pages/installations/[provider]/index.tsx`

This is the critical callback handler. The flow:

```typescript
const AppPostInstallation: NextPageWithLayout = () => {
  const router = useRouter();
  const { installation_id, setup_action, state, provider, code } = router.query;

  useEffect(() => {
    if (provider === "github" && state && installation_id) {
      appInstallationService
        .addInstallationApp(state.toString(), provider, { installation_id })
        .then(() => {
          window.opener = null;
          window.open("", "_self");
          window.close();
        });
    }
    // Slack handling also present...
  }, [state, installation_id, provider, code]);

  return <Spinner />; // Shows loading screen
};
```

For GitHub, the page:
1. Extracts `installation_id` and `state` from query parameters
2. Calls the backend API to complete the installation
3. Closes the popup window after success

---

### 4. **Backend API Endpoint**

**File:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/api/urls/integration.py`

The endpoint called is:

```python
path(
    "workspaces/<str:slug>/workspace-integrations/<str:provider>/",
    WorkspaceIntegrationViewSet.as_view({
        "post": "create",
    }),
    name="workspace-integrations",
)
```

**API Route:** `POST /api/workspaces/{workspace_slug}/workspace-integrations/github/`

**Frontend Service Call:**
```typescript
// File: /Users/sarathfrancis/work/git/innovation_lab/jet/web/services/app_installation.service.ts
async addInstallationApp(workspaceSlug: string, provider: string, data: any): Promise<any> {
    return this.post(`/api/workspaces/${workspaceSlug}/workspace-integrations/${provider}/`, data)
}
```

---

### 5. **Backend Installation Processing**

**File:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/api/views/integration/base.py`

The `WorkspaceIntegrationViewSet.create()` method processes the installation:

```python
def create(self, request, slug, provider):
    workspace = Workspace.objects.get(slug=slug)
    integration = Integration.objects.get(provider=provider)
    config = {}
    
    if provider == "github":
        installation_id = request.data.get("installation_id", None)
        if not installation_id:
            return Response(
                {"error": "Installation ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Fetch GitHub metadata using the installation_id
        metadata = get_github_metadata(installation_id)
        config = {"installation_id": installation_id}
    
    # Create a bot user for the integration
    bot_user = User.objects.create(
        email=f"{uuid.uuid4().hex}@jetpm.app",
        username=uuid.uuid4().hex,
        password=make_password(uuid.uuid4().hex),
        is_password_autoset=True,
        is_bot=True,
        first_name=integration.title,
        avatar=integration.avatar_url or "",
    )
    
    # Create API token for the bot
    api_token = APIToken.objects.create(
        user=bot_user,
        user_type=1,  # bot user
        workspace=workspace,
    )
    
    # Create the workspace integration record
    workspace_integration = WorkspaceIntegration.objects.create(
        workspace=workspace,
        integration=integration,
        actor=bot_user,
        api_token=api_token,
        metadata=metadata,
        config=config,  # Contains installation_id
    )
    
    # Add bot user to workspace as member
    WorkspaceMember.objects.create(
        workspace=workspace_integration.workspace,
        member=bot_user,
        role=20,
    )
    
    return Response(
        WorkspaceIntegrationSerializer(workspace_integration).data,
        status=status.HTTP_201_CREATED,
    )
```

**Key processes:**
1. Validates `installation_id` is provided
2. Calls `get_github_metadata(installation_id)` to fetch installation details from GitHub API
3. Creates a bot user account for the integration
4. Creates an API token for the bot user
5. Creates a `WorkspaceIntegration` record storing:
   - `config`: Contains `installation_id`
   - `metadata`: GitHub API response data
   - `actor`: Bot user reference
6. Adds bot user to workspace members

---

### 6. **GitHub Metadata Retrieval**

**File:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/utils/integrations/github.py`

```python
def get_github_metadata(installation_id):
    token = get_jwt_token()  # Generate JWT from GitHub App credentials
    
    url = f"https://api.github.com/app/installations/{installation_id}"
    headers = {
        "Authorization": "Bearer " + str(token),
        "Accept": "application/vnd.github+json",
    }
    response = requests.get(url, headers=headers).json()
    return response
```

The JWT token is generated using:
- `GITHUB_APP_ID` environment variable
- `GITHUB_APP_PRIVATE_KEY` environment variable

```python
def get_jwt_token():
    app_id = os.environ.get("GITHUB_APP_ID", "")
    secret = bytes(os.environ.get("GITHUB_APP_PRIVATE_KEY", ""), encoding="utf8")
    current_timestamp = int(datetime.now().timestamp())
    due_date = datetime.now() + timedelta(minutes=10)
    expiry = int(due_date.timestamp())
    payload = {
        "iss": app_id,
        "sub": app_id,
        "exp": expiry,
        "iat": current_timestamp,
        "aud": "https://github.com/login/oauth/access_token",
    }
    priv_rsakey = load_pem_private_key(secret, None, default_backend())
    token = jwt.encode(payload, priv_rsakey, algorithm="RS256")
    return token
```

---

### 7. **Environment Variables Required**

**Frontend (Next.js):**
- `NEXT_PUBLIC_GITHUB_APP_NAME` - The GitHub App name (e.g., "my-jet-app")

**Backend (Django):**
- `GITHUB_APP_ID` - The GitHub App ID
- `GITHUB_APP_PRIVATE_KEY` - The private key for JWT signing

**Configuration Source:**
- `turbo.json` defines `NEXT_PUBLIC_GITHUB_APP_NAME` in globalEnv
- `docker-compose.yml` and `deploy/selfhost/docker-compose.yml` pass environment variables to containers
- `apiserver/.env.example` and `deploy/selfhost/variables.env` document template values

---

### 8. **Database Schema**

The flow creates/updates these records:

- **User** - Bot user for the integration
- **APIToken** - Token for bot user to interact with Jet API
- **WorkspaceIntegration** - Links workspace to GitHub App with:
  - `config`: `{"installation_id": "..."}` 
  - `metadata`: Full GitHub installation metadata response

---

### 9. **Uninstallation Flow**

**File:** `/Users/sarathfrancis/work/git/innovation_lab/jet/apiserver/jet/api/views/integration/base.py` (destroy method)

```python
def destroy(self, request, slug, pk):
    workspace_integration = WorkspaceIntegration.objects.get(pk=pk, workspace__slug=slug)
    
    if workspace_integration.integration.provider == "github":
        installation_id = workspace_integration.config.get("installation_id", False)
        if installation_id:
            delete_github_installation(installation_id=installation_id)
    
    workspace_integration.delete()
```

Calls `delete_github_installation()` to revoke the app access on GitHub.

---

### 10. **Complete Request Flow Diagram**

```
Browser                  GitHub              Jet Web              Jet API
  |                        |                    |                     |
  |---(click install)----->|                    |                     |
  |                        |                    |                     |
  |<---redirect w/ state----|                    |                     |
  |  & installation_id      |                    |                     |
  |                        |                    |                     |
  |---GET /installations/github?--- (popup)     |                     |
  |   installation_id=XXX&state=slug            |                     |
  |                        |                    |                     |
  |                        |          useEffect triggers              |
  |                        |                    |                     |
  |                        |         POST /api/workspaces/          |
  |                        |         {slug}/workspace-              |
  |                        |    integrations/github/--- with ------>|
  |                        |         {installation_id}  │            |
  |                        |                    |        │            |
  |                        |                    |        │    Generate JWT
  |                        |                    |        │    from App ID & Key
  |                        |                    |        │            |
  |                        |                    |        │    GET /api.github.com/
  |                        |                    |        │    app/installations/{id}
  |                        |<---OAuth API Response------|            |
  |                        |                    |        │            |
  |                        |                    |        │    Create Bot User
  |                        |                    |        │    Create API Token
  |                        |                    |        │    Create Integration
  |                        |                    |        │            |
  |                        |                    |<---200 OK---------|
  |<---close popup---------|                    |        |            |
  |                        |                    |        |            |
  (Installation Complete)
```

---

### Key Files Summary

| File | Purpose |
|------|---------|
| `web/hooks/use-integration-popup.tsx` | Opens GitHub OAuth popup with app URL |
| `web/pages/installations/[provider]/index.tsx` | Handles OAuth callback from GitHub |
| `web/services/app_installation.service.ts` | API service for installation endpoints |
| `apiserver/jet/api/views/integration/base.py` | Creates/deletes workspace integrations |
| `apiserver/jet/utils/integrations/github.py` | JWT generation and GitHub API calls |
| `apiserver/jet/api/urls/integration.py` | API routes for integrations |
| `turbo.json` | Frontend environment variable definitions |
| `docker-compose.yml` | Container environment configuration |

This complete flow ensures secure OAuth authentication with GitHub Apps and proper management of installation credentials within the Jet workspace system.

---

