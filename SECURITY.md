# Security Policy

Please report suspected vulnerabilities privately to
[support@mrscraper.com](mailto:support@mrscraper.com). Include the affected
component, reproduction steps, and potential impact. Do not open a public issue
for an unpatched vulnerability or include credentials, tokens, customer data,
or private target content in a report.

This repository contains no MrScraper credentials. Authentication is handled
by Kiro's OAuth 2.1 MCP connection, which stores and refreshes the tokens. If
you use the API key fallback, the key stays in your own environment and
user-level Kiro MCP configuration and carries full account authority. If a
credential may have been exposed, revoke it through the relevant account or
client immediately and then contact support.
