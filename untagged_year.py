#!/bin/env python3
# Make a webpage showing all the untagged files in the Synology Photos shared space.
# (c) Cormac McGaughey, 2025

import collections
import subprocess
import datetime
import sys

# Validate command line.
if len(sys.argv) != 4:
    print("Usage: python untagged_year.py input.txt output.html URL")
    sys.exit(1)

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
URL = sys.argv[3]

# Read and group entries by date
entries_by_date = collections.OrderedDict()

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        date, photo_id, folder, filename = line.split("|", 3)
        entries_by_date.setdefault(date, []).append({
            "id": photo_id,
            "folder": folder,
            "filename": filename
        })

def id_link(photo_id):
    return f'<a href="https://{URL}/#/shared_space/timeline/item/{photo_id}" target="_blank">{photo_id}</a>'

# HTML template parts

# Get the current date and time
now = datetime.datetime.now()

# Create a datetime object representing the current date and time

# Display a message indicating what is being printed
#print("Current date and time : ")

# Print the current date and time in a specific format
updated_time=now.strftime("%Y-%m-%d %H:%M:%S")

html_head = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Untagged Photos by Date</title>
<style>
body { font-family: sans-serif; }
details { margin-bottom: 1.2em; }
summary { font-weight: bold; font-size: 1.1em; cursor: pointer; }
ul { margin: 0.3em 0 0.7em 1.4em; }
li { margin-bottom: 0.3em; }
</style>
</head>
<body>
<h1>Untagged Photos by Date</h1>
"""

html_tail = """
</body>
</html>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write(html_head)
    out.write(f'<h3><b><i>Last updated: {updated_time}</i></b></h3>')
    for date, entries in entries_by_date.items():
        out.write(f'<details>\n<summary>{date} ({len(entries)} items)</summary>\n<ul>\n')
        for entry in entries:
            out.write(
                f'<li>{id_link(entry["id"])} | <code>{entry["folder"]}</code> | <b>{entry["filename"]}</b></li>\n'
            )
        out.write('</ul>\n</details>\n')
    out.write(html_tail)

print(f"Done. HTML written to {OUTPUT_FILE}")
