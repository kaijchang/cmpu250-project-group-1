import json
import os

import requests
from bs4 import BeautifulSoup

data_dir_path = os.path.join(os.path.dirname(__file__), '..', 'data')
imdb_data_file_path = os.path.join(data_dir_path, 'imdb-original.json')
data_file_path = os.path.join(data_dir_path, 'box-office-mojo-original.json')

with open(imdb_data_file_path, 'r') as f:
    imdb_data = json.load(f)

print(len(imdb_data))

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0'})

data = {}

for title_id in imdb_data:
    print(title_id)

    response = session.get(f'https://www.boxofficemojo.com/title/{title_id}')
    if response.url.endswith('/credits/'):
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    is_release_page = False

    by_release_header = soup.find('h3', text='By Release')
    original_release_link = soup.find('a', text='Original Release')
    if by_release_header:
        if original_release_link:
            response = session.get(f'https://www.boxofficemojo.com{original_release_link["href"]}')
            soup = BeautifulSoup(response.text, 'html.parser')
            is_release_page = True
        else:
            continue

    data[title_id] = {}

    tables = soup.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[(2 if is_release_page else 1):]
        for tr in trs:
            tds = tr.find_all('td')
            name, release_date, opening, gross = (td.text.strip() for td in tds)
            data[title_id][name] = {
                'release_date': release_date,
                'opening': opening,
                'gross': gross
            }

    print(data[title_id])

    with open(data_file_path, 'w') as f:
        json.dump(data, f)
