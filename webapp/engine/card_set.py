"""
This module contains the CardSet class.
"""


class CardSet(object):

    """
    A card set is simply a set of cards. This could be anything from
    52 playing cards to every magic card created. These can be loaded
    from a configuration file or defined via python.
    """

    def load_from_dict(self, dictionary):
        """
        This function takes in a dictonary and uses that to create the card set.
        This will add to anything that is currently in the card set.
        """

        pass

    def all_cards(self):
        """
        Return a list of all the cards for this card set.
        """

        return []

    def create(self, card_name, number=1):
        """
        Create an instance of the card with card_name. If number == 1 then this
        will return a single instance. Otherwise this returns a list of cards
        each of which is a copy of the card_name.
        """

        pass

    def create_set(self):
        """
        Create a single instance of every card in this set. This will return a
        list which contains a Card object for every card in this set.
        """

        pass
