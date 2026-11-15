#!/usr/bin/env python3
"""DailyCarry scans every hour while its seat is empty. Restores the file if the line does not match."""
import os
import shutil
import py_compile

TARGET = "main.py"
BACKUP = "main.py.bak_hour"

OLD = "    DAILY_CARRY_INTERVAL_HOURS = 24.0\n"
NEW = "    DAILY_CARRY_INTERVAL_HOURS = 1.0\n"


def main():
    if not os.path.exists(TARGET):
        print(f"STOPPED missing {TARGET}")
        return
    shutil.copy2(TARGET, BACKUP)
    text = open(TARGET, encoding="utf-8").read()
    n = text.count(OLD)
    if n != 1:
        shutil.copy2(BACKUP, TARGET)
        print(f"STOPPED interval count={n}")
        print(f"restored from {BACKUP} — bot file was not changed")
        return
    text = text.replace(OLD, NEW, 1)
    open(TARGET, "w", encoding="utf-8").write(text)
    try:
        py_compile.compile(TARGET, doraise=True)
    except Exception as e:
        shutil.copy2(BACKUP, TARGET)
        print(f"STOPPED compile: {e}")
        print(f"restored from {BACKUP} — bot file was not changed")
        return
    print("DONE interval=1h")
    print(f"backup={BACKUP}")


if __name__ == "__main__":
    main()
