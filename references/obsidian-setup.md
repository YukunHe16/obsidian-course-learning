# Obsidian installation and UI setup

Read this workflow when initializing a semester, installing Obsidian, registering a vault, configuring core plugins, opening a study page, or verifying Bases and Graph.

## Capability and installation check

1. Confirm that Computer Use is available in the current Codex desktop task. Use it for browser, Finder, installer, and Obsidian UI work. If it is unavailable, do not claim that GUI setup or verification succeeded; report the blocked portion and give the exact manual actions still needed.
2. On macOS, check both application locations and the CLI before deciding Obsidian is absent:

   ```bash
   test -d /Applications/Obsidian.app || \
     test -d "$HOME/Applications/Obsidian.app" || \
     command -v obsidian
   ```

3. If Obsidian is absent and the user asked to initialize the system, use Computer Use to visit the official download page at <https://obsidian.md/download>, download the current macOS release, and install it in Applications. Never use an advertisement, mirror, or unofficial download page. A Homebrew cask is an acceptable alternative only when the user prefers package-manager installation.
4. Downloading and installing the official Obsidian app is part of an explicit setup request. Still pause at the moment of any EULA, administrator credential, login, security-sensitive permission, or other unexpected authorization screen. Never type the user's password or enable Obsidian Sync without a separate request.
5. Launch Obsidian once through Computer Use. Confirm the app window is live before continuing; this also registers the `obsidian://` URI handler on macOS.

## Division of work

- Use shell scripts for deterministic file creation, source hashing, and validation.
- Use Computer Use for first launch, Vault switcher actions, **Open folder as vault**, Settings, core-plugin toggles, navigation, and visible verification.
- The `obsidian` CLI and `obsidian://` deep links may speed up navigation after registration, but they do not prove the UI is usable. Re-inspect Obsidian after using either one.
- Re-read the current app state after UI actions. Do not reuse stale element identifiers or assume that a click succeeded.

## Register and configure the vaults

1. In the Vault switcher, choose **Open folder as vault** and register `<semester>/Overview`.
2. Repeat for every `<semester>/Courses/<COURSE_ID>` directory. They must remain independent sibling vaults; never register the semester root or `Courses/` as a vault.
3. In each vault, verify that these core plugins are enabled: **Bases**, **Backlinks**, **Graph view**, **Properties view**, **Templates**, and **File recovery**. Do not install or enable community plugins.
4. Do not enable Sync, Publish, accounts, telemetry changes, or unrelated appearance settings unless the user separately requests them.

## Visible acceptance check

Use Computer Use to perform and observe all of the following:

1. Switch to the Overview vault and open `Home.md`.
2. Open `views/Semester.base` and confirm that Obsidian renders it as a Base rather than plain text or an error.
3. Switch to each course vault and open `Home.md`.
4. Open the course Base views and confirm they render.
5. Open Graph view and confirm existing Wiki links appear as nodes and edges. A new empty course can have a sparse graph; report that honestly instead of inventing content.
6. Leave the most useful Home or requested study page open for the user.

Completion requires both structural validation from `validate_vault.py` and visible Obsidian verification. Report which vaults and pages were actually opened, any UI step that remains, and whether user confirmation was required.
