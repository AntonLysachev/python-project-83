from flask import (Flask,
                   render_template,
                   request, flash,
                   redirect,
                   url_for,
                   get_flashed_messages)
import os
from dotenv import load_dotenv
from page_analyzer.CRUD.crud_utils import (save_url,
                                           get_column,
                                           get_url,
                                           get_info_url,
                                           save_check,
                                           get_url_check)
from datetime import date
from page_analyzer.utilities.validator import validate
from page_analyzer.utilities.checker import check


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index() -> render_template:
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages), 200


@app.route('/urls', methods=["POST"])
def add_url():
    today = date.today()
    url = request.form.get('url')
    errors = validate(url)
    if errors:
        flash(*errors)
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 422
    is_available = get_url('urls', 'name', url)
    if is_available:
        id = is_available['id']
        flash('Страница уже существует', 'info')
        return redirect(url_for('urls_view', id=id))
    save_url(url, today)
    id = get_column('id', 'urls', 'name', url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls_view', id=id))


@app.route('/urls/<id>')
def urls_view(id):
    messages = get_flashed_messages(with_categories=True)
    url = get_url('urls', 'id', id)
    list_info = get_url_check('url_checks', 'url_id', id)
    return render_template('urls_view.html',
                           messages=messages,
                           url=url,
                           list_info=list_info)


@app.route('/urls')
def urls():
    urls = get_info_url()
    return render_template('urls.html', urls=urls), 200


@app.route('/urls/<id>/checks', methods=["POST"])
def checks(id):
    today = date.today()
    url = get_column('name', 'urls', 'id', id)
    status_code, h1, title, description = check(url)
    if status_code:
        save_check(id, status_code, h1, title, description, today)
        return redirect(url_for('urls_view', id=id))
    flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('urls_view', id=id))


if __name__ == '__main__':
    app.run(debug=True)
