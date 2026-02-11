#!/usr/bin/env python3
"""
PythonHub menu.py
Full-featured launcher:
- auto-detects subfolders under 'Python/'
- two-step navigation (folder -> file)
- themes (themes/*.json)
- animations (spinner/progress/diagonal/dots)
- sound support (termux-media-player or playsound fallback)
- safe execution modes (interactive OR capture + error display)
- config stored in config.txt
- settings stored in settings.txt
"""

import os
import sys
import json
import time
import subprocess
import traceback

ROOT = os.path.dirname(os.path.abspath(__file__))
PY_CONTENT = os.path.join(ROOT, "Python")
THEME_DIR = os.path.join(ROOT, "themes")
SOUND_DIR = os.path.join(ROOT, "sounds")
CONFIG_FILE = os.path.join(ROOT, "config.txt")
SETTINGS_FILE = os.path.join(ROOT, "settings.txt")
IGNORE_LIST = {"themes", "sounds", "menu.py", "config.txt", "README.md", "settings.txt", "update_readme.py"}

# ------------------------
# Utility functions
# ------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def safe_input(prompt=""):
    try:
        return input(prompt)
    except EOFError:
        return ""

# ------------------------
# Config loader/saver
# ------------------------
DEFAULT_CONFIG = {
    "title": "HURON",
    "subtitle": "AI-LINUX v1.0",
    "theme": "cyber_neon",
    "sound": "on"
}

def load_config():
    cfg = DEFAULT_CONFIG.copy()
    if not os.path.exists(CONFIG_FILE):
        save_config(cfg)
        return cfg
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    k, v = line.split("=", 1)
                    cfg[k.strip()] = v.strip()
    except Exception:
        pass
    return cfg

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        for k, v in cfg.items():
            f.write(f"{k} = {v}\n")

config = load_config()

# ------------------------
# Settings loader (animation)
# ------------------------
DEFAULT_SETTINGS = {"animation": "spinner"}

def load_settings():
    s = DEFAULT_SETTINGS.copy()
    if not os.path.exists(SETTINGS_FILE):
        save_settings(s)
        return s
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    k, v = line.split("=", 1)
                    s[k.strip()] = v.strip()
    except Exception:
        pass
    return s

def save_settings(s):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        for k, v in s.items():
            f.write(f"{k} = {v}\n")

settings = load_settings()

# ------------------------
# Theme loader
# ------------------------
def load_theme(name):
    path = os.path.join(THEME_DIR, f"{name}.json")
    if not os.path.exists(path):
        # fallback: first available theme
        try:
            first = next(f for f in os.listdir(THEME_DIR) if f.endswith(".json"))
            path = os.path.join(THEME_DIR, first)
        except StopIteration:
            return {}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}

theme = load_theme(config.get("theme", DEFAULT_CONFIG["theme"]))

# helper for color
def color(key):
    return theme.get(key, "")

RESET = "\u001b[0m"

# ------------------------
# Sound system
# ------------------------
# We will try termux-media-player first (Termux). Fallback to playsound if installed.
def play_sound_file(filename):
    if config.get("sound", "on").lower() != "on":
        return
    path = os.path.join(SOUND_DIR, filename)
    if not os.path.exists(path):
        return
    # Try termux-media-player (Termux)
    try:
        subprocess.Popen(["termux-media-player", "play", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return
    except Exception:
        pass
    # Fallback to playsound module if available
    try:
        from playsound import playsound
        playsound(path, block=False)
    except Exception:
        pass

# ------------------------
# Animations
# ------------------------
def spinner_animation(text="Loading", cycles=8, speed=0.10):
    frames = ["|", "/", "-", "\\"]
    for _ in range(cycles):
        for f in frames:
            print(f"{text} {f}", end="\r")
            time.sleep(speed)
    print(" " * 40, end="\r")

def progress_bar_animation(text="Loading", length=24, speed=0.03):
    for i in range(length + 1):
        filled = "#" * i
        empty = "-" * (length - i)
        pct = int((i / length) * 100)
        print(f"{text}: [{filled}{empty}] {pct}%", end="\r")
        time.sleep(speed)
    print()

def diagonal_animation(text="Loading", lines=8, cycles=3, speed=0.08):
    for _ in range(cycles):
        for i in range(lines):
            print("\n" * i + " " * (i*2) + "•")
            time.sleep(speed)
            clear()
    print()

def dots_animation(text="Loading", repeats=3, speed=0.4):
    for _ in range(repeats):
        for i in range(1,4):
            print(f"{text}{'.'*i}", end="\r")
            time.sleep(speed)
    print(" " * 40, end="\r")

def run_animation(kind, text="Loading"):
    if kind == "spinner":
        spinner_animation(text)
    elif kind == "progress":
        progress_bar_animation(text)
    elif kind == "diagonal":
        diagonal_animation(text)
    else:
        dots_animation(text)

# ------------------------
# Auto-detect folders (main categories)
# ------------------------
def scan_categories():
    try:
        items = [d for d in os.listdir(PY_CONTENT) if os.path.isdir(os.path.join(PY_CONTENT, d))]
    except FileNotFoundError:
        items = []
    # filter hidden/system folders and ignore list
    items = [i for i in items if i not in IGNORE_LIST and not i.startswith(".")]
    items.sort()
    return items

# ------------------------
# List files inside a folder (.py and .md)
# ------------------------
def list_folder_files(folder):
    p = os.path.join(PY_CONTENT, folder)
    try:
        files = os.listdir(p)
    except FileNotFoundError:
        return []
    # show only .py and .md
    files = [f for f in files if (f.endswith(".py") or f.endswith(".md")) and not f.startswith(".")]
    files.sort()
    return files

# ------------------------
# Run script - two modes:
#  - interactive: spawn subprocess directly (useful for interactive apps)
#  - captured : run and capture output; on error allow viewing full traceback (A+B)
# ------------------------
def run_script_interactive(script_path):
    # run with the same interpreter, interactive (no capture)
    try:
        subprocess.run([sys.executable, script_path])
    except Exception as e:
        print(color("error_color") + "[ERROR] Failed to launch interactively." + RESET)
        print(str(e))
        safe_input("Press ENTER to return...")

def run_script_captured(script_path):
    # run and capture stdout/stderr
    try:
        proc = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=None)
        out = proc.stdout
        err = proc.stderr
        if out:
            print(color("menu_text_color") + out + RESET)
        if proc.returncode != 0:
            print(color("error_color") + "[ERROR] Script finished with errors." + RESET)
            # show short summary
            err_summary = err.strip().splitlines()[-10:]
            print(color("error_color") + "\n".join(err_summary) + RESET)
            choice = safe_input("\nPress ENTER to view full output & traceback, or type 'skip' to skip: ")
            if choice.strip().lower() != "skip":
                print("\n--- FULL STDOUT ---")
                print(out)
                print("\n--- FULL STDERR ---")
                print(err)
            safe_input("\nPress ENTER to return to menu...")
        else:
            safe_input("\nProgram finished. Press ENTER to return.")
    except subprocess.SubprocessError as e:
        print(color("error_color") + "[ERROR] Running script error: " + str(e) + RESET)
        safe_input("Press ENTER to return...")

# ------------------------
# Menu UI rendering
# ------------------------
def print_header():
    clear()
    tcolor = color("title_color") or ""
    scolor = color("subtitle_color") or ""
    acolor = color("accent_color") or ""
    mcolor = color("menu_text_color") or ""
    print(tcolor + config.get("title", "") + RESET)
    print(scolor + config.get("subtitle", "") + RESET)
    print(acolor + "=" * 48 + RESET)
    print()

def category_menu():
    while True:
        print_header()
        cats = scan_categories()
        if not cats:
            print(color("error_color") + "No content found in 'Python/' folder." + RESET)
            print("Create folders under Python/ like games, scripts, tools etc.")
            safe_input("\nPress ENTER to open Python folder or Ctrl+C to quit...")
            # try auto-create
            os.makedirs(PY_CONTENT, exist_ok=True)
            continue

        print(color("menu_text_color") + "Categories:" + RESET)
        for i, c in enumerate(cats, 1):
            print(f"{color('menu_number_color')}{i:02d}{RESET} {color('menu_text_color')}{c}{RESET}")
        print()
        print(f"{color('menu_number_color')}99{RESET} {color('menu_text_color')}Settings{RESET}")
        print(f"{color('menu_number_color')}00{RESET} {color('error_color')}Exit{RESET}")

        choice = safe_input("\nEnter number: ").strip()
        play_click()
        if choice == "00":
            play_exit()
            run_animation(settings.get("animation", "spinner"), "Exiting")
            clear()
            sys.exit(0)
        if choice == "99":
            settings_menu()
            continue
        if not choice.isdigit():
            continue
        idx = int(choice) - 1
        if 0 <= idx < len(cats):
            open_category(cats[idx])

def open_category(cat):
    while True:
        print_header()
        print(color("menu_text_color") + f"[ {cat} ]" + RESET)
        files = list_folder_files(cat)
        for i, f in enumerate(files, 1):
            print(f"{color('menu_number_color')}{i:02d}{RESET} {color('menu_text_color')}{f}{RESET}")
        print()
        print(f"{color('menu_number_color')}00{RESET} {color('error_color')}Back{RESET}")

        choice = safe_input("\nEnter number: ").strip()
        play_click()
        if choice == "00":
            return
        if not choice.isdigit():
            continue
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            selected = files[idx]
            full_path = os.path.join(PY_CONTENT, cat, selected)
            # if file is markdown, show it
            if selected.endswith(".md"):
                show_markdown(full_path)
            elif selected.endswith(".py"):
                # ask how to run (interactive or captured)
                mode = safe_input("Run interactively? (y/n) [n]: ").strip().lower() or "n"
                play_open()
                run_animation(settings.get("animation", "spinner"), "Opening")
                clear()
                print(color("accent_color") + f"--- Running {selected} ---" + RESET)
                print()
                if mode == "y":
                    run_script_interactive(full_path)
                else:
                    run_script_captured(full_path)

def show_markdown(path):
    clear()
    print(color("menu_text_color") + f"---- Viewing {os.path.basename(path)} ----" + RESET)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            print(fh.read())
    except Exception as e:
        print(color("error_color") + "Failed to read file: " + str(e) + RESET)
    safe_input("\nPress ENTER to return...")

# ------------------------
# Settings menu (animations, theme, sound, title/subtitle)
# ------------------------
def settings_menu():
    while True:
        print_header()
        print(color("menu_text_color") + "Settings:" + RESET)
        print("[01] Change Title")
        print("[02] Change Subtitle")
        print("[03] Change Theme")
        print("[04] Choose Animation")
        print("[05] Toggle Sound")
        print("[06] Update README (auto-generate)")
        print("[00] Back")
        choice = safe_input("\nEnter number: ").strip()
        play_click()
        if choice == "00":
            return
        if choice == "01":
            new = safe_input("New Title: ").strip()
            if new:
                config["title"] = new
                save_config(config)
        elif choice == "02":
            new = safe_input("New Subtitle: ").strip()
            if new:
                config["subtitle"] = new
                save_config(config)
        elif choice == "03":
            choose_theme()
        elif choice == "04":
            choose_animation()
        elif choice == "05":
            toggle_sound()
        elif choice == "06":
            update_readme_auto()
            safe_input("README updated. Press ENTER...")
        else:
            continue

def choose_theme():
    themes = [t[:-5] for t in os.listdir(THEME_DIR) if t.endswith(".json")]
    while True:
        clear()
        print_header()
        print(color("menu_text_color") + "Available Themes:" + RESET)
        for i, t in enumerate(themes, 1):
            print(f"{color('menu_number_color')}{i:02d}{RESET} {color('menu_text_color')}{t}{RESET}")
        print(f"{color('menu_number_color')}00{RESET} Back")
        choice = safe_input("\nChoose theme number: ").strip()
        play_click()
        if choice == "00":
            return
        if not choice.isdigit():
            continue
        idx = int(choice) - 1
        if 0 <= idx < len(themes):
            config["theme"] = themes[idx]
            save_config(config)
            # reload theme global
            global theme
            theme = load_theme(config["theme"])
            return

def choose_animation():
    options = ["spinner", "progress", "diagonal", "dots"]
    while True:
        clear()
        print_header()
        print(color("menu_text_color") + "Animation options:" + RESET)
        for i, o in enumerate(options, 1):
            print(f"{color('menu_number_color')}{i:02d}{RESET} {color('menu_text_color')}{o}{RESET}")
        print(f"{color('menu_number_color')}00{RESET} Back")
        choice = safe_input("\nChoose animation: ").strip()
        play_click()
        if choice == "00":
            return
        if not choice.isdigit():
            continue
        idx = int(choice) - 1
        if 0 <= idx < len(options):
            settings["animation"] = options[idx]
            save_settings(settings)
            return

def toggle_sound():
    current = config.get("sound", "on")
    new = "off" if current.lower() == "on" else "on"
    config["sound"] = new
    save_config(config)

# ------------------------
# sound helpers
# ------------------------
def play_click():
    play_sound_file("click.wav")

def play_open():
    play_sound_file("open.wav")

def play_exit():
    play_sound_file("exit.wav")

# ------------------------
# README auto-update script hook
# ------------------------
def update_readme_auto():
    """
    Create README.md (root) with an index of categories and files.
    """
    try:
        readme_path = os.path.join(ROOT, "README.md")
        with open(readme_path, "w", encoding="utf-8") as fh:
            fh.write("# Python Hub (Auto-generated README)\n\n")
            fh.write("## Categories and files\n\n")
            cats = scan_categories()
            if not cats:
                fh.write("No categories found. Add folders under `Python/` (games, scripts, tools, etc.)\n")
            for c in cats:
                fh.write(f"### {c}\n\n")
                files = list_folder_files(c)
                if not files:
                    fh.write("- (empty)\n\n")
                for f in files:
                    fh.write(f"- {f}\n")
                fh.write("\n")
    except Exception as e:
        print(color("error_color") + "Failed to update README: " + str(e) + RESET)

# ------------------------
# Start program
# ------------------------
if __name__ == "__main__":
    # ensure content folder exists
    os.makedirs(PY_CONTENT, exist_ok=True)
    os.makedirs(THEME_DIR, exist_ok=True)
    os.makedirs(SOUND_DIR, exist_ok=True)
    main_loop = category_menu
    main_loop()
