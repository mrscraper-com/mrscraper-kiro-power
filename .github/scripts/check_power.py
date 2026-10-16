#!/usr/bin/env python3
"""Structural checks for the MrScraper Kiro power.

Covers what the JSON schemas and the Agent Skills validator do not: Kiro's
submission requirements, the hosted MCP endpoint, and that the legacy
POWER.md package stays in sync with the Agent Plugins package.

Usage: python3 .github/scripts/check_power.py [repo-root]
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
LEGACY = ROOT / "legacy"

PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
MANIFEST_FIELDS = {
    "$schema", "name", "version", "description", "author", "homepage",
    "repository", "license", "keywords", "extensions",
}
NAME_RE = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
ENDPOINT = "https://mcp.mrscraper.com/mcp"
SKILLS = ["mrscraper", "mrscraper-fetch", "mrscraper-serp"]
LINK_RE = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")

errors = []


def check(condition, message):
    if not condition:
        errors.append(message)
    return condition


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}


def frontmatter(path):
    """Parse the simple YAML frontmatter used here: scalars, quoted strings,
    inline JSON lists, and `|` block scalars."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not check(match, f"{path.relative_to(ROOT)}: missing frontmatter"):
        return {}, text
    fields, lines, i = {}, match.group(1).split("\n"), 0
    while i < len(lines):
        key, _, value = lines[i].partition(":")
        value = value.strip()
        if value == "|":
            block = []
            while i + 1 < len(lines) and (lines[i + 1].startswith("  ") or not lines[i + 1].strip()):
                i += 1
                block.append(lines[i][2:])
            value = "\n".join(block).strip()
        elif value.startswith(("[", '"')):
            value = json.loads(value)
        fields[key.strip()] = value
        i += 1
    return fields, text[match.end():]


def check_links(path, root):
    for target in LINK_RE.findall(path.read_text(encoding="utf-8")):
        if re.match(r"^[a-z]+:", target):
            continue
        resolved = (path.parent / target).resolve()
        check(resolved.is_relative_to(root) and resolved.exists(),
              f"{path.relative_to(ROOT)}: broken or escaping link {target}")


# plugin.json
manifest = load_json(ROOT / "plugin.json")
check(set(manifest) <= MANIFEST_FIELDS,
      f"plugin.json: fields outside Agent Plugins 1.0.0: {sorted(set(manifest) - MANIFEST_FIELDS)}")
check(manifest.get("$schema") == PLUGIN_SCHEMA, "plugin.json: wrong $schema")
check(manifest.get("name") == "mrscraper" and NAME_RE.match(manifest.get("name", "")),
      "plugin.json: name must be mrscraper")
check(SEMVER_RE.match(str(manifest.get("version", ""))), "plugin.json: version must be semver")
check(isinstance(manifest.get("description"), str) and manifest.get("description"),
      "plugin.json: description required")
author = manifest.get("author", {})
check(isinstance(author, dict) and author.get("name"), "plugin.json: author.name required")
check(author.get("url") and author.get("email"), "plugin.json: author.url and author.email recommended")
keywords = manifest.get("keywords", [])
check(isinstance(keywords, list) and keywords and all(isinstance(k, str) and k for k in keywords),
      "plugin.json: keywords must be a non-empty list of strings")
check(len(keywords) == len({k.lower() for k in keywords}), "plugin.json: duplicate keywords")
check(manifest.get("license") == "MIT", "plugin.json: license must be MIT (SPDX)")
check(manifest.get("repository") == "https://github.com/mrscraper-com/mrscraper-kiro-power",
      "plugin.json: unexpected repository")

# mcp.json
mcp = load_json(ROOT / "mcp.json")
check(set(mcp) == {"$schema", "mcpServers"}, "mcp.json: only $schema and mcpServers allowed")
check(mcp.get("$schema") == MCP_SCHEMA, "mcp.json: wrong $schema")
server = mcp.get("mcpServers", {}).get("mrscraper", {})
check(list(mcp.get("mcpServers", {})) == ["mrscraper"], "mcp.json: expected one server named mrscraper")
check(server == {"type": "streamable-http", "url": ENDPOINT},
      "mcp.json: mrscraper must be streamable-http at the hosted endpoint, with no headers")

# skills/
found = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
check(found == sorted(SKILLS), f"skills/: expected {SKILLS}, found {found}")
skill_bodies = {}
for name in SKILLS:
    path = ROOT / "skills" / name / "SKILL.md"
    if not check(path.is_file(), f"skills/{name}/SKILL.md missing"):
        continue
    fields, _ = frontmatter(path)
    check(fields.get("name") == name and SKILL_NAME_RE.match(name),
          f"skills/{name}: frontmatter name must match the directory")
    description = fields.get("description", "")
    check(0 < len(description) <= 1024, f"skills/{name}: description must be 1-1024 characters")
    check_links(path, ROOT)
    skill_bodies[name] = path.read_text(encoding="utf-8")

# legacy/ (POWER.md format)
power, power_body = frontmatter(LEGACY / "POWER.md")
for field in ("name", "displayName", "description", "keywords", "author"):
    check(power.get(field), f"legacy/POWER.md: frontmatter {field} required")
check(power.get("name") == manifest.get("name"), "legacy/POWER.md: name differs from plugin.json")
check(power.get("description") == manifest.get("description"),
      "legacy/POWER.md: description differs from plugin.json")
check(power.get("keywords") == keywords, "legacy/POWER.md: keywords differ from plugin.json")
check(power.get("author") == author.get("name"), "legacy/POWER.md: author differs from plugin.json")
check_links(LEGACY / "POWER.md", LEGACY)

legacy_mcp = load_json(LEGACY / "mcp.json")
legacy_server = legacy_mcp.get("mcpServers", {}).get("mrscraper", {})
check(list(legacy_mcp.get("mcpServers", {})) == ["mrscraper"],
      "legacy/mcp.json: expected one server named mrscraper")
check(legacy_server.get("url") == ENDPOINT, "legacy/mcp.json: wrong endpoint")
check("headers" not in legacy_server and "env" not in legacy_server,
      "legacy/mcp.json: must not ship headers or env")
check("### mrscraper" in power_body, "legacy/POWER.md: must document the mrscraper server")

steering = sorted(p.stem for p in (LEGACY / "steering").glob("*.md"))
check(steering == sorted(SKILLS), f"legacy/steering: expected {SKILLS}, found {steering}")
for name, body in skill_bodies.items():
    path = LEGACY / "steering" / f"{name}.md"
    if not path.is_file():
        continue
    expected = re.sub(r"\(\.\./([a-z-]+)/SKILL\.md\)", r"(\1.md)", body)
    check(path.read_text(encoding="utf-8") == expected,
          f"legacy/steering/{name}.md: differs from skills/{name}/SKILL.md")
    check(f"steering/{name}.md" in power_body, f"legacy/POWER.md: does not list steering/{name}.md")
    check_links(path, LEGACY)

# Kiro submission requirements
readme = (ROOT / "README.md").read_text(encoding="utf-8")
check("https://mrscraper.com/privacy-policy" in readme, "README.md: must link to the privacy policy")
check("support@mrscraper.com" in readme, "README.md: must give a support contact")
check_links(ROOT / "README.md", ROOT)
check((ROOT / "LICENSE").read_text(encoding="utf-8").startswith("MIT License"), "LICENSE: must be MIT")

if errors:
    print("\n".join(f"error: {e}" for e in errors))
    sys.exit(1)
print(f"ok: mrscraper {manifest['version']}, {len(skill_bodies)} skills, "
      f"{len(keywords)} keywords, legacy package in sync")
