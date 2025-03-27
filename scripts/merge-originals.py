import json
import csv
import os

data_dir_path = os.path.join(os.path.dirname(__file__), '..', 'data')
imdb_original_data_file_path = os.path.join(data_dir_path, 'imdb-original.json')
box_office_mojo_original_data_file_path = os.path.join(data_dir_path, 'box-office-mojo-original.json')
cleaned_data_file_path = os.path.join(data_dir_path, 'imdb-cleaned.csv')

with open(imdb_original_data_file_path, 'r') as f:
    imdb_original_data = json.load(f)

with open(box_office_mojo_original_data_file_path, 'r') as f:
    box_office_mojo_original_data = json.load(f)

print(len(imdb_original_data))
print(len(box_office_mojo_original_data))

with open(cleaned_data_file_path, 'w') as f:
    writer = csv.writer(f)

    header_row = [
        'id',
        'title',
        'genres',
        'weighted_rating',
        'release_year',
        'gross',
    ]

    for i in range(1, 11):
        header_row.append(f'rating_{i}')

    for i in range(5):
        header_row.append(f'country_{i}')
        for j in range(1, 11):
            header_row.append(f'country_{i}_rating_{j}')
    
    writer.writerow(header_row)

    for title_id in imdb_original_data:
        title_data = imdb_original_data[title_id]
        box_office_data = box_office_mojo_original_data.get(title_id, {})

        node = title_data['node']

        title_id = node['title']['id']
        title_text = node['title']['titleText']['text']
        genres = ','.join([genre['genre']['text'] for genre in node['title']['titleGenres']['genres']])
        release_year = node['title']['releaseDate']['year']

        weighted_rating = title_data['weighted_rating']
        top_countries = title_data['top_countries']

        market = box_office_data.get('Domestic', { 'gross': None })
        gross = market['gross']

        row = [
            title_id,
            title_text,
            genres,
            weighted_rating,
            release_year,
            gross,
        ]

        for i in range(10):
            row.append(node['title']['aggregateRatingsBreakdown']['histogram']['histogramValues'][i]['voteCount'])

        for i in range(5):
            row.append(top_countries[i])
            country_histogram = title_data[f'{i}_histogram']
            for j in range(10):
                row.append(country_histogram[j]['voteCount'])
        
        writer.writerow(row)
