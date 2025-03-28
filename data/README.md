# Codebook

| Variables | Description |
| :---      |         :---| 
| weighted_rating | A continuous numeric variable for the weighted average of user votes calculated using a proprietary algorithm. IMDb uses an alternative algorithm when "unusual voting activity is detected." | 
| unweighted_rating| A continuous numeric variable for the average of user votes before the proprietery algorithm is applied | 
| rating_{1...10} | A discrete numeric variable for the total number of votes for each rating. |
| country_{0...4} | A nominal variable for each of the five countries with the most votes cast. |
| country_{0...4}_rating{1...10} | A discrete numeric variable for the number of votes for each rating for each of the five countries with the most votes cast. |
| total_votes | A discrete numeric variable for the total number of votes across each rating | 
| polarization_score | A continuous numeric variable that calculates the 'polarizaton score' based on Esteban and Ray's algorithm | 
| rating_diff | A continuous numeric variable that calculates the difference beween weighted_rating and unweighted_rating | 
| country_ptp | A discrete numeric variable that calculates difference between the highest and lowest average ratings between the top five countries with the most votes |
| max_country_ptp | A discrete numeric variable that records the country code wiith the highest ratings for a given movie |
| min_country_ptp | A discrete numeric variable that records the country code with the lowest ratings for a given movie |
| gross | A discrete numeric variable that represents the total US box office earnings of a given movie 
