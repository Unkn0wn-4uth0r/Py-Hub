#!/usr/bin/env python3
import os
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

# === CONFIG: change only these =================================================
APP_NAME = "PY-HUB"     # <- Change this to rename the big ASCII title everywhere
VERSION = "1.0"
CREATOR = "Unkn0wn_4uth0r"   # <- change author/creator info
# ==============================================================================


def build_ascii_title(text):
    """
    Build a simple ASCII title block that uses the chosen APP_NAME.
    This keeps the banner dynamic: change APP_NAME and everything updates.
    """
    # You can replace this "block" with any ASCII forged for your APP_NAME.
    # This is a fixed art block for aesthetic; it displays the uppercase app name
    # on the banner line below the art.
    art = (
        f"{Fore.CYAN}██╗  ██╗██╗   ██╗██████╗  ██████╗ ███╗   ██╗\n"
        f"{Fore.CYAN}██║  ██║██║   ██║██╔══██╗██╔═══██╗████╗  ██║\n"
        f"{Fore.CYAN}███████║██║   ██║██████╔╝██║   ██║██╔██╗ ██║\n"
        f"{Fore.CYAN}██╔══██║██║   ██║██╔══██╗██║   ██║██║╚██╗██║\n"
        f"{Fore.CYAN}██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║ ╚████║\n"
        f"{Fore.CYAN}╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝\n"
    )
    header = f"{Fore.MAGENTA}                {text.upper()} v{VERSION}\n"
    return art + header


def banner():
    """Clear the screen and print the banner with current app name and creator."""
    os.system("clear")
    print(build_ascii_title(APP_NAME))
    print(Fore.YELLOW + f"[-] Tool Created by {CREATOR}\n")


def print_menu():
    """Displays the menu options"""
    print(Fore.RED + "[::] " + Fore.WHITE + "Select an Option For You " + Fore.RED + "[::]\n")
    print(Fore.GREEN + "[01]" + Fore.WHITE + " Games")
    print(Fore.GREEN + "[02]" + Fore.WHITE + " Scripts")
    print(Fore.GREEN + "[03]" + Fore.WHITE + " Cool Information")
    print(Fore.GREEN + "[04]" + Fore.WHITE + " View README")
    print(Fore.GREEN + "[99]" + Fore.WHITE + " About")
    print(Fore.GREEN + "[00]" + Fore.WHITE + " Exit\n")


def run_python_file(folder, filename):
    """
    Runs a python file inside the given folder.
    Explanation: using subprocess.run is safer and cleaner than os.system for
    invoking Python scripts — it inherits the terminal and exits back to menu.
    """
    os.system("clear")
    path = os.path.join(folder, filename)
    print(Fore.CYAN + f"Running {filename}...\n")
    # Use the same Python interpreter
    subprocess.run([os.sys.executable, path])
    input(Fore.YELLOW + "\nPress Enter to return to menu...")


def list_files(folder, extensions=(".py", ".md")):
    """Return a sorted list of files in folder with chosen extensions."""
    try:
        items = [f for f in sorted(os.listdir(folder)) if f.endswith(extensions)]
    except FileNotFoundError:
        items = []
    return items


def list_and_select(folder):
    """Generic handler to list .py and .md and run/show the chosen file."""
    os.system("clear")
    files = list_files(folder)
    if not files:
        print(Fore.RED + f"No files found in '{folder}'.")
        input(Fore.YELLOW + "\nPress Enter to return...")
        return

    for i, f in enumerate(files, 1):
        print(Fore.GREEN + f"[{i:02}] " + Fore.WHITE + f)
    print(Fore.RED + "[00] Back\n")
    choice = input(Fore.YELLOW + "Select: ").strip()
    if not choice.isdigit():
        print(Fore.RED + "Invalid input.")
        input(Fore.YELLOW + "Press Enter...")
        return
    idx = int(choice)
    if idx == 0:
        return
    if 1 <= idx <= len(files):
        selected = files[idx - 1]
        if selected.endswith(".py"):
            run_python_file(folder, selected)
        else:
            # show markdown or text
            os.system("clear")
            path = os.path.join(folder, selected)
            with open(path, "r", encoding="utf-8") as fh:
                print(fh.read())
            input(Fore.YELLOW + "\nPress Enter to return...")


def view_readme():
    os.system("clear")
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            print(fh.read())
    except FileNotFoundError:
        print(Fore.RED + "README.md not found.")
    input(Fore.YELLOW + "\nPress Enter to return...")


def about():
    os.system("clear")
    print(Fore.CYAN + f"📘 {APP_NAME} v{VERSION}\nCreated by {CREATOR}\n")
    print("A stylish Python Hub for organizing and running games, scripts, and notes.")
    input(Fore.YELLOW + "\nPress Enter to return...")


def main_loop():
    while True:
        banner()
        print_menu()
        choice = input(Fore.YELLOW + "[-] Select an option: ").strip()

        if choice in ("1", "01"):
            list_and_select("games")
        elif choice in ("2", "02"):
            list_and_select("scripts")
        elif choice in ("3", "03"):
            list_and_select("cool_info")
        elif choice in ("4", "04"):
            view_readme()
        elif choice in ("99",):
            about()
        elif choice in ("0", "00"):
            os.system("clear")
            print(Fore.GREEN + f"Exiting {APP_NAME}... Goodbye!\n")
            break
        else:
            print(Fore.RED + "❌ Invalid option.")
            input(Fore.YELLOW + "Press Enter...")

if __name__ == "__main__":
    main_loop()
