import os
path = input("Enter folder to clean (or leave blank for current): ").strip() or "."
deleted = 0
for f in os.listdir(path):
    if f.endswith((".log", ".tmp")):
        try:
            os.remove(os.path.join(path, f))
            deleted += 1
        except Exception:
            pass
print("Deleted", deleted, "temp files.")
