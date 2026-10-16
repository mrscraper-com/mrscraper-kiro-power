---
name: "mrscraper"
displayName: "MrScraper Web Scraping"
description: "Scrape public web pages as HTML, Markdown, or screenshots, discover pages through Google search, and check account usage with MrScraper's hosted MCP server."
keywords: ["mrscraper", "scrape", "scraping", "scraper", "web scraping", "crawl", "serp", "google search", "page to markdown", "website screenshot"]
author: "MrScraper"
---

# MrScraper

## Overview

MrScraper gives Kiro agents live web data through a hosted MCP server. The
agent can retrieve a known public page as HTML, Markdown, or a screenshot,
discover pages through Google, and check the account's token usage.

**Key capabilities:**

- **Page retrieval**: fetch any public URL with automatic browser fallback,
  real-device routing, geo-targeted proxies, selector waits, and retry limits.
- **Google discovery**: search by query text or a Google search URL, with
  region, language, and page controls; parsed organic results come back as
  JSON.
- **Account usage**: subscription status, token usage, remaining tokens, and
  rate limits.
- **Retrieve first, extract locally**: the raw page response stays the source
  of truth, and summaries, tables, and JSON are derived from it locally.
- **OAuth 2.1**: Kiro signs in through the browser with dynamic client
  registration. No API key is stored in this power.

## When to Use This Power

Activate this power when the user:

- Gives a public URL and wants it read, summarized, archived, compared, or
  turned into structured data.
- Wants a page as Markdown, raw HTML, or a screenshot.
- Needs a page that renders with JavaScript or depends on the visitor's
  country.
- Asks to search Google, inspect search results, or find sources before
  reading them.
- Asks how many MrScraper tokens are left or what plan is active.

Do not use it for clicking through pages, filling in forms, logged-in browser
sessions, parsing local files, or scheduled monitoring.

## Onboarding

### Step 1: Connect the MrScraper MCP server

Kiro installs the server as `power-mrscraper-mrscraper`:

- **Connection:** Streamable HTTP at `https://mcp.mrscraper.com/mcp`
- **Authorization:** OAuth 2.1 with PKCE and dynamic client registration. No
  client ID, client secret, or API key is needed.

When Kiro first connects, it opens the MrScraper consent page in the browser.
The user signs in to MrScraper and approves access. Kiro stores and refreshes
the tokens. Never ask the user to paste an authorization code, access token,
or API key into the chat.

### Step 2: Confirm the tools

Check that the server exposes exactly these tools: `scraperAPI`, `webSearch`,
and `status`. If they are missing, ask the user to open the MCP servers tab in
the Kiro panel and reconnect `power-mrscraper-mrscraper`. Connection errors
appear under Output > "Kiro - MCP Logs".

### Step 3: Verify access

Call `status` with an empty object (`{}`). A successful account summary means
the connection is authorized. If it fails, report the error and do not claim
that setup is complete.

## Available Steering Files

| File | Purpose |
| --- | --- |
| [`steering/mrscraper.md`](./steering/mrscraper.md) | Connection, authentication, routing, response handling, account status, and troubleshooting |
| [`steering/mrscraper-fetch.md`](./steering/mrscraper-fetch.md) | Retrieving a known URL with `scraperAPI`: output formats, page-loading options, token cost, and retries |
| [`steering/mrscraper-serp.md`](./steering/mrscraper-serp.md) | Google discovery with `webSearch`: queries, locale, pagination, and parsed results |

## When to Load Steering Files

Load files with the `kiroPowers` tool, action `readSteering`, power name
`mrscraper`. Most tasks need one file.

- The user has a URL to read, convert, archive, or extract from →
  `mrscraper-fetch.md`
- The task starts with a question or query and no URL → `mrscraper-serp.md`,
  then `mrscraper-fetch.md` for the pages worth reading
- Setup, sign-in, missing tools, errors, or token usage → `mrscraper.md`

## Available MCP Servers

### mrscraper

- **Connection:** `https://mcp.mrscraper.com/mcp` (Streamable HTTP)
- **Authorization:** OAuth 2.1. Scopes: `scrape:read` for `scraperAPI` and
  `webSearch`, `account:read` for `status`.

| Tool | Purpose |
| --- | --- |
| `scraperAPI` | Retrieve a known public URL as HTML (default), Markdown, a base64 JPEG screenshot, or a combination. Required input: `url`. |
| `webSearch` | Search Google with query text or a Google search URL in `url`. Set `raw: false` for parsed JSON; organic results are in `data.data.organic`. |
| `status` | Report subscription status, token usage and limit, remaining tokens, rate limits, and renewal date. No inputs. |

Every tool returns `{status_code, data, headers}`, plus `error` on failure.
For `scraperAPI`, `headers["x-status-code"]` is the target page's own HTTP
status. Check `isError`, `error`, and both status codes before using `data`.

## MCP Configuration

```json
{
  "mcpServers": {
    "mrscraper": {
      "type": "http",
      "url": "https://mcp.mrscraper.com/mcp",
      "oauthScopes": ["scrape:read", "account:read", "offline_access"]
    }
  }
}
```

## Best Practices

- Start a page retrieval with the URL alone, then add browser rendering,
  `super`, `wait_for_selector`, or `geo_code` one at a time when the response
  shows they are needed.
- Request Markdown for readable text and HTML when an extractor needs the
  page structure. Request screenshots only when an image is needed, and save
  them to a file.
- For many pages with the same layout, retrieve a few samples, write one local
  extractor, then apply it to every saved response.
- Check `status` before a large batch. Use `token_cap` and `max_retries` to
  bound the cost of a single retrieval.
- Save large intermediate results under the project's `.mrscraper/` directory
  and keep it out of version control.
- Only retrieve content the user is allowed to access, and follow the target
  site's terms.

## Troubleshooting

- **Tools missing:** reconnect `power-mrscraper-mrscraper` in the MCP servers
  tab, then check "Kiro - MCP Logs".
- **401 or expired sign-in:** reconnect the server so Kiro runs the OAuth
  flow again.
- **403 insufficient_scope:** reauthorize so Kiro requests the missing scope.
- **Page incomplete or blocked:** load `mrscraper-fetch.md` and change one
  page-loading option at a time.
- **Weak search results:** load `mrscraper-serp.md` and set `region` and
  `language`, or rewrite the query.

## License and support

This power is MIT-licensed and connects to the hosted
[MrScraper MCP server](https://docs.mrscraper.com/docs/getting-started/mcp-server).

- [Privacy Policy](https://mrscraper.com/privacy-policy)
- [Terms of Use](https://mrscraper.com/terms-of-use)
- [Acceptable Use Policy](https://mrscraper.com/acceptable-use-policy)
- Support: [support@mrscraper.com](mailto:support@mrscraper.com)
