# Summary: Enhancing the Accuracy of the Alphabet Enhanced Model

## Introduction

The goal of this work was to improve the predictive accuracy of a simple alphabetical football match outcome predictor (the "alphabet model") by incorporating additional statistical features and combining them in a principled, weighted manner. The target was to exceed 50% accuracy on the 2021 Barclays Premier League season, as measured by historical match data.

## Methodology

### Baseline Model
The baseline "alphabet model" predicts the outcome of a match based solely on the alphabetical order of the home and away team names. This naive approach achieved approximately 40% accuracy.

### Feature Engineering and Model Enhancement
To improve upon the baseline, the following features were engineered from historical match results:

1. **Pair Majority Outcome**: The most common outcome (home win, away win, draw) for each (home, away) team pair in the training data.
2. **Home Team Majority Outcome**: The most common outcome for each home team when playing at home.
3. **Away Team Majority Outcome**: The most common outcome for each away team when playing away.
4. **Team Win Rate**: The average win rate for each team over the most recent three seasons.
5. **Team Goal Difference**: The average goal difference (goals scored minus goals conceded) for each team over the most recent three seasons.

### Weighted Voting System
A weighted voting system was implemented to combine the above features. For each possible match outcome (HOME, AWAY, DRAW), a score was computed as follows:

- Pair majority outcome: +3 to the predicted outcome
- Home team majority: +2 to the predicted outcome
- Away team majority: +2 to the predicted outcome
- Win rate: +1 to HOME if home win rate > away, +1 to AWAY if away win rate > home
- Goal difference: +1 to HOME if home goal diff > away, +1 to AWAY if away goal diff > home

The outcome with the highest total score was selected as the prediction. In the event of a tie, the model fell back to the original alphabetical rule.

## Results

The enhanced model ("alphabet_enhanced") was evaluated on the 2021 Barclays Premier League season. The accuracy improved from 40% (alphabet model) to 52.4%, surpassing the 50% target and approaching the performance of more sophisticated models such as the Points and Offense Simulator models.

| Model               | Accuracy |
|---------------------|----------|
| Alphabet            | 0.400    |
| Alphabet Enhanced   | 0.524    |
| Points              | 0.539    |
| Offense Simulator   | 0.505    |
| Full Simulator      | 0.550    |

## Conclusion

By systematically incorporating historical pairwise outcomes, team-specific statistics, and recent performance metrics into a weighted voting framework, the predictive accuracy of the alphabet-based model was significantly improved. This approach demonstrates the value of feature engineering and ensemble-style decision making in sports outcome prediction. 