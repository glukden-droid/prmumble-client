# PRMumble client notes

Mumble 1.5 built as a drop-in replacement for PRMumble 1.3 (`mods\pr\bin\PRMumble`).
Server is a separate project: prmumble (github.com/glukden-droid/prmumble, Mumble 1.5 + PR patch).

## How the PR launcher uses the client
- Start: `<bin>\PRMumble\PRMumble.exe -m -z prmumble://<name>@<ip:port>` (WorkingDirectory = bin\PRMumble).
  -m = --multiple, -z = --minimize. Name: chars outside `[-=\w\[\]{}()|.]` replaced with `.`.
  Restarted when the mumble ip:port changes; stopped when mumble is disabled.
- The launcher (not the game) writes `MumbleLink` (standard LinkedMem):
  name "Project Reality: BF2", uiVersion=2, avatar/camera pos/front/top,
  identity JSON `{"commander":b,"squad_leader":b,"squad":n,"team":"blufor|opfor","name":"..","hash":"<account id>","pass":"<one-time password>"}`,
  context `{"ipport":"ip:port"}`. Not in game -> zero positions, empty identity.
  pass = one-time password from the game server, checked by the voice server.
- Squad/team/role in the identity can be wrong for a moment (death, respawn, camera);
  the server ignores changes shorter than 3 s.

## Talking HUD
- The client writes shared memory `Local\PRMumbleSharedData1` (the launcher tries 1..10), 32768 bytes, UTF-8.
- Records separated by `\x02`, fields by `\x01`: name, channel, talkstate (0..3), mute, deaf, x, y, z.
- name = "name" of the user's identity (else user name); position = UserState field 20
  (repeated float position), sent by each client, relayed by the server to the own team.
- Users listed: own channel and its links, plus users currently talking; self always;
  muted/deafened/suppressed users skipped.
- Launcher shows a user if talkstate is 1..3 and position != 0,0,0; local voice within 70 m.
  channel "commander" -> Commander, "squad N" -> Squad Leader N or "Squad" if N == own squad, else Local.

## Positional audio (PRMumble 1.3 defaults)
Positional on, headphone on, transmit position on, min distance 2.5 m, max distance 75 m,
volume beyond max 0, bloom 0.15. Only normal speech (local voice) is positional;
radio (whisper/shout) is heard at full volume.

## Shortcuts
- Kept in HKCU\SOFTWARE\Project Reality\PR Mumble\shortcuts in the Mumble 1.3 QSettings format
  (size, N\index, N\keys, N\data); the launcher reads them to show the transmit state and writes defaults.
- Values: "@Variant(<QDataStream Qt_4_0>)" as REG_BINARY. keys = list of [uint (DI instance << 8) | 4,
  device GUID]; data = 1.3 ShortcutTarget (users, forceCenter, channel, group, links, children),
  "@Invalid()" for PTT, DWORD 0 for mute/deaf. A shortcut with unparsable data is dropped by the launcher.
- PR indices: 1 PTT, 2 squad radio (current channel), 3 all SL, 4-12 SL1-9, 13 commander, 15 mute, 16 deafen,
  21 volume up, 22 volume down.
- Defaults: squad radio = current channel, forceCenter; SL all = group bf2_squad_leader;
  SL1..9 = bf2_first..ninth_squad_leader; commander = bf2_commander (children, forceCenter).

## Mumble 1.5 patch (patches/0001-project-reality.patch, source of truth: build\mumble + git diff)
main.cpp (portable data\, -z, prmumble://, HUD start, registry shortcuts load), Settings (positional
defaults, registry shortcuts save), PluginManager (Link auto-enable, send position), Messages
(identity/position in, resend position on ServerSync), Mumble.proto (20 = position, tokens 120),
AudioOutputSpeech (only normal speech positional), PRReality.*, PRShortcuts.*,
GlobalShortcut_win (1.5 -> 1.3 buttons). Built by the GitHub workflow.

Plugins: only link, renamed ProjectReality (ProjectReality.dll); game plugins and link_tester dropped.

## Tools
- scripts/prmumble_cmdline.ps1 - shows how the launcher started PRMumble.exe (run during a game).
- scripts/hud_dump.py - reads HUD shared memory on the game PC.
- scripts/pr_shortcuts.py - decodes the PR shortcuts in the registry.

## Vehicle icon in the HUD (idea, not done)
- HUD icons are font glyphs (voicechatfont_8 in fonts_client.zip), glyphs 26-29 = talking/disconnected/
  deafened/muted. The launcher prints the name field as is, so a glyph char in the name shows as an icon.
- Needs: game server python -> mumo (vehicle + seat per player) -> clients (server patch), glyphs added
  to the font (client mod file: every player needs it, may fail the launcher file check).
