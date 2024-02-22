from page_analyzer.CRUD.crud_utils import get_field, to_dict_table
from urllib.request import urlopen
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

urls = to_dict_table('urls')
responses = []
for url in urls:
    with urlopen(url['name']) as response:
       url['response_cod'] = response.getcode()
print(urls)
