"""
This module contains the code required to create an aiohttp session and
execute requests, parse the JSON and instantiate the appropriate object,
and houses the Pokemon, Ability, Move, and Stat classes.
"""


class PokedexRequest:
    """
    Request has the values needed to make a request to get pokemon data.
    """

    def __init__(self, mode: str, name_or_id: str, expanded: bool,
                 num_threads=1):
        """
        Initialize a request.
        :param mode string (but wil be enum on final assignment)
        name of the id of the object being queried
        :param name_or_id the name or id number of the Pokemon
        :param expanded bool an optional flag that prompts the pokedex to do a
        sub-query to get more information about a particular attribute
        :param num_threads the number of threads the request can use.
        """
        self.mode = mode
        self.name_or_id = name_or_id
        self.expanded = expanded
        self.num_threads = num_threads

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
    def __init__(self, name: str, id_: int, height: int, weight: int, stats,
                 types: list, abilities, move, expanded: bool):
        """
        :param height: int, the height of the Pokemon
        :param weight: int, the weight of the Pokemon
        :param stats: a list of stats the Pokemon has
        :param types: a list of the types the Pokemon has
        :param abilities: a list of the Pokemon's abilities
        :param move: a list of the Pokemon's moves
        """
        super().__init__(name, id_)
        self.height = height
        self.weight = weight
        self.stats = stats
        self.types = types
        self.abilities = abilities
        self.move = move
        self.expanded = expanded

    def types_str(self):
        result = ''
        for a_type in self.types:
            result += f'\n\t\t Name: {a_type}'
        return result

    def stats_str(self):
        result = ''
        if self.expanded:
            for stat in self.stats:
                stat = str(stat).replace('\n', "\n\t\t")
                result += f'\n\t\t{stat}'
            return result

    def abilities_str(self):
        result = ''
        if self.expanded:
            for ability in self.abilities:
                ability = str(ability).replace('\n', "\n\t\t")
                result += f'{ability}'
            return result
        else:
            for ability in self.abilities:
                result += f'\n\t\tName: {ability}'
            return result

    def move_str(self):
        result = ''
        if self.expanded:
            for move in self.move:
                move = str(move).replace('\n', "\n\t\t")
                result += f'\n\t\t{move}'
            return result
        else:
            result = ''
            for move in self.move:
                result += f'\n\t\tName: {move[0]}, Level: {move[1]}'
            return result

    def __str__(self):
        """Returns the current state of the Pokemon"""
        return f'Pokemon: {self.name} ' \
               f'\n\tId: {self.id}' \
               f'\n\tHeight: {self.height}' \
               f'\n\tWeight: {self.weight}' \
               f'\n\tStats: {self.stats_str()}' \
               f'\n\tTypes: {self.types_str()}' \
               f'\n\tAbility: {self.abilities_str()}' \
               f'\n\tMoves: {self.move_str()}' \
               f'\n\tExpanded: {self.expanded}'


class Ability(PokedexObject):

    def __init__(self, name: str, id_: int, generation: str, effect: str,
                 effect_short: str, pokemon: list):
        """
        :param generation: str, the generation in which the move was
        introduced
        :param effect: str, the effect of the ability
        :param effect_short: str, a short description of the Pokemon's effect
        :param Pokemon: list, a list of Pokemon that could potentially have
        this ability
        """
        super().__init__(name, id_)
        self.generation = generation
        self.effect = effect
        self.effect_short = effect_short
        self.pokemon = pokemon

    def __str__(self):
        """Returns the current state of the Ability"""
        effect = self.effect.replace("\n", " ")
        effect_short = self.effect_short.replace('\n', ' ')
        result = f'\nName: {self.name}' \
                 f'\nId: {self.id}' \
                 f'\nGeneration: {self.generation}' \
                 f'\nEffect: {effect}, ' \
                 f'\nEffect short: {effect_short}' \
                 f'\nPokemon:'
        for pokemon in self.pokemon:
            result += f' {pokemon}'
        return result


class Move(PokedexObject):
    """
    Moves are the skills of Pokemon in battle.
    """

    def __init__(self, name: str, id_: int, generation: str, accuracy: int,
                 pp: int, power: int, type_: str, damage_class: str,
                 effect_short: str):
        """
        :param generation: str, the generation in which the move was
        introduced
        :param accuracy: int, percent value of how successful the move is
        :param pp: int, power points, the number of times the move can be
        used
        :param power: int, the base power of the move
        :param type_: str, the elemental type of the move
        :param damage_class: str, the type of damage the move inflicts on the
        target
        :param effect_short: str, a short description of the Pokemon's effect
        """
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
        effect_short = self.effect_short.replace('\n', ' ')
        result = f'\nName: {self.name}' \
                 f'\nId: {self.id}' \
                 f'\nGeneration: {self.generation}' \
                 f'\nAccuracy: {self.accuracy}' \
                 f'\nPP: {self.pp}' \
                 f'\nPower: {self.power}' \
                 f'\nType: {self.type}' \
                 f'\nDamage Class: {self.damage_class}' \
                 f'\nEffect Short: {self.effect_short}'
        return result


class Stat(PokedexObject):
    """
    Pokemon queries in the expanded mode allows the user to query more details
    about the stat of the Pokemon. The stat of the Pokemon grows as they gain
    levels.
    """

    def __init__(self, name: str, id_: int, is_battle_only: bool):
        """
        :param is_battle_only: bool, whether this stat only exists
        within a battle
        """
        super().__init__(name, id_)
        self.is_battle_only = is_battle_only

    def __str__(self):
        """Returns the current state of the Move"""
        result = f'\nName: {self.name}' \
                 f'\nID: {self.id}' \
                 f'\nBattle only: {self.is_battle_only}'
        return result
