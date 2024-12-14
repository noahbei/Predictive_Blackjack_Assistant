# Predictive Blackjack Assistant

This project provides a predictive assistant for Blackjack, recommending whether to "hit" or "stand". It has two main ways to do this: one that simulates all possible game states and another that uses Hi-Lo card counting.

## Features

- **Search Based Algorithm**: Simulates all possible game states to recommend whether to "hit" or "stand" based on the player's current hand and the dealer's up card.
- **Hi-Lo Card Counting**: Enhances decision-making by keeping track of the running count, adjusting recommendations based on the true count of the remaining cards in the deck.
- **Game Simulation**: Supports automated simulations of Blackjack games to evaluate the assistant's performance over many iterations.

## Requirements

- Python 3
- `unittest` (for testing purposes)

## Installation

To install and use this project, clone the repository and install the required dependencies.

```bash
git clone https://github.com/noahbei/Predictive_Blackjack_Assistant
cd Predictive_Blackjack_Assistant
pip install -r requirements.txt
```
## Usage
To run the search-based predictive blackjack assistant:
```bash
python3 main.py
```
This will start a blackjack game where the assistant automatically makes recommendations based on the simulated outcomes. You can interact with the game in non-automated mode by responding to the recommendations.

To run the Hi-Lo predictive blackjack assistant:
```bash
python3 hilo_blackjack.py
```
This version uses the Hi-Lo card counting method to adjust the recommendations based on the running count.

Testing the Assistant
To run automated simulations and test the assistant's performance:
```bash
$ python3 -m unittest "tests/test_hilo_blackjack.py" 
```
```bash
$ python3 -m unittest "tests/test_search_blackjack.py" 
```
This will run 10,000 simulations, recording the outcomes (win, loss, tie) and providing statistics on the assistant's performance.

