import concurrent

import requests

from pokeretriever.pokeretriever import *


class PokedexMaker:
    session = None

    def __init__(self, session):
        PokedexMaker.session = session

    @classmethod
    def execute_request(cls, pokedex_request: PokedexRequest) -> PokedexObject:
        pass

    @classmethod
    def _get_pokemon(cls, name: str, expanded=True):
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        with cls.session.get(url) as response:
            json_response = response.json()
            if expanded:
                return Pokemon(
                    name=json_response['name'],
                    id_=json_response['id'],
                    height=json_response['height'],
                    weight=json_response['weight'],
                    stats=[cls._get_stats(stat['stat']['name']) for stat in
                           json_response['stats']],
                    types=[a_type['type']['name'] for a_type
                           in json_response['types']],
                    abilities=[cls._get_abilities(ability['ability']['name'])
                               for ability in json_response['abilities']],
                    move=[cls._get_move(move['move']['name']) for move in
                          json_response['moves']]
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
                          for move in json_response['moves']]
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
