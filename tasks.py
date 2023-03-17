import json
import os
from os.path import relpath

from bs4 import BeautifulSoup as bs

from pathlib import Path
import markdown
from invoke import task
from pprint import pprint
from functools import cache


def _get_html_components(html_text: str):
    soup = bs(html_text, "html.parser")

    body_tag = soup.body
    if body_tag is None:
        body_tag = soup

    body = "\n".join(str(txt) for txt in body_tag.contents)

    title = soup.find("title")

    if title is not None:
        title = title.text.strip()
    elif (h1 := soup.find("h1")) is not None:
        title = h1.text.strip()
    else:
        title = ""

    return (title, body)


@cache
def _find_root():
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
    p = _find_root().joinpath('posts').resolve()
    print(p)

    rel =  Path(relpath(p, _find_root())).resolve().absolute()
    print(rel)

def _format_page_content(page_title: str, page_content: str):



    html_boilerplate_header = rf"""
    <!DOCTYPE html>
    <html lang = "en">
      <head>
        <meta charset="utf-8">
        <title>{page_title}</title>
        <link rel="stylesheet" href="../et-book/et-book.css">
        <link rel="stylesheet" href="../css/index-page-base.css">
        <link rel="stylesheet" href="../css/tufte.css">

        <meta name="viewport" content="width=device-width, initial-scale=1">
      </head>
  """.strip()

    html_boilerplate_body = (
        rf"""
      <body>
        <h1><a href = "https://keagud.github.io">keagud dot github dot io</a></h1>
        <p><i id="quote"></i></p>
        <br>

        """
        + page_content
        + r"""
        <script>
          const quotesJson = (()=>{
            let reader = new XMLHttpRequest();
            reader.open("GET", """
        + '"../quotes.json"'
        + """, false);
            reader.send();
            return JSON.parse(reader.responseText);
          })();

          console.log(quotesJson);

      const quoteElement = document.querySelector("#quote");

      quoteElement.textContent = (() => {

      const quotesArr = quotesJson["quotes"];

      console.table(quotesArr);
      let index = Math.floor(Math.random() * (quotesArr.length));
      console.log(quotesArr[index]);
      return quotesArr[index];

    })();
        </script>
         </body>
    </html>
    """
    )

    return "\n".join((html_boilerplate_header, html_boilerplate_body))


@task
def quote(c):
    with open("quotes.txt", "r") as infile:
        lines = [line.strip() for line in infile.readlines() if not line or not line.isspace()]

    with open("quotes.json", "w") as outfile:
        json.dump({"quotes": lines}, outfile, indent=4 )


def _post(input_filename: str, replace: bool = False, pretty: bool = True):
    input_filename = os.path.normpath(input_filename)
    with open(input_filename, "r") as infile:
        md_content = "\n".join([line.strip() for line in infile.readlines()])

    html_content = markdown.markdown(md_content)

    pprint(html_content)

    components = _get_html_components(html_content)

    full_html = _format_page_content(*components )

    if pretty:
        soup = bs(full_html, features="html.parser")
        full_html = soup.prettify(formatter="html")

    base_name, _ = os.path.splitext(os.path.basename(input_filename))

    target_name = f"./posts/{base_name}.html"

    if os.path.exists(target_name) and not replace:
        raise FileExistsError

    print(full_html)

    with open(target_name, "w") as post_file:
        post_file.write(full_html)


def _make_index_html(target_dir: str | None = None):

    if target_dir is None:
        target_dir = _find_root().joinpath("posts").as_posix()

    index_items = []

    for file in Path(target_dir).glob("*.html"):
        if file.name == "index.html":
            continue

        with open(file, "r") as post_file:
            soup = bs(post_file.read(), "html.parser")

        post_title = soup.find("title")

        if post_title is None:
            continue

        post_title = post_title.text.strip()

        index_items.append((post_title, file.name))
    pprint(index_items)

    links_list = "\n".join(
        [f'<li><a href = "./{link}">{title}</a></li>' for title, link in index_items]
    )

    return _format_page_content("Posts", rf"<ul>{links_list}</ul>" )


@task
def post(c, input_filename: str, replace: bool = True, pretty: bool = True):
    _post(input_filename, replace=replace, pretty=pretty)


@task
def postall(c, target_dir: str = "./posts-md", replace: bool = False):
    for file in Path(target_dir).glob("*.md"):
        _post(file.as_posix(), replace=replace)


@task
def index(c):
    target_file = _find_root().joinpath("./posts/index.html").as_posix()

    index_text = _make_index_html()

    with open(target_file, "w") as index_file:
        index_file.write(index_text)


@task
def clean(c):
    post_path = _find_root().joinpath("posts")

    for file in post_path.glob("*.html"):
        if file.name ==  "index.html" or file.is_dir():
            continue
        file.unlink(missing_ok=True)






