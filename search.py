import blackjack

def simulate_outcome(deck, hand, dealer_hand, depth=3):
    """
    Simulates outcomes for a given state using BFS.
    - deck: Remaining cards in the deck
    - hand: Player's current hand
    - dealer_hand: Dealer's current hand
    - depth: Number of levels to explore in the decision tree
    """
    from collections import deque
    import itertools

    # Nodes will store (player_hand, dealer_hand, deck, player_turn, score)
    queue = deque([(hand, dealer_hand, deck[:], True, 0)])  # True if player's turn
    outcomes = {"win": 0, "lose": 0, "tie": 0, "bust": 0}

    # BFS on decision tree
    for _ in range(depth):
        for _ in range(len(queue)):
            curr_hand, curr_dealer_hand, curr_deck, player_turn, _ = queue.popleft()
            curr_value = blackjack.calculate_hand_value(curr_hand)

            # Check for terminal state
            if curr_value > 21:  # Player busts
                outcomes["bust"] += 1
                continue

            if not player_turn:  # Dealer's turn
                dealer_value = blackjack.calculate_hand_value(curr_dealer_hand)
                if dealer_value >= 17:
                    # Compare hands
                    if dealer_value > 21 or curr_value > dealer_value:
                        outcomes["win"] += 1
                    elif curr_value < dealer_value:
                        outcomes["lose"] += 1
                    else:
                        outcomes["tie"] += 1
                    continue

                # Dealer draws a card
                for i, card in enumerate(curr_deck):
                    new_deck = curr_deck[:i] + curr_deck[i + 1:]
                    new_dealer_hand = curr_dealer_hand + [card]
                    queue.append((curr_hand, new_dealer_hand, new_deck, False, 0))
            else:
                # Player's turn: Hit or Stand
                # "Stand" branch
                queue.append((curr_hand, curr_dealer_hand, curr_deck, False, 0))

                # "Hit" branch
                for i, card in enumerate(curr_deck):
                    new_deck = curr_deck[:i] + curr_deck[i + 1:]
                    new_hand = curr_hand + [card]
                    queue.append((new_hand, curr_dealer_hand, new_deck, True, 0))

    return outcomes

def recommend_action(player_hand, dealer_hand, deck):
    """
    Recommends whether the player should hit or stand based on simulated outcomes.
    """
    outcomes_hit = simulate_outcome(deck, player_hand + [deck[0]], dealer_hand)
    outcomes_stand = simulate_outcome(deck, player_hand, dealer_hand)

    # Calculate win probabilities
    prob_hit = outcomes_hit["win"] / (sum(outcomes_hit.values()) or 1)
    prob_stand = outcomes_stand["win"] / (sum(outcomes_stand.values()) or 1)

    return "hit" if prob_hit > prob_stand else "stand"

# Integrate into the game loop
def play_blackjack_with_recommendations():
    deck = blackjack.create_deck(3)

    player_hand = [deck.pop()]
    dealer_hand = [deck.pop()]
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())

    print("Dealer's hand:")
    blackjack.display_hand(dealer_hand, hide_first_card=True)

    print("Your hand:", blackjack.get_hand_total(player_hand))
    blackjack.display_hand(player_hand)

    while blackjack.calculate_hand_value(player_hand) < 21:
        recommendation = recommend_action(player_hand, dealer_hand, deck)
        print(f"Recommendation: {recommendation}")

        move = input("Do you want to 'hit' or 'stand'? (Recommended: {}) ".format(recommendation)).lower()
        if move == 'hit':
            player_hand.append(deck.pop())
            print("Your hand:", blackjack.get_hand_total(player_hand))
            blackjack.display_hand(player_hand)
        elif move == 'stand':
            break
        else:
            print("Invalid input. Please enter 'hit' or 'stand'.")

    player_value = blackjack.calculate_hand_value(player_hand)
    if player_value > 21:
        print("You busted! Dealer wins.")
        return

    print("Dealer's hand:")
    blackjack.display_hand(dealer_hand)

    while blackjack.calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
        print("Dealer's hand:")
        blackjack.display_hand(dealer_hand)

    dealer_value = blackjack.calculate_hand_value(dealer_hand)

    if dealer_value > 21 or player_value > dealer_value:
        print("You win!")
    elif player_value < dealer_value:
        print("Dealer wins.")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_blackjack_with_recommendations()
