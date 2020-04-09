import concurrent

import requests

from pokeretriever.pokeretriever import *


class PokedexMaker:
    session = None

    def __init__(self, session):
        PokedexMaker.session = session

    @classmethod
    def execute_request(cls, pokedex_request: PokedexRequest) -> PokedexObject:
        if pokedex_request.mode == 'pokemon':
            return cls._get_pokemon(pokedex_request.name_or_id,
                                    pokedex_request.expanded)
        elif pokedex_request.mode == 'stat':
            return cls._get_stats(pokedex_request.name_or_id)
        elif pokedex_request.mode == 'ability':
            return cls._get_abilities(pokedex_request.name_or_id)
        elif pokedex_request.mode == 'move':
            return cls._get_move(pokedex_request.name_or_id)

    @classmethod
    def _get_pokemon(cls, name: str, expanded=False):
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        with cls.session.get(url) as response:
            json_response = response.json()
            if expanded:
                with concurrent.futures.ThreadPoolExecutor(
                        max_workers=10) as executor:
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
        url = f'https://pokeapi.co/api/v2/stat/{name}'
        with cls.session.get(url) as response:
            json_response = response.json()
            return Stat(
                name=json_response['name'],
                id_=json_response['id'],
                is_battle_only=json_response['is_battle_only']
            )

    @classmethod
    def _get_abilities(cls, name: str):
        url = f'https://pokeapi.co/api/v2/ability/{name}'
        with cls.session.get(url) as response:
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
        url = f'https://pokeapi.co/api/v2/move/{name}'
        with cls.session.get(url) as response:
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


def test_method():
    with concurrent.futures.ThreadPoolExecutor(
            max_workers=1) as executor:
        with requests.Session() as session:
            pokedex_maker = PokedexMaker(session)
            result = executor.map(pokedex_maker._get_pokemon, (1,))

    results = list(result)
    # print(list(result))
    print(results[0])


if __name__ == '__main__':
    test_method()
