"""
This module is for showing that Moves can be generated using aiohttp.
"""

import aiohttp
import asyncio


class Moves:
    """Moves represents the moves of a specific pokemon."""

    def __init__(self, name: str, id_: int, generation: str, accuracy: int,
                 pp: int, power: int, type_: str, damage_class: str,
                 effect_short: str):
        """
        Initialize moves.
        :param name: str
        :param id_: int
        :param generation: str
        :param accuracy: int
        :param pp: int
        :param power: int
        :param type_: str
        :param damage_class: str
        :param effect_short: str
        """
        self.name = name
        self.id = id_
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


class APIClass:
    @classmethod
    async def get_move(cls, url: str, session: aiohttp.ClientSession) -> dict:
        """
        Creates and returns a Move object from url.
        :param url: the url containing a json containing move values
        :param session: an aiohttp ClientSession
        :return: Move object
        """
        response = await session.request(method='GET', url=url)
        # " '.json()' : Read response’s body as JSON, return dict"
        json_response = await response.json()
        a_move = Moves(
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

        return a_move

    @classmethod
    async def process_move_requests(cls, id_list: list):
        """
        Processes and obtains move objects obtained from the list.

        :param id_list: list of move ids
        """
        url = 'https://pokeapi.co/api/v2/move/{}'
        async with aiohttp.ClientSession() as session:
            list_urls = [url.format(req_id) for req_id in id_list]
            coroutines = [cls.get_move(a_url, session) for a_url in list_urls]
            responses = await asyncio.gather(*coroutines)
            print(responses)
            for res in responses:
                print(res)


def main():
    """
    Creates Moves from a list of move ids.
    :return: int
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    list_o_move_ids = [1, 2, 3, 4]
    response = loop.run_until_complete(
        APIClass.process_move_requests(list_o_move_ids))
    # print(response)
    # print(type(response))


if __name__ == '__main__':
    main()
