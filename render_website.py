from os import replace
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler
from livereload import Server, shell
from more_itertools import chunked
import json
import os
from urllib.parse import quote

JSON_PATH = os.path.join("./", "books.json")


def get_books_description(path):
    with open(path, "r", encoding="utf-8") as file:
        data = file.read()
        return json.loads(data)


def normalize_data_path(books):
    for book in books:
        book["img_src"] = quote(book["img_src"].replace("\\", "/"))
        book["book_path"] = quote(book["book_path"].replace("\\", "/"))


def on_reload():
    description = get_books_description(JSON_PATH)
    books = description["books"]
    normalize_data_path(books)
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("template.html")
    rendered_page = template.render(books=[*chunked(description["books"], 2)])

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)


on_reload()
server = Server()
server.watch("./template.html", on_reload)
server.serve(root="./")
