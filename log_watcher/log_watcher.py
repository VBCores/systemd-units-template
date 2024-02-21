#!/usr/bin/env python3
# General recommendation for log format:
# RCUTILS_CONSOLE_OUTPUT_FORMAT="{\"_\": \"{message}\", \"level\": \"{severity}\", \"timestamp\": {time}, \"loc\": \"{name}\"}"

import shutil
import psutil
import os
import subprocess

from pathlib import Path
from os.path import getctime
from datetime import datetime, timedelta

from config import config

if psutil.Process(os.getpid()).ppid() == 1:
    IS_UNDER_SYSTEMD = True
    from systemd import journal
else:
    IS_UNDER_SYSTEMD = False

    class BogusJournal:
        def send(self, msg, *args, **kwargs):
            print(msg)

    journal = BogusJournal()

DAYS_THRESHOLD = int(config["LOGS"].get("days_threshold", 3))
BOOTS_THRESHOLD = int(config["LOGS"].get("boots_threshold", 2))

LOG_DIR = Path(config["LOGS"].get("ros_logs", "/root/.ros/log"))
if not LOG_DIR.exists() or not LOG_DIR.is_dir():
    journal.send(f"Invalid path: {LOG_DIR}.")
    exit(1)
journal.send(
    f"Checking logs in {LOG_DIR}. Saving last {DAYS_THRESHOLD} days and/or {BOOTS_THRESHOLD} boots."
)

NOW = datetime.now()

jctl_call = subprocess.run(["journalctl", "--list-boots"], capture_output=True)
jctl_call.check_returncode()
jctl_output = jctl_call.stdout.decode() if jctl_call.stdout is not None else None
threshold_boot_time = NOW
if jctl_output is not None:
    jctl_lines = jctl_output.split("\n")
    boot_entry = jctl_lines[-BOOTS_THRESHOLD - 1 :][0]
    boot_parts = boot_entry.split(" ")
    boot_start_time_str = " ".join(boot_parts[3:5])
    threshold_boot_time = datetime.strptime(boot_start_time_str, "%Y-%m-%d %H:%M:%S")

threshold_days = NOW - timedelta(days=DAYS_THRESHOLD)

journal.send(
    f"Found thresholds: boot - <{threshold_boot_time.strftime('%c')}>, days - <{threshold_days.strftime('%c')}>"
)
threshold = min(threshold_days, threshold_boot_time)
journal.send(f"Using threshold - <{threshold.strftime('%c')}>.")

dirs = [d for d in LOG_DIR.iterdir() if d.is_dir()]

for log_dir in dirs:
    if datetime.fromtimestamp(getctime(log_dir)) >= threshold:
        continue
    journal.send(f"Deleting {log_dir}")
    shutil.rmtree(log_dir)
