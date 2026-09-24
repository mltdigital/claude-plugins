# MLT Digital Claude plugins

Private plugin marketplace for the MLT Digital team.

## Install (once)

From a terminal:

```bash
claude plugin marketplace add mltdigital/claude-plugins
claude plugin install eeat-html-builder@mlt-digital
```

Or inside a Claude Code session, type the same commands as slash commands (`/plugin marketplace add ...`,
`/plugin install ...`) in the chat box. They are not shell commands.

You need read access to this repo (SSH key or `gh auth login`).

## Get updates

```bash
claude plugin marketplace update mlt-digital
claude plugin update eeat-html-builder@mlt-digital
```

Then `/reload-plugins` or start a new session.

## Plugins

| Plugin | Version | What it does |
| --- | --- | --- |
| [eeat-html-builder](plugins/eeat-html-builder/) | 0.5.0 | Drop-in YMYL/EEAT HTML content blocks for law firm sites |

## Publishing a change (maintainer)

1. Edit under `plugins/<name>/`.
2. Bump `version` in `plugins/<name>/.claude-plugin/plugin.json` and in `.claude-plugin/marketplace.json`.
3. `claude plugin validate .` then commit and push to `main`.

Audit history lives in `docs/`.
