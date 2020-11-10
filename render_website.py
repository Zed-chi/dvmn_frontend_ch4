import json
import os
from urllib.parse import quote


from jinja2 import Environment, FileSystemLoader, select_autoescape

from livereload import Server

from more_itertools import chunked


JSON_PATH = os.path.join("./", "books.json")
HTML_DIR = os.path.join("./", "pages")


def get_books_description_from_json(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        data = file.read()
        return json.loads(data)


def normalize_data_path(books):
    for book in books:
        book["img_src"] = quote(
            book["img_src"].replace("\\", "/").replace(".", "..", 1))
        book["book_path"] = quote(
            book["book_path"].replace("\\", "/").replace(".", "..", 1))


def on_reload():
    description = get_books_description_from_json(JSON_PATH)
    books_list = description["books"]
    normalize_data_path(books_list)
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("template.html")
    chunks_by_10 = [*chunked(description["books"], 10, strict=False)]
    pages_count = len(chunks_by_10)

    for id, chunk in enumerate(chunks_by_10):
        rendered_page = template.render(
            books=[*chunked(chunk, 2)],
            pages_count=pages_count,
            current_page=id + 1,
        )
        path = os.path.join(HTML_DIR, f"index{id+1}.html")
        with open(path, "w", encoding="utf8") as file:
            file.write(rendered_page)


on_reload()
server = Server()
server.watch("./template.html", on_reload)
server.serve(root="./")
