# Python Hub

This is your personal Python Hub — a terminal-based launcher that auto-detects
games, scripts, and info files inside the `Python/` folder and lets you run them.

## Quick start
1. Put Python files in `Python/<category>/` (e.g. `games/`, `scripts/`).
2. Edit `config.txt` to change the title, subtitle or theme.
3. Edit `settings.txt` to change animation style.
4. (Optional) Add `sounds/*.wav` (click.wav, open.wav, exit.wav).
5. Run `python menu.py`.

## Config
`config.txt` contains:

title = HURON
subtitle = AI-LINUX v1.0
theme = cyber_neon
sound = on

## Settings
`settings.txt` contains:
animation = spinner or progress, diagonal, dots (dots means the simple "..." 
animation). The menu will read this and apply the chosen animation.

## Themes
Look in `themes/` for available theme JSON files.

## Notes
- For Termux sound playback, install `termux-api` and allow audio playback.
- For richer system info install `psutil` (`pip install psutil`).
