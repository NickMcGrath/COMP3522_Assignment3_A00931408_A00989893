"""
This module if for Creating and displaying or saving information about
Pokemon.
"""
import argparse
import requests
import concurrent.futures
import multiprocessing
import sys
from pokedex_maker import InvalidPokeObject, PokedexMaker
from pokeretriever.pokeretriever import *


class Arguments:
    """
    Arguments has the values needed to make a request to get pokemon data.
    """

    def __init__(self, mode: str, input_data: str, expanded: bool,
                 input_file: str = None, output_file: str = None):
        """
        Initialize a Arguments.
        :param mode string
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
    """
    The program driver.

    Takes command line arguments, gets the pokemon data, outputs the
    data in specified format.
    """

    def __init__(self):
        """
        Initialize a Driver with an empty PokedexObject list and
        arguments.
        """
        self.pokedex_objects = None  # PokedexObject
        self.arguments = None  # Arguments

    def start(self):
        """
        Takes command line arguments, gets the pokemon data, outputs the
        data in specified format.
        """
        self.arguments = ArgumentParser.setup_commandline_request()

        if self.arguments.input_file is not None:
            try:
                name_id_list = self._get_name_id_list(
                    self.arguments.input_file)
            except FileNotFoundError:
                print("Could not find your file "
                      ":( ensure it is at project level")
                sys.exit(1)
        else:
            name_id_list = [self.arguments.input_data]
        pokedex_requests = []
        # append requests to list
        for name_id in name_id_list:
            pokedex_requests.append(PokedexRequest(
                self.arguments.mode,
                name_id,
                self.arguments.expanded,
                4  # number of threads each request can expand to
            ))
        # download the objects
        downloader = PokeObjectDownloader(pokedex_requests,
                                          multiprocessing.cpu_count())
        try:
            self.pokedex_objects = downloader.download()
        except InvalidPokeObject as e:
            print(e)
            sys.exit(2)

        if self.arguments.output_file is not None:
            file_reporter = TextFileReporter(self.arguments.output_file)
            report = Report(self.pokedex_objects, file_reporter.make_report)
            report.export()
        else:
            terminal_reporter = TerminalReporter()
            report = Report(self.pokedex_objects,
                            terminal_reporter.make_report)
            report.export()

    @staticmethod
    def _get_name_id_list(file_name) -> list:
        """
        Helper method to get a list of pokeObject names or ids.
        :param file_name: str, the file name.
        :return: list of pokeObject names
        """

        with open(file_name, mode='r', encoding='utf-8') as file:
            return [line.strip('\n') for line in file]


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
        Exports the pokedex objects to the appropriate formatter.
        :return:
        """
        self.formatter(self.pokedex_objects)


class TerminalReporter:
    """
    Contains a make_report method to display all pokemon in a list in the
    terminal.
    Part of a strategy pattern for Report.
    """

    def __init__(self):
        """
        Initialize a TerminalReporter
        """
        pass

    def make_report(self, pokedex_objects: list):
        """
        Makes a terminal report.
        :param pokedex_objects: list of PokeObjects
        """
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
        """
        Initialize a TextFileReporter.
        :param file_name: str, the output file name.
        """
        self.file_name = file_name

    def make_report(self, pokedex_objects: list):
        """
        Makes a text file report.
        :param pokedex_objects: list of PokeObjects
        """
        with open(self.file_name, 'w') as file:
            for pokedex in pokedex_objects:
                file.write(str(pokedex))


class PokeObjectDownloader:
    """
    PokeObjectDownloader takes requests for PokedexObjects and gets
    them.
    """

    def __init__(self, pokedex_requests: list, max_workers: int):
        """
        Initialize a PokeObjectDownloader.
        Note: the max threads the downloader can use is the max request
        objects it can process at a time. Each request object has a
        parameter of how many threads it can use as well (multiplying
        the threads total).
        :param pokedex_requests: list of requests
        :param max_workers: the max threads the downloader can use.
        """
        self.pokedex_requests = pokedex_requests
        self.max_workers = max_workers

    def download(self):
        """
        Processes each request in the list.
        :return: list of PokeObjects.
        """
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.max_workers) as executor:
            with requests.Session() as session:
                pokedex_maker = PokedexMaker(session)
                result = executor.map(pokedex_maker.execute_request,
                                      self.pokedex_requests)

        return list(result)


def main():
    """
    Starts the program driver.
    :return: int
    """
    driver = Driver()
    driver.start()


if __name__ == '__main__':
    main()
