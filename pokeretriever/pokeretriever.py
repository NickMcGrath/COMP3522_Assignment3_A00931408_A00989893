"""
This module contains the code required to create an aiohttp session and
execute requests, parse the JSON and instantiate the appropriate object,
and houses the Pokemon, Ability, Move, and Stat classes.
"""
import aiohttp


class PokedexRequest:
    """
    Request has the values needed to make a request to get pokemon data.
    """

    def __init__(self, mode: str, name_or_id: str, expanded: bool, session):
        """
        Initialize a request.
        :param mode string (but wil be enum on final assignment)
        name of the id of the object being queried
        :param name_or_id the name or id number of the Pokemon
        :param expanded bool an optional flag that prompts the pokedex to do a
        sub-query to get more information about a particular attribute
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
    def __init__(self, name: str, id_: int):
        """Initialize moves."""
        self.name = name
        self.id = id_

    def __str__(self):
        """Returns the current state of the Move"""
        return f'PokedexObject={str(vars(self))}'


class Pokemon(PokedexObject):
    def __init__(self, name: str, id_: int, height: int, weight: int, stats, types: list,
                 abilities, move):
        super().__init__(name, id_)
        self.height = height
        self.weight = weight
        self.stats = stats
        self.types = types
        self.abilities = abilities
        self.move = move

    def __str__(self):
        """Returns the current state of the Move"""
        return f'Pokemon={str(vars(self))}'


class Ability(PokedexObject):
    def __init__(self, name: str, id_: int, generation: str, effect: str, effect_short: str,
                 Pokemon: list):
        super().__init__(name, id_)
        self.generation = generation
        self.effect = effect
        self.effect_short = effect_short
        self.Pokemon = Pokemon

    def __str__(self):
        """Returns the current state of the Move"""
        return f'current state of Ability={str(vars(self))}'


class Move(PokedexObject):
    """Moves represents the moves of a specific pokemon."""
    def __init__(self, name: str, id_: int, generation: str, accuracy: int, pp: int, power: int,
                 type_: str, damage_class: str, effect_short: str):
        super().__init__(name, id_)
        self.generation = generation
        self.accuracy = accuracy
        self.pp = pp
        self.power = power
        self.type = type_
        self.damage_class = damage_class
        self.effect_short = effect_short

    def __str__(self):
        """Returns the current state of the Move"""
        return f'current state of Moves={str(vars(self))}'


class Stat(PokedexObject):
    def __init__(self, name: str, id_: int, is_battle_only: bool):
        """Initialize moves."""
        super().__init__(name, id_)
        self.is_battle_only = is_battle_only

    def __str__(self):
        """Returns the current state of the Move"""
        return f'current state of Stat={str(vars(self))}'
