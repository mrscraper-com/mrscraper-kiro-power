# MrScraper power for Kiro

MrScraper connects [Kiro](https://kiro.dev) to a hosted MCP server for
retrieving public web pages as HTML, Markdown, or screenshots, Google
discovery, and account usage. The power also includes three skills that help
the agent choose the right workflow and keep raw page content.

The power follows the [Agent Plugins](https://agent-plugins.org/) 1.0.0
format that Kiro uses for [powers](https://kiro.dev/docs/powers/).

## What this power adds

- The hosted Streamable HTTP endpoint at `https://mcp.mrscraper.com/mcp`.
  Kiro installs it as `power-mrscraper-mrscraper` and connects it only while
  the power is active.
- OAuth 2.1 sign-in through Kiro's MCP client, with dynamic client
  registration. This repository stores no credentials.
- Skills: `mrscraper`, `mrscraper-fetch`, and `mrscraper-serp`.
- Activation keywords such as `scrape`, `scraping`, `web scraping`, `crawl`,
  `serp`, `google search`, and `mrscraper`.

## Requirements

- [Kiro IDE](https://kiro.dev/downloads/) 1.0.288 or later. Older versions
  can use the [`legacy/`](legacy/) package instead.
- A [MrScraper](https://app.mrscraper.com) account.
- A local browser for the OAuth sign-in.
- Permission to access and process the target content.

## Install

In the Kiro IDE:

1. Open the **Powers** panel and select **Add Custom Power**.
2. Select **Import power from GitHub**.
3. Enter `https://github.com/mrscraper-com/mrscraper-kiro-power` and select
   **Install**.

To install from a local clone instead, choose **Import power from a folder**
and select the cloned `mrscraper-kiro-power` directory.

## Sign in

The first time the power connects, Kiro discovers MrScraper's authorization
server, registers itself, and opens the MrScraper consent page in your
browser. Sign in to MrScraper and approve access. Kiro stores and refreshes the
tokens. Never paste OAuth tokens or API keys into the chat.

The power's server, `power-mrscraper-mrscraper`, then exposes these tools.
If it does not connect, check Output > **Kiro - MCP Logs** in the Kiro panel.

| Tool | Purpose |
| --- | --- |
| `scraperAPI` | Retrieve a known page as HTML, Markdown, a screenshot, or a combination. |
| `webSearch` | Discover public pages through Google. |
| `status` | Inspect subscription status, token usage, and remaining tokens. |

The OAuth scopes are `scrape:read` (`scraperAPI` and `webSearch`) and
`account:read` (`status`). Revoke access at any time under Connected
applications in your MrScraper account.

## Try it

Select **Try power** in the Powers panel, or ask in a Kiro chat:

```text
Scrape https://www.scrapethissite.com/pages/simple/ and list the five most populous countries.
```

```text
Use Google search to find the official documentation for Playwright locators, then summarize the top result.
```

```text
How many MrScraper tokens do I have left?
```

Kiro asks for approval before it runs MCP tools unless you have trusted them.

## Retrieve-first routing

When a public URL is already known, the skills direct the agent to retrieve it
with `scraperAPI` first and treat the raw response as the source of truth. The
agent can then read, summarize, compare, or derive structured output locally
without losing details. When no URL is known, `webSearch` finds candidate pages
first. For many pages with the same layout, the agent retrieves a few samples,
writes one local extractor, and applies it to every saved response.

## Older Kiro versions

Kiro versions before 1.0.288 read the original `POWER.md` power format. The
[`legacy/`](legacy/) folder holds the same power in that format: `POWER.md`,
an `mcp.json` for the same hosted server, and the three skills as steering
files. Install it with **Import power from GitHub** and the URL
`https://github.com/mrscraper-com/mrscraper-kiro-power/tree/main/legacy`.
Install only one of the two packages.

## Connect the MCP server without the power

To add only the MCP server, put this entry in `~/.kiro/settings/mcp.json` (all
workspaces) or `.kiro/settings/mcp.json` (one workspace). Open either file from
the command palette with **Kiro: Open user MCP config (JSON)** or **Kiro: Open
workspace MCP config (JSON)**.

```json
{
  "mcpServers": {
    "mrscraper": {
      "url": "https://mcp.mrscraper.com/mcp",
      "oauthScopes": ["scrape:read", "account:read", "offline_access"]
    }
  }
}
```

`oauthScopes` asks for MrScraper's own scopes instead of Kiro's default
OpenID scopes. Kiro reconnects when you save the file and then opens the
consent page as described above.

### API key fallback

Use OAuth whenever possible. If OAuth cannot complete, create an
[API key](https://app.mrscraper.com/api-tokens), export it as
`MRSCRAPER_API_KEY` in the environment Kiro starts from, and send it as a
bearer token from your user-level `~/.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "mrscraper": {
      "url": "https://mcp.mrscraper.com/mcp",
      "headers": {
        "Authorization": "Bearer ${MRSCRAPER_API_KEY}"
      }
    }
  }
}
```

Kiro expands only approved variables: open Kiro settings, search for **Mcp
Approved Env Vars**, and add `MRSCRAPER_API_KEY`. An API key carries full
account authority, so never put it in a workspace file that is committed.

The power's own server always uses OAuth. With the API key fallback, skip the
power and copy only its skills to `~/.kiro/skills/` (all workspaces) or
`.kiro/skills/` (one workspace):

```bash
git clone --depth 1 https://github.com/mrscraper-com/mrscraper-kiro-power.git
mkdir -p ~/.kiro/skills
cp -R mrscraper-kiro-power/skills/* ~/.kiro/skills/
```

## Data and permissions

The power sends MCP tool inputs, including target URLs and search queries, to
MrScraper's hosted service. Page responses and tool results are then available
to the agent for the requested task. Use it only with public or otherwise
authorized content, and follow the target site's requirements.

Review MrScraper's [MCP documentation](https://docs.mrscraper.com/docs/getting-started/mcp-server),
[Privacy Policy](https://mrscraper.com/privacy-policy),
[Terms of Use](https://mrscraper.com/terms-of-use), and
[Acceptable Use Policy](https://mrscraper.com/acceptable-use-policy) before
use.

## Update

Open the power in the Powers panel, select **Check for updates**, then
**Install updates**. Kiro refreshes the power from this repository.

## Support and security

- Product help: [MrScraper MCP documentation](https://docs.mrscraper.com/docs/getting-started/mcp-server)
- Bugs and feature requests: [GitHub Issues](https://github.com/mrscraper-com/mrscraper-kiro-power/issues)
- Account help: [support@mrscraper.com](mailto:support@mrscraper.com)
- Security reports: see [SECURITY.md](SECURITY.md)

## Development

```text
plugin.json        Agent Plugins 1.0.0 manifest: name, version, keywords
mcp.json           hosted MCP server (streamable-http, OAuth)
skills/            mrscraper, mrscraper-fetch, mrscraper-serp
legacy/            the same power in the POWER.md format for Kiro < 1.0.288
```

Run the structural checks on a local checkout:

```bash
python3 .github/scripts/check_power.py
```

The [validation workflow](.github/workflows/validate.yml) also validates
`plugin.json` and `mcp.json` against the published Agent Plugins 1.0.0
schemas and each skill with the Agent Skills reference validator. Test the
power in the Kiro IDE with **Import power from a folder** before a release.

The skills are copied unchanged from the canonical MrScraper MCP skills, and
the legacy steering files must match them. Record user-visible changes in
[CHANGELOG.md](CHANGELOG.md) and use [PUBLISHING.md](PUBLISHING.md) for the
release and Kiro submission checklist.

## License

[MIT](LICENSE)
