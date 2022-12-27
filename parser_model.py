import requests
from bs4 import BeautifulSoup

URL = 'https://www.radartutorial.eu/19.kartei/'
MAIN_URL_SUFFIX = 'ka03.ru.html'


def delete_suffix(text):
    return text[:-1]


def delete_prefix_and_suffix_spaces(text):
    while len(text) > 0 and text.startswith(' '):
        text = text[1:]

    while len(text) > 0 and text.endswith(' '):
        text = text[:-1]

    return text


def handle_text(tmp_text):
    tmp_text = tmp_text.replace('\r', '\n')
    elems = tmp_text.split('\n')
    elems_without_zero_strings = []
    for string in elems:
        string = delete_prefix_and_suffix_spaces(string)
        if len(string) != 0 and string != 'Страница в разработке':
            elems_without_zero_strings.append(string)

    new_text = ' '.join(elems_without_zero_strings[1:])
    return new_text


def get_index_of_model(model, models):
    return models.index(model)


def get_models():
    page = requests.get(URL + MAIN_URL_SUFFIX)
    soup = BeautifulSoup(page.text, "html.parser")
    result = soup.findAll('a', class_='ttip')
    return [delete_suffix(line.text) for line in result]


def get_discription_by_model(model):
    page = requests.get(URL + MAIN_URL_SUFFIX)
    soup = BeautifulSoup(page.text, "html.parser")
    result_page = soup.findAll('a', class_='ttip')
    index_of_model = get_index_of_model(model, [delete_suffix(line.text) for line in result_page])

    description_page = requests.get(URL + result_page[index_of_model].get('href'))
    soup = BeautifulSoup(description_page.text, "html.parser")
    return handle_text(soup.findAll('section', class_='fliesstext')[0].text)
