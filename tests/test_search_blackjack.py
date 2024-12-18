import unittest
from collections import Counter
from main import play_blackjack_with_recommendations

class TestBlackjackSimulation(unittest.TestCase):
    def test_simulation_outcomes(self):
        results = {"win": 0, "lose": 0, "tie": 0}
        num_simulations = 10000 

        for _ in range(num_simulations):
            result = play_blackjack_with_recommendations(automated = True)
            self.assertIn(result, ["win", "lose", "tie"], "Unexpected simulation result.")
            results[result] += 1

        total = sum(results.values())
        win_rate = results["win"] / total
        loss_rate = results["lose"] / total
        tie_rate = results["tie"] / total

        print(f"Simulation outcomes after {num_simulations} games:")
        print(f"Wins: {results['win']} ({win_rate * 100:.2f}%)")
        print(f"Losses: {results['lose']} ({loss_rate * 100:.2f}%)")
        print(f"Ties: {results['tie']} ({tie_rate * 100:.2f}%)")

if __name__ == "__main__":
    unittest.main()
