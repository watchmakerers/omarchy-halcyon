# Halcyon apps

The Frutiger Aero apps from Halcyon Linux, ported to Omarchy: games, mail, photos, media player, Media Center, messenger, notes, calendar, search, gadgets, Navigator and the Welcome Center.

This folder is kept apart from Omarchy's own files so upstream updates merge cleanly. `omarchy-install-halcyon-apps` copies it to `~/.local/share/omarchy-halcyon`, installs the packages in `packages.txt`, and adds the launchers and menu entries. Window rules live in `default/hypr/apps/halcyon.lua`.

Halcyon Update is not included, because Omarchy has its own update system.
