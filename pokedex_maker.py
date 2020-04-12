"""
Module contains a facade to create PokeObjects from a request.
"""
import concurrent

from pokeretriever.pokeretriever import *


class InvalidPokeObject(Exception):
    """Exception for Invalid PokeObjects."""

    def __init__(self, name: str):
        """Initialize the exception with the name that did not work."""
        super().__init__()
        self.name = name

    def __str__(self):
        """display the name that cause the error."""
        return f'Invalid PokeObject {self.name}'


class PokedexMaker:
    """
    Facade to create PokeObjects from a request.
    """
    session = None

    def __init__(self, session):
        """
        Initialize a PokedexMaker.
        :param session: a requests.Session()
        """
        PokedexMaker.session = session

    @classmethod
    def execute_request(cls, pokedex_request: PokedexRequest) -> PokedexObject:
        """
        Creates a PokeObject from a request.
        :param pokedex_request: PokedexRequest
        :return: PokedexObject
        """
        if pokedex_request.mode == 'pokemon':
            return cls._get_pokemon(pokedex_request.name_or_id,
                                    pokedex_request.expanded,
                                    pokedex_request.num_threads)
        elif pokedex_request.mode == 'stat':
            return cls._get_stats(pokedex_request.name_or_id)
        elif pokedex_request.mode == 'ability':
            return cls._get_abilities(pokedex_request.name_or_id)
        elif pokedex_request.mode == 'move':
            return cls._get_move(pokedex_request.name_or_id)

    @classmethod
    def _get_pokemon(cls, name: str, expanded=False, num_threads=1):
        """
        Helper method to get a Pokemon.
        :param name: name or id of the pokemon
        :param expanded: bool
        :param num_threads: int max number of threads for request
        :return: Pokemon
        """
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        with cls.session.get(url) as response:
            if str(response.content) == "b'Not Found'":
                raise InvalidPokeObject(name)
            json_response = response.json()
            if expanded:
                with concurrent.futures.ThreadPoolExecutor(
                        max_workers=num_threads) as executor:
                    stats_param = [stat['stat']['name'] for stat in
                                   json_response['stats']]
                    stats_list = list(executor.map(cls._get_stats,
                                                   stats_param))
                    abilities_param = [ability['ability']['name']
                                       for ability in
                                       json_response['abilities']]
                    ability_list = list(executor.map(cls._get_abilities,
                                                     abilities_param))
                    moves_param = [move['move']['name'] for move in
                                   json_response['moves']]
                    moves_list = list(executor.map(cls._get_move,
                                                   moves_param))

                return Pokemon(
                    name=json_response['name'],
                    id_=json_response['id'],
                    height=json_response['height'],
                    weight=json_response['weight'],
                    stats=stats_list,
                    types=[a_type['type']['name'] for a_type
                           in json_response['types']],
                    abilities=ability_list,
                    move=moves_list,
                    expanded=expanded
                )
            else:
                return Pokemon(
                    name=json_response['name'],
                    id_=json_response['id'],
                    height=json_response['height'],
                    weight=json_response['weight'],
                    stats=[(stat['stat']['name'], stat['base_stat'])
                           for stat in json_response['stats']],
                    types=[a_type['type']['name'] for a_type
                           in json_response['types']],
                    abilities=[ability['ability']['name'] for
                               ability in json_response['abilities']],
                    move=[(move['move']['name'],
                           move['version_group_details'][0][
                               'level_learned_at'])
                          for move in json_response['moves']],
                    expanded=expanded
                )

    @classmethod
    def _get_stats(cls, name: str):
        """
        Helper method to get Stats.
        :param name: the name of the stat
        :return: Stat
        """
        url = f'https://pokeapi.co/api/v2/stat/{name}'
        with cls.session.get(url) as response:
            if str(response.content) == "b'Not Found'":
                raise InvalidPokeObject(name)
            json_response = response.json()
            return Stat(
                name=json_response['name'],
                id_=json_response['id'],
                is_battle_only=json_response['is_battle_only']
            )

    @classmethod
    def _get_abilities(cls, name: str):
        """
        Helper method to get Ability.
        :param name: the name of the Ability
        :return: Ability
        """
        url = f'https://pokeapi.co/api/v2/ability/{name}'
        with cls.session.get(url) as response:
            if str(response.content) == "b'Not Found'":
                raise InvalidPokeObject(name)
            json_response = response.json()
            return Ability(
                name=json_response['name'],
                id_=json_response['id'],
                generation=json_response['generation']['name'],
                effect=json_response['effect_entries'][0]['effect'],
                effect_short=json_response['effect_entries'][0]
                ['short_effect'],
                pokemon=[pokemon['pokemon']['name']
                         for pokemon in json_response['pokemon']]
            )

    @classmethod
    def _get_move(cls, name: str):
        """
        Helper method to get Move.
        :param name: the name of the Move
        :return: Move
        """
        url = f'https://pokeapi.co/api/v2/move/{name}'
        with cls.session.get(url) as response:
            if str(response.content) == "b'Not Found'":
                raise InvalidPokeObject(name)
            json_response = response.json()
            return Move(
                name=json_response['name'],
                id_=json_response['id'],
                generation=json_response['generation']['name'],
                accuracy=json_response['accuracy'],
                pp=json_response['pp'],
                power=json_response['power'],
                type_=json_response['type']['name'],
                damage_class=json_response['damage_class']['name'],
                effect_short=json_response['effect_entries'][0]['short_effect']
            )
