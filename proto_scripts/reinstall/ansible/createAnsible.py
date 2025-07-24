import os
import re
import json
from collections import defaultdict
from datetime import datetime

LOG_FILE = "/var/log/pkg_install_tracker/installations.log"

# Parse ISO 8601 datetime
parse_ts = lambda ts: datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")

# Load log lines
entries = []
with open(LOG_FILE) as f:
    for line in f:
        try:
            entry = json.loads(line)
            entry["parsed_time"] = parse_ts(entry["timestamp"])
            entries.append(entry)
        except Exception:
            continue

# Collect events per package
package_events = defaultdict(list)

for entry in entries:
    mgr = entry["manager"]
    cmd = entry["command"]
    ts = entry["parsed_time"]

    # Detect install/remove
    action = None
    if re.search(r"\binstall\b", cmd):
        action = "install"
    elif re.search(r"\b(remove|uninstall)\b", cmd):
        action = "remove"
    else:
        continue

    # Extract package names
    if mgr == "APT":
        match = re.findall(r"apt(?:-get)?\s+(?:install|remove)\s+(-y\s+)?([\w\-\.]+)", cmd)
        pkgs = [m[1] for m in match]
    elif mgr == "PIP":
        match = re.findall(r"pip(?:3)?\s+(?:install|uninstall)\s+([\w\-\.]+)", cmd)
        pkgs = match
    elif mgr == "CARGO":
        match = re.findall(r"cargo\s+(?:install|uninstall)\s+([\w\-\.]+)", cmd)
        pkgs = match
    elif mgr == "FLATPAK":
        match = re.findall(r"flatpak\s+(?:install|remove)\s+.*?([\w\.]+/[\w\.]+)", cmd)
        pkgs = match
    else:
        continue

    for pkg in pkgs:
        package_events[pkg].append((ts, action, mgr, cmd))

# Determine final installs
final_installs = []

for pkg, events in package_events.items():
    events.sort()  # by timestamp
    active = False
    last_install = None
    for ts, action, mgr, cmd in events:
        if action == "install":
            last_install = (ts, mgr, cmd)
            active = True
        elif action == "remove" and active:
            # Removed after install
            last_install = None
            active = False

    if last_install:
        final_installs.append((*last_install, pkg))

# Sort installs by original timestamp
final_installs.sort()

# Generate playbook
playbook = [
    {"name": f"Install {pkg}",
     "become": True,
     "ansible.builtin.shell": cmd}
    for ts, mgr, cmd, pkg in final_installs
]

with open("playbook.yml", "w") as f:
    f.write("- hosts: all\n  tasks:\n")
    for task in playbook:
        f.write(f"  - name: {task['name']}\n")
        f.write(f"    become: {str(task['become']).lower()}\n")
        f.write(f"    ansible.builtin.shell: {task['ansible.builtin.shell']}\n")
