from CRUD.crud_utils import get_field

response = get_field('urls', 'name', 'http://google.com')

print(response)