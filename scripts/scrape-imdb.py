import json
import os

import requests
from bs4 import BeautifulSoup

data_dir_path = os.path.join(os.path.dirname(__file__), '..', 'data')
data_file_path = os.path.join(data_dir_path, 'imdb-original.json')

advanced_title_search_query = """
fragment BaseTitleCard on Title {
    id
    titleText {
        text
    }
    releaseDate {
        year
    }
}

fragment TitleListItemMetadata on Title {
    ...BaseTitleCard
}

query AdvancedTitleSearch(
    $first: Int!
    $after: String
    $titleTypeConstraint: TitleTypeSearchConstraint
    $interestConstraint: InterestSearchConstraint
    $genreConstraint: GenreSearchConstraint
    $certificateConstraint: CertificateSearchConstraint
    $characterConstraint: CharacterSearchConstraint
    $userRatingsConstraint: UserRatingsSearchConstraint
    $titleTextConstraint: TitleTextSearchConstraint
    $creditedCompanyConstraint: CreditedCompanySearchConstraint
    $explicitContentConstraint: ExplicitContentSearchConstraint
    $sortBy: AdvancedTitleSearchSortBy!
    $sortOrder: SortOrder!
    $releaseDateConstraint: ReleaseDateSearchConstraint
    $colorationConstraint: ColorationSearchConstraint
    $runtimeConstraint: RuntimeSearchConstraint
    $watchOptionsConstraint: WatchOptionsSearchConstraint
    $awardConstraint: AwardSearchConstraint
    $rankedTitleListConstraint: RankedTitleListSearchConstraint
    $titleCreditsConstraint: TitleCreditsConstraint
    $inTheatersConstraint: InTheatersSearchConstraint
    $soundMixConstraint: SoundMixSearchConstraint
    $keywordConstraint: KeywordSearchConstraint
    $originCountryConstraint: OriginCountrySearchConstraint
    $languageConstraint: LanguageSearchConstraint
    $episodicConstraint: EpisodicSearchConstraint
    $alternateVersionMatchingConstraint: AlternateVersionMatchingSearchConstraint
    $crazyCreditMatchingConstraint: CrazyCreditMatchingSearchConstraint
    $goofMatchingConstraint: GoofMatchingSearchConstraint
    $filmingLocationConstraint: FilmingLocationSearchConstraint
    $plotMatchingConstraint: PlotMatchingSearchConstraint
    $quoteMatchingConstraint: TitleQuoteMatchingSearchConstraint
    $soundtrackMatchingConstraint: SoundtrackMatchingSearchConstraint
    $triviaMatchingConstraint: TitleTriviaMatchingSearchConstraint
    $withTitleDataConstraint: WithTitleDataSearchConstraint
    $myRatingConstraint: MyRatingSearchConstraint
    $listConstraint: ListSearchConstraint
) {
    advancedTitleSearch(
        first: $first
        after: $after
        constraints: {
            titleTypeConstraint: $titleTypeConstraint
            genreConstraint: $genreConstraint
            certificateConstraint: $certificateConstraint
            characterConstraint: $characterConstraint
            userRatingsConstraint: $userRatingsConstraint
            titleTextConstraint: $titleTextConstraint
            creditedCompanyConstraint: $creditedCompanyConstraint
            explicitContentConstraint: $explicitContentConstraint
            releaseDateConstraint: $releaseDateConstraint
            colorationConstraint: $colorationConstraint
            runtimeConstraint: $runtimeConstraint
            watchOptionsConstraint: $watchOptionsConstraint
            awardConstraint: $awardConstraint
            rankedTitleListConstraint: $rankedTitleListConstraint
            titleCreditsConstraint: $titleCreditsConstraint
            inTheatersConstraint: $inTheatersConstraint
            soundMixConstraint: $soundMixConstraint
            keywordConstraint: $keywordConstraint
            originCountryConstraint: $originCountryConstraint
            languageConstraint: $languageConstraint
            episodicConstraint: $episodicConstraint
            alternateVersionMatchingConstraint: $alternateVersionMatchingConstraint
            crazyCreditMatchingConstraint: $crazyCreditMatchingConstraint
            goofMatchingConstraint: $goofMatchingConstraint
            filmingLocationConstraint: $filmingLocationConstraint
            plotMatchingConstraint: $plotMatchingConstraint
            quoteMatchingConstraint: $quoteMatchingConstraint
            soundtrackMatchingConstraint: $soundtrackMatchingConstraint
            triviaMatchingConstraint: $triviaMatchingConstraint
            withTitleDataConstraint: $withTitleDataConstraint
            myRatingConstraint: $myRatingConstraint
            listConstraint: $listConstraint
            interestConstraint: $interestConstraint
        }
        sort: { sortBy: $sortBy, sortOrder: $sortOrder }
    ) {
        total
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
        edges {
            node {
                title {
                    ...TitleListItemMetadata
                    aggregateRatingsBreakdown {
                        histogram {
                            histogramValues {
                                voteCount
                                rating
                            }
                        }
                    }
                }
            }
        }
    }
}"""

title_keywords_query = """
query TitleKeywordsQuery($tconst: ID!) {
    title(id: $tconst) {
        keywords(first: 100) {
            edges {
                node {
                    keyword {
                        text {
                            text
                        }
                    }
                }
            }
        }
    }
}"""

title_filtered_histogram_data_query = """
query TitleFilteredHistogramData($tconst: ID!, $country: Country!) {
    title(id: $tconst) {
        aggregateRatingsBreakdown {
            histogram(demographicFilter: {country: $country}) {
                histogramValues {
                    voteCount
                    rating
                }
            }
        }
    }
}"""

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0'})
graphql_url = 'https://caching.graphql.imdb.com'

after = None

if os.path.exists(data_file_path):
    with open(data_file_path) as f:
        all_data = json.load(f)
else:
    all_data = {}

while True:
    print(after)

    response = session.post(graphql_url, json={
        'query': advanced_title_search_query,
        'variables': {
            'first': 1000,
            'after': after,
            'sortBy': 'POPULARITY',
            'sortOrder': 'ASC',
            'titleTypeConstraint': {
                'anyTitleTypeIds': ['movie']
            },
            'userRatingsConstraint': {
            'ratingsCountRange': {
                'min': 50000
            } 
            }
        }
    })

    page_data = response.json()

    after = page_data['data']['advancedTitleSearch']['pageInfo']['endCursor']

    for edge_idx, edge in enumerate(page_data['data']['advancedTitleSearch']['edges']):
        title_data = {}

        node = edge['node']
        title_data['node'] = node

        title_id = node['title']['id']

        if title_id in all_data:
            continue

        title_url = f'https://www.imdb.com/title/{title_id}'

        print(edge_idx, node['title']['titleText']['text'], title_url)
        
        response = session.get(title_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        interest_div = soup.find(attrs={'data-testid': 'interests'})

        title_data['genres'] = [a.text for a in interest_div.find_all('a')]
        print(title_data['genres'])

        ratings_url = f'https://www.imdb.com/title/{title_id}/ratings'

        response = session.get(ratings_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        weighted_rating = soup.find(attrs={
            'data-testid': 'rating-button__aggregate-rating__score'
        }).find('span').text

        unweighted_rating = soup.find(attrs={
            'data-testid': 'calculations-label'
        }).text.split(' ')[0]

        rating_group = soup.find(class_='ipc-chip-group')

        top_countries = [button['id'].split('-')[-1] for button in rating_group.find_all('button')]

        title_data['weighted_rating'] = weighted_rating
        title_data['unweighted_rating'] = unweighted_rating
        title_data['top_countries'] = top_countries

        response = session.post(graphql_url, json={
            'query': title_keywords_query,
            'variables': {
                'tconst': title_id,
            }
        })
        data = response.json()['data']
        
        title_data['keywords'] = [keyword['node']['keyword']['text']['text'] for keyword in data['title']['keywords']['edges']]

        for country_idx, country in enumerate(top_countries):
            response = session.post(graphql_url, json={
                'query': title_filtered_histogram_data_query,
                'variables': {
                    'tconst': title_id,
                    'country': country
                }
            })
            data = response.json()['data']

            histogram_data = data['title']['aggregateRatingsBreakdown']['histogram']['histogramValues']

            title_data[f'{country_idx}_histogram'] = histogram_data

        all_data[title_id] = title_data

        with open(data_file_path, 'w') as f:
            json.dump(all_data, f)

    if not page_data['data']['advancedTitleSearch']['pageInfo']['hasNextPage']:
        break
