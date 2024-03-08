from flask import (Flask,
                   render_template,
                   request, flash,
                   redirect,
                   url_for)
import os
from dotenv import load_dotenv
from page_analyzer.CRUD.crud_utils import (save_url,
                                           get_column,
                                           get_url,
                                           get_info_url,
                                           save_info_url,
                                           get_url_list)
from urllib.parse import urlparse
from page_analyzer.utilities.validator import validate
from page_analyzer.utilities.html_content import html_content, get_content


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DEBUG_SWITCH = os.getenv('DEBUG_SWITCH')


@app.route('/')
def index() -> render_template:
    return render_template('index.html'), 200


@app.route('/urls', methods=["POST"])
def add_url():
    url = request.form.get('url')
    errors = validate(url)
    if errors:
        for error in errors:
            flash(*error)
        return render_template('index.html'), 422
    url = urlparse(url)
    normalize_url = f'{url.scheme}://{url.netloc}'
    is_exists = get_url('name', normalize_url)
    if is_exists:
        id = is_exists['id']
        flash('Страница уже существует', 'info')
        return redirect(url_for('urls_view', id=id))
    id = save_url(normalize_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('urls_view', id=id))


@app.route('/urls/<id>')
def urls_view(id):
    url = get_url('id', id)
    list_info = get_url_list('url_checks', 'url_id', id)
    return render_template('urls_view.html',
                           url=url,
                           list_info=list_info)


@app.route('/urls')
def urls():
    urls = get_info_url()
    return render_template('urls.html', urls=urls), 200


@app.route('/urls/<id>/checks', methods=["POST"])
def checks(id):
    url = get_column('name', 'id', id)
    html = get_content(url)
    if html:
        status_code, h1, title, description = html_content(html)
        save_info_url(id, status_code, h1, title, description)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('urls_view', id=id))
    flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('urls_view', id=id))


if __name__ == '__main__':
    app.run(debug=DEBUG_SWITCH)
