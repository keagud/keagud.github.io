import json
import os

from bs4 import BeautifulSoup as bs

import markdown
from invoke import task


@task
def quote(c):
    with open("quotes.txt", "r") as infile:
        lines = [l.strip() for l in infile.readlines()]

    with open("quotes.json", "w") as outfile:
        json.dump({"quotes": lines}, outfile, indent=4)

#TODO programmatically generate table of contents from post directory contents
@task
def post(c, input_filename: str, replace: bool = False, pretty: bool = True):
    input_filename = os.path.normpath(input_filename)
    with open(input_filename, "r") as infile:
        md_content = infile.read()

    post_lines = [l for l in md_content.splitlines() if not l.isspace()]
    post_title = post_lines[0].strip("#")

    html_content = markdown.markdown(md_content)

    full_html = rf"""
    “<!DOCTYPE html>
    <head> 
        <meta charset="utf-8"/>
        <title>{post_title.title()}</title>
        <link rel="stylesheet" href="../css/tufte.css">
        <link rel="stylesheet" href="../css/layout.css">
        <link rel="stylesheet" href = "../et-book">
        
    </head>

    <body>

    <div class = "home-button">
        <p>
        <a href = "../index.html">
            home
        </a>
        <h1>
    <p>

        {html_content}

    </body>

    """

    if pretty:
        soup = bs(full_html, features="html.parser")
        full_html = soup.prettify()

    base_name, _ = os.path.splitext(os.path.basename(input_filename))

    target_name = f"./posts/{base_name}.html"

    if os.path.exists(target_name) and not replace:
        raise FileExistsError

    with open(target_name, "w") as post_file:
        post_file.write(full_html)
