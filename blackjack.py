numDecks = 3

import random

# Define the deck and card values
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Function to create a deck
def create_deck(numDecks):
    deck = []
    for x in range(numDecks):
        for suit in suits:
            for rank in ranks:
                deck.append((rank, suit))
    random.shuffle(deck)
    return deck

# Function to calculate the value of a hand
def calculate_hand_value(hand):
    value = 0
    ace_count = 0
    for card in hand:
        value += values[card[0]]
        if card[0] == 'A':
            ace_count += 1
    while value > 21 and ace_count:
        value -= 10
        ace_count -= 1
    return value

def get_hand_total(hand):
    total = 0
    ace_count = 0
    for card in hand:
        rank = card[0]
        total += values[rank]
        if rank == 'A':
            ace_count += 1
    
    # Adjust for Aces if total value is greater than 21
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1
    
    return total

# Function to display a hand
def display_hand(hand, hide_first_card=False):
    if hide_first_card:
        print("[hidden]", hand[1])
    else:
        for card in hand:
            print(card, end=" ")
        print()

# Function to play the game
def play_blackjack():
    deck = create_deck(numDecks)

    player_hand = [deck.pop()]
    dealer_hand = [deck.pop()]
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())

    print("Dealer's hand:")
    display_hand(dealer_hand, hide_first_card=True)

    print("Your hand:", get_hand_total(player_hand))
    display_hand(player_hand)

    while calculate_hand_value(player_hand) < 21:
        move = input("Do you want to 'hit' or 'stand'? ").lower()
        if move == 'hit':
            player_hand.append(deck.pop())
            print("Your hand:", get_hand_total(player_hand))
            display_hand(player_hand) 
        elif move == 'stand':
            break
        else:
            print("Invalid input. Please enter 'hit' or 'stand'.")

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
    play_blackjack()

