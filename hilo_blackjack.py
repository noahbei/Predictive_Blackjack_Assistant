from shuffling_deck import Card, generate_deck, shuffle_all_decks
from blackjack import convert_to_tuples, calculate_hand_value, display_hand
from collections import deque

# Hi-Lo card counting values
hilo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

# Updates the running count based on the given hand.
def calculate_running_count(hand, running_count):
    for card in hand:
        rank = card[0]
        if rank in hilo_values:
            running_count += hilo_values[rank]
    return running_count

# Converts running count to true count based on the number of remaining decks.
def true_count(running_count, remaining_decks):
    if remaining_decks == 0:
        return running_count
    return running_count / remaining_decks

# Recommends an action based on the true count.
def recommend_hilo_action(player_hand, dealer_hand, running_count, remaining_decks):
    true_count_value = true_count(running_count, remaining_decks)

    # Basic strategy combined with Hi-Lo count:
    if true_count_value >= 1:
        return "hit" if calculate_hand_value(player_hand) <= 16 else "stand"
    else:
        return "stand" if calculate_hand_value(player_hand) >= 12 else "hit"

# Generate and shuffle decks
def play_blackjack_hilo(num_decks=1):
    all_decks = []
    for _ in range(num_decks):
        all_decks.extend(generate_deck())
    shuffled_deck = shuffle_all_decks(all_decks)
    deck = convert_to_tuples(shuffled_deck)

    # Initialize hands and running count
    player_hand = [deck.pop()]
    dealer_hand = [deck.pop()]
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())

    # Initialize running count based on initial hands
    running_count = calculate_running_count(player_hand + dealer_hand, 0)

    print("Dealer's hand:")
    display_hand(dealer_hand, hide_first_card=True)

    print("Your hand:", calculate_hand_value(player_hand))
    display_hand(player_hand)

    # Player's turn
    while calculate_hand_value(player_hand) < 21:
        remaining_decks = len(deck) // 52
        recommendation = recommend_hilo_action(player_hand, dealer_hand, running_count, remaining_decks)
        if recommendation == 'hit':
            new_card = deck.pop()
            player_hand.append(new_card)
            running_count = calculate_running_count([new_card], running_count)
            print("Your hand:", calculate_hand_value(player_hand))
            display_hand(player_hand)
        elif recommendation == 'stand':
            break

    player_value = calculate_hand_value(player_hand)
    if player_value > 21:
        print("You busted! Dealer wins.")
        return "lose"

    # Dealer's turn
    print("Dealer's hand:")
    display_hand(dealer_hand)
    while calculate_hand_value(dealer_hand) < 17:
        new_card = deck.pop()
        dealer_hand.append(new_card)
        running_count = calculate_running_count([new_card], running_count)
        print("Dealer's hand:")
        display_hand(dealer_hand)

    dealer_value = calculate_hand_value(dealer_hand)
    if dealer_value > 21:
        print("Dealer busted! You win.")
        return "win"

    # Final evaluation
    if player_value > dealer_value:
        print("You win!")
        return "win"
    elif player_value < dealer_value:
        print("Dealer wins.")
        return "lose"
    else:
        print("It's a tie!")
        return "tie"

if __name__ == "__main__":
    result = play_blackjack_hilo()
    print(result)
