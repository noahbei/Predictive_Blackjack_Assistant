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

## How to play
After running either **`main.py`** or **`hilo_blackjack.py`**, players will be shown what cards have been dealt to them and the dealer. They will then be given a recommendation to either 'hit' or 'stand'. The user then gets to pick from these options by typing in the terminal. Continue this loop until the game ends to see who wins.

## Project File Structure
This is an overview of the files in the project and their respective purposes:

- **`.gitignore`**: Specifies which files and directories Git should ignore in version control.

- **`blackjack.py`**: Contains the core logic for a Blackjack game. It defines the rules, player actions, and game flow for a standard game of Blackjack.

- **`hilo_blackjack.py`**: Implements a variant of Blackjack, Hi-Lo Blackjack, where players are given recommendations to 'hit' or 'stand' whether the next card is higher or lower than the previous one.

- **`main.py`**: Implements a variant of Blackjack that uses searching where players are given recommendations to 'hit' or 'stand' based on the probability that a 'hit' or 'stand' will win.

- **`shuffling_deck.py`**: Contains code for shuffling the deck of cards, a critical function for card-based games like Blackjack.

- **`tests/`**: A directory containing unit tests for the project

  - **`tests/test_hilo_blackjack.py`**: Contains tests for the functionality of the Hi-Lo Blackjack game, ensuring that its rules and mechanics work correctly.
  
  - **`tests/test_search_blackjack.py`**: Contains tests for a "search" functionality within the Blackjack game (possibly related to card or player search), ensuring that the search feature works correctly.

  - **`tests/__init__.py`**: Marks the `tests` directory as a Python package and may include setup code for tests.
