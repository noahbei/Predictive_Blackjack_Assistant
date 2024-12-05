from blackjack import generate_deck, shuffle_all_decks, calculate_hand_value, display_hand, convert_to_tuples

def simulate_outcome(deck, hand, dealer_hand, depth=3, is_player_turn=True):
    """
    Simulates outcomes for a given state using a search algorithm (Minimax-like approach).
    - deck: Remaining cards in the deck
    - hand: Player's current hand
    - dealer_hand: Dealer's current hand
    - depth: Number of levels to explore in the decision tree
    - is_player_turn: Whether it's the player's turn
    Returns a dictionary of outcomes (win, lose, tie, bust).
    """
    if depth == 0 or calculate_hand_value(hand) > 21:
        # Terminal state or maximum depth reached
        player_value = calculate_hand_value(hand)
        dealer_value = calculate_hand_value(dealer_hand)

        if player_value > 21:
            return {"win": 0, "lose": 1, "tie": 0, "bust": 1}
        if dealer_value > 21:
            return {"win": 1, "lose": 0, "tie": 0, "bust": 0}
        if player_value > dealer_value:
            return {"win": 1, "lose": 0, "tie": 0, "bust": 0}
        if player_value < dealer_value:
            return {"win": 0, "lose": 1, "tie": 0, "bust": 0}
        return {"win": 0, "lose": 0, "tie": 1, "bust": 0}

    outcomes = {"win": 0, "lose": 0, "tie": 0, "bust": 0}

    if is_player_turn:
        # Player's turn: Hit or Stand
        for i, card in enumerate(deck):
            new_hand = hand + [card]
            new_deck = deck[:i] + deck[i + 1:]
            result = simulate_outcome(new_deck, new_hand, dealer_hand, depth - 1, False)
            for key in outcomes:
                outcomes[key] += result[key]

        # "Stand" branch
        result = simulate_outcome(deck, hand, dealer_hand, depth - 1, False)
        for key in outcomes:
            outcomes[key] += result[key]

    else:
        # Dealer's turn: Hit until 17 or higher
        dealer_value = calculate_hand_value(dealer_hand)
        if dealer_value >= 17:
            result = simulate_outcome(deck, hand, dealer_hand, depth - 1, True)
            for key in outcomes:
                outcomes[key] += result[key]
        else:
            for i, card in enumerate(deck):
                new_dealer_hand = dealer_hand + [card]
                new_deck = deck[:i] + deck[i + 1:]
                result = simulate_outcome(new_deck, hand, new_dealer_hand, depth - 1, True)
                for key in outcomes:
                    outcomes[key] += result[key]

    return outcomes

def recommend_action(player_hand, dealer_hand, deck, depth=3):
    """
    Recommends whether the player should hit or stand based on simulated outcomes.
    """
    outcomes_hit = simulate_outcome(deck, player_hand + [deck[0]], dealer_hand, depth)
    outcomes_stand = simulate_outcome(deck, player_hand, dealer_hand, depth)

    # Calculate win probabilities
    prob_hit = outcomes_hit["win"] / (sum(outcomes_hit.values()) or 1)
    prob_stand = outcomes_stand["win"] / (sum(outcomes_stand.values()) or 1)

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
        print(f"Recommendation: {recommendation}")

        move = input(f"Do you want to 'hit' or 'stand'? (Recommended: {recommendation}) ").lower()
        if move == 'hit':
            player_hand.append(deck.pop())
            print("Your hand:", calculate_hand_value(player_hand))
            display_hand(player_hand)
        elif move == 'stand':
            break
        else:
            print("Invalid input. Please enter 'hit' or 'stand'.")

    # Final evaluation
    player_value = calculate_hand_value(player_hand)
    if player_value > 21:
        print("You busted! Dealer wins.")
        return

    print("Dealer's hand:")
    display_hand(dealer_hand)
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
        print("Dealer's hand:")
        display_hand(dealer_hand)

    dealer_value = calculate_hand_value(dealer_hand)

    if dealer_value > 21 or player_value > dealer_value:
        print("You win!")
    elif player_value < dealer_value:
        print("Dealer wins.")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_blackjack_with_recommendations()
