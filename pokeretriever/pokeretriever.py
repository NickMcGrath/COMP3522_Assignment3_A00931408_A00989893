"""
This module contains the code required to create an aiohttp session and
execute requests, parse the JSON and instantiate the appropriate object,
and houses the Pokemon, Ability, Move, and Stat classes.
"""
import aiohttp


class Request:
    """
    Request has the values needed to make a request to get pokemon data.
    """

    def __init__(self, mode: str, name_or_id: str, expanded: bool, session):
        """
        Initialize a request.
        :param mode string (but wil be enum on final assignment)
        name of the id of the object being queried
        :param name_or_id
        :param expanded bool
        :param session
        """
        self.mode = mode
        self.name_or_id = name_or_id
        self.expanded = expanded
        self.session = session

    def __str__(self):
        """Returns the current state of the request"""
        return f'current state of Request={str(vars(self))}'


class PokedexObject:
    pass


class Pokemon(PokedexObject):
    pass


class Ability(PokedexObject):
    pass


class Move(PokedexObject):
    pass


class Stat(PokedexObject):
    pass
