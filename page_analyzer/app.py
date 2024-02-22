from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
import os
from dotenv import load_dotenv
from page_analyzer.CRUD.crud_utils import save, get_column, get_url, to_dict_table
from datetime import date
from page_analyzer.validation.validator import validate
from page_analyzer.constants import INSERT_URL_TABLE
from urllib.request import urlopen 

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index() -> render_template:
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.route('/urls', methods=["POST"])
def add_url():
    today = date.today()
    url = request.form.get('url')
    errors = validate(url)
    if errors:
        flash(*errors)
        return redirect(url_for('index'))
    is_available = get_url('urls', 'name', url)
    if is_available:
        id = is_available['id']
        flash('Страница уже существует', 'info')
        return redirect(url_for('urls_view', id=id))
    save(INSERT_URL_TABLE, url, today)
    id = get_column('id', 'urls', 'name', url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls_view', id=id))


@app.route('/urls/<id>')
def urls_view(id):
    messages = get_flashed_messages(with_categories=True)
    url = get_url('urls', 'id', id)
    return render_template('urls_view.html', messages=messages, url=url)


@app.route('/urls')
def urls():
    urls = to_dict_table('urls')
    return render_template('urls.html', urls=urls)


if __name__ == '__main__':
    app.run(debug=True)
