"""
This module is for showing you can use the data from a commmandline to
make an object.
"""
import argparse


class Request:
    """
    Request has the values needed to make a request to get pokemon data.
    """

    def __init__(self, mode: str, input_data: str, expanded: bool,
                 input_file: str = None, output_file: str = None):
        """
        Initialize a request.
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
        return f'current state of Request={str(vars(self))}'


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
        req = Request(**kwarg)
        return req


def main():
    """
    Prints the object created from cmdline args.
    :return:
    """
    print(ArgumentParser.setup_commandline_request())


if __name__ == '__main__':
    main()
