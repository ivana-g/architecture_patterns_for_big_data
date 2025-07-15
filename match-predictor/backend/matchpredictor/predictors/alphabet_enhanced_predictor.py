from collections import Counter, defaultdict
from typing import List, Tuple, Dict
from matchpredictor.matchresults.result import Fixture, Outcome, Result
from matchpredictor.predictors.predictor import Prediction, Predictor
from matchpredictor.predictors.alphabet_predictor import AlphabetPredictor

class AlphabetEnhancedPredictor(Predictor):
    def __init__(self, pair_majority: Dict[Tuple[str, str], Outcome], home_majority: Dict[str, Outcome], away_majority: Dict[str, Outcome], team_win_rate: Dict[str, float], team_goal_diff: Dict[str, float]):
        self.pair_majority = pair_majority
        self.home_majority = home_majority
        self.away_majority = away_majority
        self.team_win_rate = team_win_rate
        self.team_goal_diff = team_goal_diff
        self.fallback = AlphabetPredictor()

    def predict(self, fixture: Fixture) -> Prediction:
        home = fixture.home_team.name.lower()
        away = fixture.away_team.name.lower()
        key = (home, away)
        scores = {Outcome.HOME: 0, Outcome.AWAY: 0, Outcome.DRAW: 0}
        # Pair majority (weight 3)
        if key in self.pair_majority:
            scores[self.pair_majority[key]] += 3
        # Home majority (weight 2)
        if home in self.home_majority:
            scores[self.home_majority[home]] += 2
        # Away majority (weight 2)
        if away in self.away_majority:
            scores[self.away_majority[away]] += 2
        # Win rate (weight 1)
        if home in self.team_win_rate and away in self.team_win_rate:
            if self.team_win_rate[home] > self.team_win_rate[away]:
                scores[Outcome.HOME] += 1
            elif self.team_win_rate[home] < self.team_win_rate[away]:
                scores[Outcome.AWAY] += 1
        # Goal difference (weight 1)
        if home in self.team_goal_diff and away in self.team_goal_diff:
            if self.team_goal_diff[home] > self.team_goal_diff[away]:
                scores[Outcome.HOME] += 1
            elif self.team_goal_diff[home] < self.team_goal_diff[away]:
                scores[Outcome.AWAY] += 1
        # Pick the outcome with the highest score
        max_score = max(scores.values())
        best_outcomes = [outcome for outcome, score in scores.items() if score == max_score]
        if len(best_outcomes) == 1:
            return Prediction(outcome=best_outcomes[0])
        else:
            return self.fallback.predict(fixture)

def train_alphabet_enhanced_predictor(training_data: List[Result]) -> AlphabetEnhancedPredictor:
    pair_outcomes = defaultdict(list)
    home_outcomes = defaultdict(list)
    away_outcomes = defaultdict(list)
    team_results = defaultdict(list)
    team_goal_diff = defaultdict(list)
    # Determine the most recent season in the training data
    seasons = [result.season for result in training_data]
    if seasons:
        max_season = max(seasons)
        recent_seasons = {max_season, max_season-1, max_season-2}
    else:
        recent_seasons = set()
    for result in training_data:
        home = result.fixture.home_team.name.lower()
        away = result.fixture.away_team.name.lower()
        pair_outcomes[(home, away)].append(result.outcome)
        home_outcomes[home].append(result.outcome)
        away_outcomes[away].append(result.outcome)
        # For win rate and goal diff: only use results from recent seasons
        if result.season in recent_seasons:
            if result.outcome == Outcome.HOME:
                team_results[home].append(1)
                team_results[away].append(0)
            elif result.outcome == Outcome.AWAY:
                team_results[home].append(0)
                team_results[away].append(1)
            else:
                team_results[home].append(0.5)
                team_results[away].append(0.5)
            # Goal difference
            team_goal_diff[home].append(result.home_goals - result.away_goals)
            team_goal_diff[away].append(result.away_goals - result.home_goals)
    pair_majority = {k: Counter(v).most_common(1)[0][0] for k, v in pair_outcomes.items()}
    home_majority = {k: Counter(v).most_common(1)[0][0] for k, v in home_outcomes.items()}
    away_majority = {k: Counter(v).most_common(1)[0][0] for k, v in away_outcomes.items()}
    team_win_rate = {k: sum(v)/len(v) if v else 0.0 for k, v in team_results.items()}
    team_goal_diff_avg = {k: sum(v)/len(v) if v else 0.0 for k, v in team_goal_diff.items()}
    return AlphabetEnhancedPredictor(pair_majority, home_majority, away_majority, team_win_rate, team_goal_diff_avg) 