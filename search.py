from blackjack import generate_deck, shuffle_all_decks, calculate_hand_value, display_hand, convert_to_tuples
from collections import deque
import random

def simulate_outcome(deck, hand, dealer_hand, depth=3):
    """
    Simulates outcomes for a given state using BFS.
    - deck: Remaining cards in the deck
    - hand: Player's current hand
    - dealer_hand: Dealer's current hand
    - depth: Number of levels to explore in the decision tree
    Returns a dictionary of outcomes (win, lose, tie, bust).
    """
    outcomes = {"win": 0, "lose": 0, "tie": 0, "bust": 0}
    queue = deque([(hand, dealer_hand, deck, True, 0)])  # (player_hand, dealer_hand, deck, is_player_turn, current_depth)

    while queue:
        curr_hand, curr_dealer_hand, curr_deck, is_player_turn, curr_depth = queue.popleft()

        # Terminal state or maximum depth reached
        if curr_depth >= depth or calculate_hand_value(curr_hand) > 21:
            player_value = calculate_hand_value(curr_hand)
            dealer_value = calculate_hand_value(curr_dealer_hand)

            if player_value > 21:
                outcomes["bust"] += 1
            elif dealer_value > 21:
                outcomes["win"] += 1
            elif player_value > dealer_value:
                outcomes["win"] += 1
            elif player_value < dealer_value:
                outcomes["lose"] += 1
            else:
                outcomes["tie"] += 1
            continue

        # Player's turn
        if is_player_turn:
            # "Stand" branch
            queue.append((curr_hand, curr_dealer_hand, curr_deck, False, curr_depth + 1))

            # "Hit" branch
            for i, card in enumerate(curr_deck):
                new_hand = curr_hand + [card]
                new_deck = curr_deck[:i] + curr_deck[i + 1:]
                queue.append((new_hand, curr_dealer_hand, new_deck, True, curr_depth + 1))

        # Dealer's turn
        else:
            dealer_value = calculate_hand_value(curr_dealer_hand)
            if dealer_value >= 17:
                # Evaluate final state
                queue.append((curr_hand, curr_dealer_hand, curr_deck, False, curr_depth + 1))
            else:
                for i, card in enumerate(curr_deck):
                    new_dealer_hand = curr_dealer_hand + [card]
                    new_deck = curr_deck[:i] + curr_deck[i + 1:]
                    queue.append((curr_hand, new_dealer_hand, new_deck, False, curr_depth + 1))

    return outcomes
def resolve_stand(player_hand, dealer_hand, deck):
    """
    Resolves the game when the player stands.
    Simulates the dealer's turn and determines the final outcome.
    """
    dealer_value = calculate_hand_value(dealer_hand)

    # Dealer's turn: hit until at least 17
    while dealer_value < 17 or (dealer_value == 17 and 'A' in [card[0] for card in dealer_hand]):
        dealer_hand.append(deck.pop())
        dealer_value = calculate_hand_value(dealer_hand)

    # Evaluate outcomes
    player_value = calculate_hand_value(player_hand)
    if player_value > 21:
        return {"win": 0, "lose": 1, "tie": 0, "bust": 1}  # Player busts
    if dealer_value > 21:
        return {"win": 1, "lose": 0, "tie": 0, "bust": 0}  # Dealer busts
    if player_value > dealer_value:
        return {"win": 1, "lose": 0, "tie": 0, "bust": 0}
    if player_value < dealer_value:
        return {"win": 0, "lose": 1, "tie": 0, "bust": 0}
    return {"win": 0, "lose": 0, "tie": 1, "bust": 0}  # Tie

def recommend_action(player_hand, dealer_hand, deck, depth=3):
    """
    Recommends whether the player should hit or stand based on simulated outcomes.
    """
    # Simulate "hit" by exploring all possible cards in the deck
    outcomes_hit = {"win": 0, "lose": 0, "tie": 0, "bust": 0}
    for i, card in enumerate(deck):
        new_hand = player_hand + [card]
        new_deck = deck[:i] + deck[i+1:]
        hit_outcomes = simulate_outcome(new_deck, new_hand, dealer_hand, depth)
        for outcome in outcomes_hit:
            outcomes_hit[outcome] += hit_outcomes[outcome] / len(deck)

    # Simulate "stand" by resolving the dealer's turn
    outcomes_stand = resolve_stand(player_hand, dealer_hand, deck)

    # Calculate scores for hit and stand
    prob_hit = outcomes_hit["win"] / (sum(outcomes_hit.values()) or 1)
    prob_stand = outcomes_stand["win"] / (sum(outcomes_stand.values()) or 1)

    # Recommend the action with the higher win probability
    return "hit" if prob_hit > prob_stand else "stand"

def play_blackjack_with_recommendations():
    # Generate and shuffle decks
    all_decks = []
    num_decks = 1
    for _ in range(num_decks):
        all_decks.extend(generate_deck())
    shuffled_deck = shuffle_all_decks(all_decks)
    deck = convert_to_tuples(shuffled_deck)

    # Deal initial hands
    player_hand = [deck.pop()]
    dealer_hand = [deck.pop()]
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())

    print("Dealer's hand:")
    display_hand(dealer_hand, hide_first_card=True)

    print("Your hand:", calculate_hand_value(player_hand))
    display_hand(player_hand)

    # Player's turn
    while calculate_hand_value(player_hand) < 21:
        recommendation = recommend_action(player_hand, dealer_hand, deck)
        print(f"Recommendation:{recommendation} ")
        move = recommendation
        #input(f"Do you want to hit or stand? (Recommended: {recommendation}) ").lower()
        if move == 'hit':
            player_hand.append(deck.pop())
            print("Your hand:", calculate_hand_value(player_hand))
            display_hand(player_hand)
        elif move == 'stand':
            break
        else:
            print("Invalid input. Please enter 'hit' or 'stand'.")

    # Evaluate player bust
    player_value = calculate_hand_value(player_hand)
    if player_value > 21:
        print("You busted! Dealer wins.")
        return "lose"  # Player busts, dealer wins

    # Dealer's turn
    print("Dealer's hand:")
    display_hand(dealer_hand)
    while calculate_hand_value(dealer_hand) < 17 or (
        calculate_hand_value(dealer_hand) == 17 and 'A' in [card[0] for card in dealer_hand]
    ):
        dealer_hand.append(deck.pop())
        print("Dealer's hand:")
        display_hand(dealer_hand)

    # Evaluate dealer bust
    dealer_value = calculate_hand_value(dealer_hand)
    if dealer_value > 21:
        return "win"  # Dealer busts, player wins

    # Final evaluation
    if player_value > dealer_value:
        return "win"
    elif player_value < dealer_value:
        return "lose"
    else:
        return "tie"  # Equal values result in a tie

if __name__ == "__main__":
    result = play_blackjack_with_recommendations()
