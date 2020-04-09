import argparse
import time
import threading
import requests
import concurrent.futures
import multiprocessing

from pokedex_maker import PokedexMaker
from pokeretriever.pokeretriever import *


class Arguments:
    """
    Arguments has the values needed to make a request to get pokemon data.
    """

    def __init__(self, mode: str, input_data: str, expanded: bool,
                 input_file: str = None, output_file: str = None):
        """
        Initialize a Arguments.
        :param mode string (but wil be enum on final assignment)
        :param input_data str, data of the intended request, usually the
        name of the id of the object being queried
        :param expanded bool
        :param input_file str, name relative path of the input file
        :param output_file, str, data of the output file
        """
        self.mode = mode
        self.input_data = input_data
        self.expanded = expanded
        self.input_file = input_file
        self.output_file = output_file

    def __str__(self):
        """Returns the current state of the request"""
        return f'current state of Arguments={str(vars(self))}'


class ArgumentParser:
    """
    ArgumentParser deals with commandline arguments.
    """

    @classmethod
    def setup_commandline_request(cls):
        """
        Reads and verifies that the proper commandline arguments where
        provided and creates a creates a Request object using values.
        :return: Request Object
        """
        parser = argparse.ArgumentParser()

        parser.add_argument('mode', type=str,
                            choices=["pokemon", "ability", "move"],
                            help="The mode to get information about the "
                                 "pokemon, Can be one of: 'pokemon', "
                                 "'ability', or 'move')")
        input_group = parser.add_mutually_exclusive_group(required=True)
        input_group.add_argument('--inputfile', type=str, dest='input_file',
                                 help="The name/relative path of the input "
                                      "file.")
        input_group.add_argument('--inputdata', type=str, dest='input_data',
                                 help="data of the intended request. usually "
                                      "the name or the id of the object "
                                      "being queried")
        parser.add_argument('--expanded', action='store_true',
                            help='When provided, certain attributes are '
                                 'expanded')
        parser.add_argument('--output', type=str, dest='output_file',
                            help='the output file name')

        kwarg = vars(parser.parse_args())
        req = Arguments(**kwarg)
        return req


class Driver:
    def __init__(self):
        self.pokedex_objects = None  # PokedexObject
        self.arguments = None  # Arguments

    def start(self):
        self.arguments = ArgumentParser.setup_commandline_request()

        if self.arguments.input_file is not None:
            name_id_list = self._get_name_id_list(self.arguments.input_file)
        else:
            name_id_list = [self.arguments.input_data]
        pokedex_requests = []
        for name_id in name_id_list:
            pokedex_requests.append(PokedexRequest(
                self.arguments.mode,
                name_id,
                self.arguments.expanded
            ))

        tp = ThreadPool(pokedex_requests, multiprocessing.cpu_count())
        self.pokedex_objects = tp.download()

        if self.arguments.output_file is not None:
            file_reporter = TextFileReporter(self.arguments.output_file)
            report = Report(self.pokedex_objects, file_reporter.make_report)
            report.export()
        else:
            terminal_reporter = TerminalReporter()
            report = Report(self.pokedex_objects,
                            terminal_reporter.make_report)
            report.export()

    def _get_name_id_list(self, file_name) -> list:
        with open(file_name, mode='r', encoding='utf-8') as file:
            return [line for line in file]


class Report:
    """
    Creates a report using the provided formatter method.
    Uses a strategy pattern for the export method.
    """

    def __init__(self, pokedex_objects: list, formatter):
        """
        Initialized a Report with the supplied parameters.
        :param pokedex_objects: list of PokedexObjects
        :param formatter: a method that takes a list of PokedexObjects
        """
        self.pokedex_objects = pokedex_objects
        self.formatter = formatter

    def export(self):
        """
        Export the report with the provided export method.
        """
        self.formatter(self.pokedex_objects)


class TerminalReporter:
    """
    Contains a make_report method to display all pokemon in a list in the
    terminal.
    Part of a strategy pattern for Report.
    """

    def __init__(self):
        pass

    def make_report(self, pokedex_objects: list):
        print('Terminal Report')
        for pokedex in pokedex_objects:
            print(pokedex)


class TextFileReporter:
    """
    Contains a make_report method to display all pokemon in a list in a
    text file.
    Part of a strategy pattern for Report.
    """

    def __init__(self, file_name: str):
        self.file_name = file_name

    def make_report(self, pokedex_objects: list):
        with open(self.file_name, 'w') as file:
            for pokedex in pokedex_objects:
                file.write(pokedex)


class ThreadPool:
    def __init__(self, pokedex_requests: list, max_workers: int):
        self.pokedex_requests = pokedex_requests
        self.max_workers = max_workers

    def download(self):
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.max_workers) as executor:
            with requests.Session() as session:
                pokedex_maker = PokedexMaker(session)

                result = executor.map(pokedex_maker.execute_request,
                                      self.pokedex_requests)
        return list(result)


def main():
    driver = Driver()
    driver.start()


if __name__ == '__main__':
    main()
