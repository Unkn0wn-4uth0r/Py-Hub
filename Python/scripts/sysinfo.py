import platform, os, psutil, sys
print("=== System Info ===")
print("OS:", platform.system(), platform.release())
print("Platform:", platform.platform())
print("Python:", platform.python_version())
try:
    import psutil
    print("CPU cores:", psutil.cpu_count())
    print("Memory total (GB):", round(psutil.virtual_memory().total / 1e9, 2))
except Exception:
    print("psutil not installed (install with pip install psutil for more info).")

