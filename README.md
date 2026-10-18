# Mumble 1.5 client for Project Reality

**English** | [Русский](README.ru.md)

Mumble 1.5 client (default `v1.5.939`) for Windows, built from the official
sources <https://github.com/mumble-voip/mumble> with the PR patch
(`patches/`). It replaces the game's PRMumble 1.3 and works with the prmumble
server (<https://github.com/glukden-droid/prmumble>).

## Download

Builds are on the [Releases](https://github.com/glukden-droid/prmumble-client/releases) page:
`PRMumble-portable-win64.zip` for the game and an `.msi` (regular Mumble install).
The build version is `1.5.939-prN` (N = build number), shown in "About" and
in `PRMumble\VERSION.txt`.

## What the patch adds

Everything the PR launcher expects from PRMumble 1.3, details in `NOTES.md`:

- started by the launcher: `PRMumble.exe -m -z prmumble://name@ip:port`
  (`prmumble://` scheme, `-z` = minimized);
- the only plugin is ProjectReality (`plugins\ProjectReality.dll`, Mumble's
  Link plugin renamed), enabled by itself; the launcher writes the position and
  identity (team, squad, name, one-time password) to `MumbleLink`;
- own position goes to the server in `UserState` field 20 (as in 1.3: when it
  moved more than 10 on any axis), others are received;
- "who is talking" HUD: shared memory `PRMumbleSharedData1`, same format as 1.3;
- audio as in PRMumble 1.3: local voice is positional up to 75 m; squad radio,
  SL and commander are heard at full volume at any distance;
- shortcuts (squad radio, SL to SL, SL to commander, mute, deafen, volume) are
  also kept in `HKCU\SOFTWARE\Project Reality\PR Mumble\shortcuts` in the 1.3
  format: the launcher reads them for the HUD and writes its own binds there;
- no "load backup settings" question on every start (the launcher always kills
  the client);
- protocol field 20 = position, temporary access tokens moved to 120, as on the server.

## Install

1. Close the game and the launcher.
2. Keep the old folder: rename `mods\pr\bin\PRMumble` to `PRMumble_1.3`.
3. Unzip into `mods\pr\bin\` so that you get a `PRMumble` folder.
   Windows marks downloaded files as "from the internet" and shows
   "unknown publisher" (the build is not signed). Remove the mark once
   (PowerShell in `mods\pr\bin\PRMumble`):
   `Get-ChildItem -Recurse | Unblock-File`
4. Start the launcher and join a server; the launcher starts the new client.

Settings, certificate and database are kept in `PRMumble\data\` (without the
`data` folder the client works as a regular installed Mumble). PR shortcuts
are taken from the registry where PRMumble 1.3 left them.

The UI language follows Windows; change it in Settings → User Interface → Language.

Rollback: delete `PRMumble` and rename `PRMumble_1.3` back to `PRMumble`.

## Build

1. GitHub → **Actions** → **Mumble client** → **Run workflow**.
2. Optionally set another Mumble tag (e.g. `v1.5.940`).
3. Download the artifact:
   - `mumble-portable-<tag>-prN-win64` - the `PRMumble` folder;
   - `mumble-installer-<tag>-prN-win64` - a regular `.msi` installer (no portable mode).

## Checks

- `scripts\hud_dump.py` - what the client writes to the HUD shared memory (on the game PC);
- `scripts\pr_shortcuts.py` - PR shortcuts in the registry;
- `scripts\prmumble_cmdline.ps1` - how the launcher started the client.

## Code signing policy

Free code signing provided by [SignPath.io](https://about.signpath.io),
certificate by [SignPath Foundation](https://signpath.org) (applied for; until
then the builds are not signed).

- Committers and reviewers: [glukden-droid](https://github.com/glukden-droid)
- Approvers: [glukden-droid](https://github.com/glukden-droid)

Signed files are built only by the GitHub Actions workflow of this repository
from the official Mumble sources and `patches/`.

## Privacy policy

This program will not transfer any information to other networked systems
unless specifically requested by the user or the person installing or
operating it. The client connects only to the voice servers the user (or the
Project Reality launcher on the user's behalf) chooses. Mumble's update checks,
plugin update checks, usage statistics and crash reports are removed from this
build; the public server list is loaded only when the user opens it in the
Connect dialog.
