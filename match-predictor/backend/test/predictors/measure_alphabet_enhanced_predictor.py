from unittest import TestCase

from matchpredictor.evaluation.evaluator import Evaluator
from matchpredictor.matchresults.results_provider import training_results, validation_results
from matchpredictor.predictors.alphabet_enhanced_predictor import train_alphabet_enhanced_predictor
from test.predictors import csv_location


class TestAlphabetEnhancedPredictor(TestCase):
    def test_accuracy_english_premier_league_2021(self) -> None:
        # Train on all seasons before 2021, validate on 2021 English Premier League
        training_data = training_results(csv_location, 2021, result_filter=lambda r: r.season < 2021 and r.fixture.league == 'Barclays Premier League')
        validation_data = validation_results(csv_location, 2021, result_filter=lambda r: r.season == 2021 and r.fixture.league == 'Barclays Premier League')
        predictor = train_alphabet_enhanced_predictor(training_data)

        accuracy, _ = Evaluator(predictor).measure_accuracy(validation_data)

        self.assertGreaterEqual(accuracy, .5) 