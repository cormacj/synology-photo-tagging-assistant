#!/bin/env python3
# Make a webpage listing all the synology tags, and it's searchable.
# (c) Cormac McGaughey, 2025

import csv
import sys
import datetime
from pathlib import Path
from html import escape


def read_data(filename):
    # Reads a pipe-delimited file into a list of tuples (number, name)
    data = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "|" not in line:
                continue
            number, name = line.split("|", 1)
            number = number.strip()
            name = name.strip()
            if number and name:
                data.append((number, name))
    return data

def generate_html(data, output_filename):
    # First the static header stuff that defines the look, adds the last run time, and the link to untagged files.
    #
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Photo Tag Links</title>
    <style>
        body {{ font-family: sans-serif; margin: 2em; }}
        #searchbox {{ padding: 0.5em; width: 300px; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin: 0.3em 0; }}
        a {{ text-decoration: none; color: #2a52be; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>Photo Tag Links</h1>
    Last run: {lastrun}
    <h3><a href="untagged_photos.html">Click Here for Untagged Photos</a></h3
<br>
<br>
Enter part of a tag to search for something.
<p/ >
    <input type="text" id="searchbox" placeholder="Search tags..." onkeyup="filterList()">
    <ul id="taglist">
"""
    # Now, covert the database output into links.
    for number, name in data:
        url = f"https://{URL}/?launchApp=SYNO.Foto.AppInstance#/general_tag/shared_space/{escape(number)}"
        html += f'        <li><a href="{url}" target="_blank">{escape(name)}</a></li>\n'
    #Finally, add the function to filter the list
    html += """    </ul>
    <script>
        function filterList() {
            var input = document.getElementById('searchbox');
            var filter = input.value.toLowerCase();
            var ul = document.getElementById("taglist");
            var li = ul.getElementsByTagName('li');
            for (var i = 0; i < li.length; i++) {
                var a = li[i].getElementsByTagName("a")[0];
                var txtValue = a.textContent || a.innerText;
                li[i].style.display = txtValue.toLowerCase().includes(filter) ? "" : "none";
            }
        }
    </script>
</body>
</html>
"""

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html)
    #print(f"HTML page written to {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python generate_links.py input.txt output.html url")
        sys.exit(1)
    now = datetime.datetime.now()
    lastrun=f'{now.strftime("%d-%h-%Y %H:%M:%S")}'
    URL = sys.argv[3]
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    data = read_data(input_file)
    generate_html(data, output_file)
