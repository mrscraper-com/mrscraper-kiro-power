# Changelog

All notable changes to the MrScraper power for Kiro are documented here. The
project follows [Semantic Versioning](https://semver.org/); the version is in
`plugin.json`.

## 0.1.0 - 2026-10-16

- First release of the MrScraper power for Kiro, in the Agent Plugins 1.0.0
  format (`plugin.json`, `mcp.json`, `skills/`).
- Hosted MCP server `https://mcp.mrscraper.com/mcp` (Streamable HTTP, OAuth 2.1
  with dynamic client registration) exposing `scraperAPI`, `webSearch`, and
  `status`. Kiro installs it as `power-mrscraper-mrscraper`.
- Skills: `mrscraper`, `mrscraper-fetch`, and `mrscraper-serp`, identical to
  the canonical MrScraper MCP skills.
- `legacy/`: the same power in the `POWER.md` format with steering files, for
  Kiro versions before 1.0.288.
- Validation workflow: Agent Plugins schemas, the Agent Skills reference
  validator, and structural checks.
