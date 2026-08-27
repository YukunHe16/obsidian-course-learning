# Obsidian installation and UI setup

Read this workflow when initializing a semester, installing Obsidian, registering a vault, configuring core plugins, opening a study page, or verifying Bases and Graph. The steps below are the same for every agent; read [agent-compatibility.md](agent-compatibility.md) for the mechanism the current agent actually has.

## Capability and installation check

1. Determine what this agent can do to a live app before promising anything: Computer Use (Codex), a computer-use MCP server or the `obsidian` CLI plus screenshots (Claude Code), or nothing. If a step needs a capability you do not have, do not claim that GUI setup or verification succeeded; report the blocked portion and give the exact manual actions still needed.
2. On macOS, check both application locations and the CLI before deciding Obsidian is absent:

   ```bash
   test -d /Applications/Obsidian.app || \
     test -d "$HOME/Applications/Obsidian.app" || \
     command -v obsidian
   ```

3. If Obsidian is absent and the user asked to initialize the system, install the current macOS release from an official source only: the download page at <https://obsidian.md/download> (Computer Use, or `curl` on the release it links to), or `brew install --cask obsidian` when the user prefers a package manager. Never use an advertisement, mirror, or unofficial download page.
4. Downloading and installing the official Obsidian app is part of an explicit setup request. Still pause at the moment of any EULA, administrator credential, login, security-sensitive permission, or other unexpected authorization screen. Never type the user's password or enable Obsidian Sync without a separate request.
5. Launch Obsidian once (`open -a Obsidian`, or through Computer Use) and confirm the app window is live before continuing. This also registers the `obsidian://` URI handler and makes the `obsidian` CLI usable, since the CLI talks to the running app.
6. Confirm CLI access with `obsidian version`. The CLI is disabled by default; enabling it at **Settings > General > Advanced** is a one-time GUI action.

## Division of work

- Use shell scripts for deterministic file creation, source hashing, and validation.
- Use the `obsidian` CLI (Obsidian 1.13+) for vault inspection, core-plugin state, opening files, querying Bases, opening Graph view, and screenshots. Its output is checkable, so prefer it over blind clicking under any agent.
- The CLI is opt-in. Check it with `obsidian version`; if it reports that the command line interface is not enabled, turn it on once at **Settings > General > Advanced** with a GUI capability or by asking the user.
- Use Computer Use or an equivalent GUI capability for first launch, **Open folder as vault**, Settings screens, and anything the CLI cannot reach.
- `obsidian://` deep links may speed up navigation after registration, but they do not prove the UI is usable. Re-inspect Obsidian after using one.
- Re-read the current app state after UI actions. Do not reuse stale element identifiers or assume that a click succeeded.

## Register and configure the vaults

1. Register `<semester>/Overview` as a vault with **Open folder as vault**. There is no CLI command for registration; use the GUI capability, or the `obsidian.json` fallback in [agent-compatibility.md](agent-compatibility.md), or ask the user to do it. `obsidian command id=app:open-vault` opens the vault switcher.
2. Repeat for every `<semester>/Courses/<COURSE_ID>` directory. They must remain independent sibling vaults; never register the semester root or `Courses/` as a vault.
3. Confirm registration with `obsidian vaults verbose` before continuing.
4. In each vault, verify that these core plugins are enabled: **Bases**, **Backlinks**, **Graph view**, **Properties view**, **Templates**, and **File recovery**. Do not install or enable community plugins.

   ```bash
   obsidian vault=<VAULT> plugins:enabled filter=core
   obsidian vault=<VAULT> plugin:enable id=bases filter=core
   ```

5. Do not enable Sync, Publish, accounts, telemetry changes, or unrelated appearance settings unless the user separately requests them.

## Visible acceptance check

Perform and observe all of the following. Every item needs evidence you actually looked at — a screenshot you read back, or a Computer Use observation. Command exit codes alone are not acceptance.

1. Switch to the Overview vault and open `Home.md`.
2. Open `views/Semester.base` and confirm that Obsidian renders it as a Base rather than plain text or an error. `obsidian vault=<VAULT> base:query path=views/Semester.base view="<view>" format=md` additionally proves the view parses and returns rows.
3. Switch to each course vault and open `Home.md`.
4. Open the course Base views and confirm they render.
5. Open Graph view (`obsidian vault=<VAULT> command id=graph:open`) and confirm existing Wiki links appear as nodes and edges. A new empty course can have a sparse graph; report that honestly instead of inventing content.
6. Leave the most useful Home or requested study page open for the user.

```bash
obsidian vault=<VAULT> open path=Home.md
obsidian vault=<VAULT> dev:screenshot path=/tmp/<VAULT>-home.png   # then read the PNG back
```

Completion requires both structural validation from `validate_vault.py` and visible Obsidian verification. Report which vaults and pages were actually opened, how each one was observed, any UI step that remains, and whether user confirmation was required.
