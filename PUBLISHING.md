# Publishing the MrScraper power for Kiro

Use this checklist for a public release and for the Kiro powers registry
submission.

## Release gate

- [ ] Merge only reviewed changes into `main`.
- [ ] Bump `version` in `plugin.json` and record user-visible changes in
      `CHANGELOG.md`. Never rename the power: Kiro uses `name` to identify an
      installed power.
- [ ] Keep `skills/` identical to the canonical MrScraper MCP skills and keep
      `legacy/` in sync (`.github/scripts/check_power.py` checks the
      latter).
- [ ] Confirm that the repository contains no credentials or private target
      data.
- [ ] Confirm the GitHub validation workflow passes.
- [ ] In a current Kiro IDE, install the power with **Add Custom Power** >
      **Import power from GitHub** and the repository URL. Confirm that Kiro
      offers one power, `mrscraper`, and not `legacy/` as a second one.
- [ ] Complete the OAuth sign-in and confirm that `power-mrscraper-mrscraper`
      exposes `scraperAPI`, `webSearch`, and `status`. The power cannot set
      OAuth scopes, so Kiro may request its defaults (`openid`, `email`,
      `profile`, `offline_access`). If sign-in fails with `invalid_scope`, or a
      tool returns `403 insufficient_scope`, stop: the authorization server has
      to grant `scrape:read` and `account:read` to such requests before the
      power can be released.
- [ ] Run the smoke-test prompts below in a new chat and check that the
      keywords activate the power.
- [ ] Repeat the install with the `legacy/` folder URL on a Kiro version
      before 1.0.288, if one is available.
- [ ] Tag the release (`v<version>`) and create a GitHub release.

Smoke-test prompts:

```text
Scrape https://www.scrapethissite.com/pages/simple/ and list the five most populous countries.
```

```text
Use Google search to find the official documentation for Playwright locators.
```

```text
How many MrScraper tokens do I have left?
```

## Kiro powers registry

Kiro lists third-party powers through the form at
[kiro.dev/powers/submit](https://kiro.dev/powers/submit/). There is no pull
request route: the `kirodotdev/powers` repository only hosts a subset of
powers and points contributors to the same form. Submitting the form means
agreeing to the
[Kiro Powers Publisher Terms and Conditions](https://kiro.dev/powers/terms)
and the AWS Privacy Notice, so a MrScraper employee with authority to bind
the company submits it. The terms require publishers to support users,
including for 90 days after a listing is removed, and to notify AWS
immediately of security issues that could affect Kiro users.

Kiro's requirements and where this repository meets them:

| Requirement | Where |
| --- | --- |
| Complete, tested, and working | Release gate above |
| Unique, specific use case | Web scraping and Google discovery; no scraping power is listed |
| MCP servers not in beta or preview | `https://mcp.mrscraper.com/mcp` is generally available |
| `plugin.json` with `$schema`, `name`, `version`, `description`, `author.name`, `keywords`, `license` | `plugin.json` |
| README links to a privacy policy and gives a support contact | README > Data and permissions, Support and security |
| Public GitHub repository | `https://github.com/mrscraper-com/mrscraper-kiro-power` |

Form values:

| Field | Value |
| --- | --- |
| Organization | MrScraper |
| Use case | Web scraping and search |
| Repository | `https://github.com/mrscraper-com/mrscraper-kiro-power` |
| Domain | Retrieving public web pages as HTML, Markdown, or screenshots, and Google search discovery, through MrScraper's hosted MCP server with OAuth |

Kiro contacts the submitter if the power fits the registry. When it is listed,
install it from [kiro.dev/powers](https://kiro.dev/powers) with **Add to
Kiro** and repeat the sign-in and smoke tests.
