# `data`

`box-office-mojo-original.json`: Original dataset scraped from Box Office Mojo, no longer in use.
`imdb-original.json`: Original dataset scraped from IMDb.
`imdb-cleaned.csv`: Cleaned version of the dataset to be used in Jupyter notebooks.

## Codebook

\* Variables not in `imdb-cleaned.csv` that are calculated in the latest Jupyter notebook.

| Variables | Description |
| :---      |         :---| 
| title | A nominal variable for the title of the movie |
| genres | A list of genres for each movie. |
| weighted_rating | A continuous numeric variable for the weighted average of user votes calculated using a proprietary algorithm. IMDb uses an alternative algorithm when "unusual voting activity is detected." |
| release_year | A categorical variable for the year the movie was released |
| keywords | A list of keywords for each movie. |
| rating_{1...10} | A discrete numeric variable for the total number of votes for each rating. |
| country_{0...4} | A nominal variable for each of the five countries with the most votes cast. |
| country_{0...4}_rating{1...10} | A discrete numeric variable for the number of votes for each rating for each of the five countries with the most votes cast. |
| unweighted_rating* | A continuous numeric variable for the average of user votes before the proprietery algorithm is applied |
| total_votes* | A discrete numeric variable for the total number of votes across each rating | 
| polarization_score | A continuous numeric variable that calculates a 'polarizaton score' based on Esteban and Ray's algorithm | 
| rating_diff* | A continuous numeric variable that calculates the difference beween weighted_rating and unweighted_rating | 
| country_ptp* | A discrete numeric variable that calculates difference between the highest and lowest average ratings between the top five countries with the most votes |
| max_country_ptp* | A nominal variable that records the country code wiith the highest ratings for a given movie |
| min_country_ptp* | A nominal variable that records the country code with the lowest ratings for a given movie |

