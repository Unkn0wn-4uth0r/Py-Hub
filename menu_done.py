import os
import json
import time
import pyfiglet

# ============================
# Load Configuration
# ============================
def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def load_themes():
    with open("themes.json", "r") as f:
        return json.load(f)

config = load_config()
themes = load_themes()

theme = themes[config["default_theme"]]

TITLE_COLOR = theme["title"]
SUB_COLOR = theme["subtitle"]
CREATOR_COLOR = theme["creator"]
NUM_COLOR = theme["menu_number"]
TEXT_COLOR = theme["menu_text"]
HEADER_COLOR = theme["header"]
RESET = theme["reset"]

ANIM_SPEED = config["animation_speed"]

# ============================
# Utility Functions
# ============================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def loading(text="Loading"):
    clear()
    for i in range(3):
        print(f"{TEXT_COLOR}{text}{'.' * (i+1)}{RESET}")
        time.sleep(ANIM_SPEED)
        clear()

# ============================
# Title Rendering
# ============================
def render_title():
    ascii_banner = pyfiglet.figlet_format(config["main_title"], font="ansi_shadow")
    print(TITLE_COLOR + ascii_banner + RESET)
    print(SUB_COLOR + config["subtitle"] + RESET)
    print(CREATOR_COLOR + config["creator"] + RESET + "\n")

# ============================
# Auto Detect Categories
# ============================
def get_categories():
    base_path = "Python"
    items = []

    for item in os.listdir(base_path):
        full = os.path.join(base_path, item)
        if os.path.isdir(full):
            items.append(item)

    return sorted(items)

# ============================
# Auto Detect Scripts in Category
# ============================
def get_scripts(category):
    path = os.path.join("Python", category)
    scripts = []

    for f in os.listdir(path):
        if f.endswith(".py"):
            scripts.append(f)

    return sorted(scripts)

# ============================
# Execute a Script
# ============================
def run_script(category, script):
    loading("Running")
    os.system(f"python Python/{category}/{script}")
    input("\nPress ENTER to return to the menu...")

# ============================
# README Viewer
# ============================
def view_readme():
    loading("Opening README")
    os.system("clear")
    with open("README.md", "r") as f:
        print(f.read())
    input("\nPress ENTER to return to the menu...")

# ============================
# About Section
# ============================
def about():
    clear()
    print(HEADER_COLOR + "ABOUT PY-HUB" + RESET)
    print(TEXT_COLOR + "A modular Python-based launcher hub." + RESET)
    print(f"{TEXT_COLOR}Version: 1.0{RESET}")
    print(f"{CREATOR_COLOR}{config['creator']}{RESET}")
    input("\nPress ENTER to return to the menu...")

# ============================
# Main Menu
# ============================
def main():
    while True:
        clear()
        render_title()

        categories = get_categories()

        print(HEADER_COLOR + "[::] Select an option [::]" + RESET)
        print()

        for i, cat in enumerate(categories, start=1):
            print(f"{NUM_COLOR}[{i:02d}]{RESET} {TEXT_COLOR}{cat.capitalize()}{RESET}")

        print(f"\n{NUM_COLOR}[98]{RESET} View README")
        print(f"{NUM_COLOR}[99]{RESET} About")
        print(f"{NUM_COLOR}[00]{RESET} Exit\n")

        choice = input(NUM_COLOR + "[-] Select an option: " + RESET)

        if choice == "00":
            loading("Exiting")
            clear()
            print(TEXT_COLOR + "Goodbye!" + RESET)
            break

        elif choice == "98":
            view_readme()

        elif choice == "99":
            about()

        else:
            try:
                idx = int(choice) - 1
                category = categories[idx]
            except:
                continue

            scripts = get_scripts(category)
            clear()
            render_title()

            print(HEADER_COLOR + f"{category.capitalize()} Scripts:" + RESET)

            for i, script in enumerate(scripts, start=1):
                print(f"{NUM_COLOR}[{i:02d}]{RESET} {TEXT_COLOR}{script}{RESET}")

            print(f"{NUM_COLOR}[00]{RESET} Back\n")

            sub_choice = input(NUM_COLOR + "Select a script: " + RESET)

            if sub_choice == "00":
                continue

            try:
                script_idx = int(sub_choice) - 1
                run_script(category, scripts[script_idx])
            except:
                pass


if __name__ == "__main__":
    main()
