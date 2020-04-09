from pokeretriever.pokeretriever import *


class PokedexMaker:
    @classmethod
    def execute_request(cls, pokedex_request: PokedexRequest) -> PokedexObject:
        pass

    @classmethod
    def _get_pokemon(cls, name: str, expanded: bool, session):
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = await session.request(method='GET', url=url)
        json_response = await response.json()
        if expanded:
            return Pokemon(
                name=json_response['name'],
                id_=json_response['id'],
                height=json_response['height'],
                weight=json_response['weight'],
                stats=cls._get_stats(name),
                types=[a_type['type']['name'] for a_type
                       in json_response['types']],
                abilities=[ability['ability']['name'] for
                           ability in json_response['abilities']],
                move=cls._get_move(name)
            )

    @classmethod
    def _get_stats(cls, name: str, session):
        pass

    @classmethod
    def _get_abilities(cls, name: str, session):
        pass

    @classmethod
    def _get_move(cls, name: str, session):
        pass
