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
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Photo Tag Links</title>
    <style>
        body {{
            font-family: sans-serif;
            margin: 0;
            padding: 1em;
            background: #fafbfc;
            color: #222;
            max-width: 700px;
            /*margin-left: auto;
            margin-right: auto;*/
        }}
        #searchbox {{
            padding: 0.7em;
            width: 100%;
            max-width: 400px;
            font-size: 1em;
            box-sizing: border-box;
            margin-bottom: 1em;
        }}
        ul {{
            list-style: none;
            padding: 0;
        }}
        li {{
            margin: 0.5em 0;
        }}
        a {{
            text-decoration: none;
            color: #2a52be;
            font-size: 1.05em;
            padding: 0.4em 0.8em;
            border-radius: 6px;
            transition: background 0.2s;
            display: inline-block;
        }}
        a:hover, a:focus {{
            text-decoration: underline;
            background: #f0f4f8;
        }}
        h1 {{
            font-size: 1.6em;
        }}
        h3 {{
            margin-top: 1em;
            margin-bottom: 0.5em;
        }}
        @media (max-width: 600px) {{
            body {{
                font-size: 1.08em;
                padding: 0.5em 0.3em;
            }}
            #searchbox {{
                font-size: 1em;
                width: 100%;
                max-width: none;
            }}
            h1 {{
                font-size: 1.2em;
            }}
        }}
    </style>
</head>
<body>
    <h1>Photo Tag Links</h1>
    Last run: {lastrun}
    <h3><a href="untagged_photos.html">Click Here for Untagged Photos</a></h3>
    <br>
    <br>
    <label for="searchbox">Enter part of a tag to search for something.</label>
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
