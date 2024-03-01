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
                                           save_pars,
                                           get_url_pars)
from urllib.parse import urlparse
from page_analyzer.utilities.validator import validate
from page_analyzer.utilities.parser import pars_url


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index() -> render_template:
    return render_template('index.html'), 200


@app.route('/urls', methods=["POST"])
def add_url():
    url = request.form.get('url')
    url = urlparse(url)
    normalize_url = f'{url.scheme}://{url.netloc}'
    errors = validate(normalize_url)
    if errors:
        flash(*errors)
        return render_template('index.html'), 422
    is_available = get_url('urls', 'name', normalize_url)
    if is_available:
        id = is_available['id']
        flash('Страница уже существует', 'info')
        return redirect(url_for('urls_view', id=id))
    save_url(normalize_url)
    id = get_column('id', 'urls', 'name', normalize_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls_view', id=id))


@app.route('/urls/<id>')
def urls_view(id):
    url = get_url('urls', 'id', id)
    list_info = get_url_pars('url_checks', 'url_id', id)
    return render_template('urls_view.html',
                           url=url,
                           list_info=list_info)


@app.route('/urls')
def urls():
    urls = get_info_url()
    return render_template('urls.html', urls=urls), 200


@app.route('/urls/<id>/checks', methods=["POST"])
def checks(id):
    url = get_column('name', 'urls', 'id', id)
    status_code, h1, title, description = pars_url(url)
    if status_code:
        save_pars(id, status_code, h1, title, description)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('urls_view', id=id))
    flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('urls_view', id=id))


if __name__ == '__main__':
    app.run(debug=True)
