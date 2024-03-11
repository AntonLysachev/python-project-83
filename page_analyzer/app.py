from flask import Flask, render_template, request, flash, redirect, url_for
import os
from dotenv import load_dotenv
from page_analyzer.db import (
    save_url,
    get_url,
    get_info_url,
    save_info_url,
    get_url_list,
)
from urllib.parse import urlparse
from page_analyzer.validator import address
import requests
from page_analyzer.html_content import get_info_site


load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
DEBUG_SWITCH = os.getenv("DEBUG_SWITCH")


@app.route("/")
def index() -> render_template:
    return render_template("index.html"), 200


@app.route("/urls", methods=["POST"])
def add_url():
    url = request.form.get("url")
    errors = address(url)
    if errors:
        for error in errors:
            flash(*error)
        return render_template("index.html"), 422
    url = urlparse(url)
    normalize_url = f"{url.scheme}://{url.netloc}"
    is_exists = get_url("name", normalize_url)
    if is_exists:
        id = is_exists["id"]
        flash("Страница уже существует", "info")
        return redirect(url_for("urls_view", id=id))
    id = save_url(normalize_url)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("urls_view", id=id))


@app.route("/urls/<id>")
def urls_view(id):
    url = get_url("id", id)
    list_info = get_url_list(id)
    return render_template("urls_view.html", url=url, list_info=list_info)


@app.route("/urls")
def urls():
    urls = get_info_url()
    return render_template("urls.html", urls=urls), 200


@app.route("/urls/<id>/checks", methods=["POST"])
def checks(id):
    url = get_url("id", id)["name"]
    html = requests.get(url)
    if html:
        status_code, h1, title, description = get_info_site(html)
        save_info_url(id, status_code, h1, title, description)
        flash("Страница успешно проверена", "success")
        return redirect(url_for("urls_view", id=id))
    flash("Произошла ошибка при проверке", "danger")
    return redirect(url_for("urls_view", id=id))


if __name__ == "__main__":
    app.run(debug=DEBUG_SWITCH)
