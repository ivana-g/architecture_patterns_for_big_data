from matchpredictor.matchresults.result import Fixture, Outcome
from matchpredictor.predictors.predictor import Prediction, Predictor

class AlphabetPredictor(Predictor):
    def predict(self, fixture: Fixture) -> Prediction:
        home = fixture.home_team.name.lower()
        away = fixture.away_team.name.lower()
        if home < away:
            return Prediction(outcome=Outcome.HOME)
        elif home > away:
            return Prediction(outcome=Outcome.AWAY)
        else:
            return Prediction(outcome=Outcome.DRAW) 