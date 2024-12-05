import unittest
from collections import Counter
from search import play_blackjack_with_recommendations

class TestBlackjackSimulation(unittest.TestCase):
    def test_simulation_outcomes(self):
        results = {"win": 0, "lose": 0, "tie": 0}
        num_simulations = 1000  # Increase this for more robust statistics

        for _ in range(num_simulations):
            result = play_blackjack_with_recommendations()
            self.assertIn(result, ["win", "lose", "tie"], "Unexpected simulation result.")
            results[result] += 1

        # Validate that outcomes are within reasonable ranges
        total = sum(results.values())
        win_rate = results["win"] / total
        loss_rate = results["lose"] / total
        tie_rate = results["tie"] / total

        print(f"Simulation outcomes after {num_simulations} games:")
        print(f"Wins: {results['win']} ({win_rate * 100:.2f}%)")
        print(f"Losses: {results['lose']} ({loss_rate * 100:.2f}%)")
        print(f"Ties: {results['tie']} ({tie_rate * 100:.2f}%)")

        # Basic assertions for blackjack outcome probabilities
        self.assertGreater(win_rate, 0.3, "Win rate is unreasonably low.")
        self.assertGreater(loss_rate, 0.3, "Loss rate is unreasonably low.")
        self.assertGreater(tie_rate, 0.05, "Tie rate is unreasonably low.")
        self.assertLess(win_rate, 0.6, "Win rate is unreasonably high.")
        self.assertLess(loss_rate, 0.6, "Loss rate is unreasonably high.")
        self.assertLess(tie_rate, 0.2, "Tie rate is unreasonably high.")

if __name__ == "__main__":
    unittest.main()
