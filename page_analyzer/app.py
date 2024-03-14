from flask import Flask, render_template, request, flash, redirect, url_for
import os
import requests
from dotenv import load_dotenv
from page_analyzer.db import (
    save_url,
    get_url_by_id,
    get_url_by_name,
    get_urls_with_last_check,
    save_info_url,
    get_url,
)
from page_analyzer.urls import validate_url, normalize_url
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
    errors = validate_url(url)
    if errors:
        for error in errors:
            flash(*error)
        return render_template("index.html"), 422
    url = normalize_url(url)
    is_exists = get_url_by_name(url)
    if is_exists:
        id = is_exists["id"]
        flash("Страница уже существует", "info")
        return redirect(url_for("urls_view", id=id))
    id = save_url(url)
    flash("Страница успешно добавлена", "success")
    return redirect(url_for("urls_view", id=id))


@app.route("/urls/<id>")
def urls_view(id):
    url = get_url_by_id(id)
    list_info = get_url(id)
    return render_template("urls_view.html", url=url, list_info=list_info)


@app.route("/urls")
def urls():
    urls = get_urls_with_last_check()
    return render_template("urls.html", urls=urls), 200


@app.route("/urls/<id>/checks", methods=["POST"])
def checks(id):
    url = get_url_by_id(id)["name"]
    response = requests.get(url)
    response.raise_for_status()
    if response:
        status_code, h1, title, description = get_info_site(response)
        save_info_url(id, status_code, h1, title, description)
        flash("Страница успешно проверена", "success")
        return redirect(url_for("urls_view", id=id))
    flash("Произошла ошибка при проверке", "danger")
    return redirect(url_for("urls_view", id=id))


if __name__ == "__main__":
    app.run(debug=DEBUG_SWITCH)
