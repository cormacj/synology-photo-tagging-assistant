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
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Untagged Photos by Date</title>
<style>
body {
    font-family: sans-serif;
    margin: 0;
    padding: 1em;
    background: #fafbfc;
    color: #222;
    max-width: 700px;
    /*margin-left: auto;
    margin-right: auto;*/
}
h1 {
    font-size: 1.7em;
    margin-bottom: 1em;
}
details {
    margin-bottom: 1.2em;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    padding: 0.7em 1em;
}
summary {
    font-weight: bold;
    font-size: 1.1em;
    cursor: pointer;
    padding: 0.6em 0;
    outline: none;
    border-radius: 4px;
    transition: background 0.2s;
}
summary:focus, summary:hover {
    background: #f0f4f8;
}
ul {
    margin: 0.3em 0 0.7em 1.4em;
    padding-left: 1.2em;
}
li {
    margin-bottom: 0.3em;
    word-break: break-word;
}
@media (max-width: 600px) {
    body {
        font-size: 1.05em;
        padding: 0.7em 0.3em;
    }
    h1 {
        font-size: 1.2em;
    }
    details {
        padding: 0.5em 0.5em;
    }
    ul {
        margin-left: 0.7em;
        padding-left: 0.7em;
    }
    summary {
        font-size: 1em;
        padding: 0.8em 0.2em;
    }
}
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
