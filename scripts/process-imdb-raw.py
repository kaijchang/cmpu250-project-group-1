import json
import csv
import os

data_dir_path = os.path.join(os.path.dirname(__file__), '..', 'data')
raw_data_file_path = os.path.join(data_dir_path, 'imdb-raw.json')
processed_data_file_path = os.path.join(data_dir_path, 'imdb-processed.csv')

with open(raw_data_file_path, 'r') as f:
    raw_data = json.load(f)

print(len(raw_data))

with open(processed_data_file_path, 'w') as f:
    writer = csv.writer(f)

    header_row = [
        'id',
        'title',
        'genres',
        'weighted_rating',
        'release_year',
    ]

    for i in range(1, 11):
        header_row.append(f'rating_{i}')

    for i in range(5):
        header_row.append(f'country_{i}')
        for j in range(1, 11):
            header_row.append(f'country_{i}_rating_{j}')
    
    writer.writerow(header_row)

    for title_data in raw_data.values():
        node = title_data['node']

        title_id = node['title']['id']
        title_text = node['title']['titleText']['text']
        genres = ','.join([genre['genre']['text'] for genre in node['title']['titleGenres']['genres']])
        release_year = node['title']['releaseDate']['year']

        weighted_rating = title_data['weighted_rating']
        top_countries = title_data['top_countries']

        row = [
            title_id,
            title_text,
            genres,
            weighted_rating,
            release_year,
        ]

        for i in range(10):
            row.append(node['title']['aggregateRatingsBreakdown']['histogram']['histogramValues'][i]['voteCount'])

        for i in range(5):
            row.append(top_countries[i])
            country_histogram = title_data[f'{i}_histogram']
            for j in range(10):
                row.append(country_histogram[j]['voteCount'])
        
        writer.writerow(row)
