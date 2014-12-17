from engine.card_game.card import Card

SUITS = ["clubs", "spades", "hearts", "diamonds"]

def create_deck(num = 1):
    """
    Creates num decks of playing cards returning them as a single array.
    """

    return [PlayingCard(suit, number)
            for suit in SUITS
            for number in range(1, 14)
            for _ in range(num)]

class PlayingCard(Card):
    """
    This represents a simple playing card.
    """

    def __init__(self, suit, number):
        super(PlayingCard, self).__init__()

        self.suit = suit
        self.number = number
        self.front_face = self.get_file_name()
        self.back_face = "b1fv.png"

    def get_file_name(self):
        """
        Converts a suit/number combination into a file name for the associated
        image.
        """

        if self.number == 1:
            return str(SUITS.index(self.suit) + 1) + ".png"
        dist_from_top = (13 - self.number) + 1
        offset = dist_from_top * 4 + 1 + SUITS.index(self.suit)
        return str(offset) + ".png"

    def get_color(self):
        """
        Returns the color of this card's suit.
        """

        if self.suit == "hearts" or self.suit == "diamonds":
            return "red"
        else:
            return "black"
