import json
from os.path import relpath

from bs4 import BeautifulSoup as bs
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import markdown
from invoke import task
from pprint import pprint
from functools import cache
from slugify import slugify
import datetime

from typing import NamedTuple


class PostData(NamedTuple):
    title: str
    date: datetime.date
    content: str
    filename: str


@task
def newpost(c, title: str):
    newpost_template_lines = [
        r'{% extends "base.html" %}',
        r"{% block title %}" + title + "{% endblock %}",
        r"{% block date %}" + datetime.date.today().isoformat() + r"{% endblock %}",
        r"{% block content %}",
        r"<p>\n</p>",
        r"{% endblock content %}",
    ]

    title_filename = f"{slugify(title.strip(), allow_unicode=False)}.md"

    new_filepath = find_root().joinpath("posts-raw", title_filename)

    assert not new_filepath.exists()

    with open(new_filepath, "w") as outfile:
        outfile.writelines([line + "\n" for line in newpost_template_lines])


@cache
def find_root():
    current_dir = Path(".").expanduser().resolve()

    def home_or_root(path: Path):
        path = path.resolve().absolute()
        if path == path.home():
            return True
        if path == path.root:
            return True
        return False

    while not home_or_root(current_dir):
        if current_dir.joinpath(".git").exists():
            return current_dir.resolve().absolute()
        current_dir = current_dir.joinpath("..")

    raise FileNotFoundError


@cache
def _post_location():
    p = find_root().joinpath("posts").resolve()
    print(p)

    rel = Path(relpath(p, find_root())).resolve().absolute()
    return rel


@task
def quote(c):
    with open("quotes.txt", "r") as infile:
        lines = [
            line.strip()
            for line in infile.readlines()
            if not line or not line.isspace()
        ]

    with open("quotes.json", "w") as outfile:
        json.dump({"quotes": lines}, outfile, indent=4)


def get_meta(content: str):
    content_lines = content.strip().split("\n")
    return (content_lines[1], content_lines[2])


def make_index(posts: list[PostData]):
    posts.sort(key=lambda x: x.date)

    templates_path = find_root().joinpath("templates")
    environment = Environment(
        loader=FileSystemLoader([find_root().as_posix(), templates_path])
    )

    index_template = environment.get_template("posts_index_template.html")
    index_content = strip_html(index_template.render(posts_index=posts).strip())

    with open(find_root().joinpath("posts", "index.html"), "w") as outfile:
        outfile.write(index_content)


def strip_html(html: str):
    lines = html.split("\n")
    return "\n".join([line for line in lines if line])


@task
def convert(c):
    post_raw_path = find_root().joinpath("posts-raw")
    post_html_path = find_root().joinpath("posts")

    templates_path = find_root().joinpath("templates")

    if not post_html_path.exists():
        post_html_path.mkdir()

    environment = Environment(
        loader=FileSystemLoader([post_raw_path, find_root().as_posix(), templates_path])
    )

    processed = []

    for raw_md in post_raw_path.glob("*.md"):
        if not raw_md.is_file:
            continue
        template = environment.get_template(raw_md.name)
        filled  = template.render(rootpath=relpath(find_root(), start=post_html_path))

        filled = strip_html(filled)
        filename = f"{raw_md.stem}.html"
        title, date_str = get_meta(filled)

        post_date = datetime.date.fromisoformat(date_str.strip())

        processed.append(
            PostData(title=title, content=filled, date=post_date, filename=filename)
        )

    for post in processed:
        with open(post_html_path.joinpath(post.filename), "w") as outfile:
            outfile.write(post.content.strip())

    make_index(processed)

    index_template = environment.get_template("main_index_template.html")
    main_index_content = strip_html(index_template.render(rootpath="."))

    with open(find_root().joinpath("index.html"), "w") as index_file:
        index_file.write(main_index_content)
