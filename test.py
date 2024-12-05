import pydealer
import random

def calculate_hand_value(hand):
    value = 0
    ace_count = 0
    for card in hand:
        if card.value in ["Jack", "Queen", "King"]:
            value += 10
        elif card.value == "Ace":
            ace_count += 1
            value += 11
        else:
            value += int(card.value)

    while value > 21 and ace_count:
        value -= 10
        ace_count -= 1

    return value

def display_hand(player, hand):
    print(f"{player}'s hand: {', '.join(map(str, hand))} (Value: {calculate_hand_value(hand)})")

def main():
    deck = pydealer.Deck()
    deck.shuffle()

    player_hand = deck.deal(2)
    dealer_hand = deck.deal(2)

    display_hand("Player", player_hand)
    display_hand("Dealer", dealer_hand[:1])

    while calculate_hand_value(player_hand) < 21:
        action = random.choice(["hit", "stay"])
        if action == "hit":
            player_hand.add(deck.deal(1))
            display_hand("Player", player_hand)
        elif action == "stay":
            break

    if calculate_hand_value(player_hand) > 21:
        print("Player busts! Dealer wins.")
        return

    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.add(deck.deal(1))

    display_hand("Dealer", dealer_hand)

    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if dealer_value > 21 or player_value > dealer_value:
        print("Player wins!")
        return 0
    elif player_value < dealer_value:
        print("Dealer wins!")
        return 1
    else:
        print("It's a tie!")
        return 2

if __name__ == "__main__":
    main()
    win = 0
    tie = 0
    lost = 0
    for x in range(5000):
        if main() == 0:
            win += 1
        elif main() == 1:
            lost += 1
        else:
            tie += 1
    print(win, tie, lost)