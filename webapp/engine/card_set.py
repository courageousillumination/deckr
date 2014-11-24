"""
This module contains the CardSet class.
"""

from engine.card import Card


def create_card_from_dict(card_def):
    """
    This is a simple function that will make a card from a dictionary of
    attributes.
    """

    card = Card()
    for attribute in card_def:
        setattr(card, attribute, card_def[attribute])

    return card


class CardSet(object):

    """
    A card set is simply a set of cards. This could be anything from
    52 playing cards to every magic card created. These can be loaded
    from a configuration file or defined via python.
    """

    def __init__(self):
        self.cards = {}

    def load_from_list(self, card_list):
        """
        This function takes in a list of dicts and uses that to create the card
        set. If any card definition in the list does not have a name, it will be
        considered an invalid card definition and will not be included in the
        card set.  This will add to anything that is currently in the card set.
        A card added to the card set will overwrite any card already in the card
        set with the same name.
        """

        for card_def in card_list:
            card_name = card_def.get('name', None)
            if card_name is not None:
                self.cards[card_name] = card_def

    def all_cards(self):
        """
        Return a list of all the cards for this card set.
        """

        return self.cards.values()

    def create(self, card_name, number=1):
        """
        Create an instance of the card with card_name. If number == 1 then this
        will return a single instance. Otherwise this returns a list of cards
        each of which is a copy of the card_name.  If there is no card with
        card_name in the card set, then an error will be thrown.
        """

        card_name = self.cards.get(card_name, None)
        if card_name is None:
            raise ValueError("Unable to get card {0}".format(card_name))

        if number == 1:
            return create_card_from_dict(card_name)
        elif number > 1:
            return [create_card_from_dict(card_name) for _ in range(number)]

    def create_set(self):
        """
        Create a single instance of every card in this set. This will return a
        list which contains a Card object for every card in this set.
        """

        return [create_card_from_dict(self.cards[x]) for x in self.cards]
