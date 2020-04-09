"""
This module is for showing you can use the data from a commmandline to
make an object.
"""
import argparse


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
