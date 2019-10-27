#! /usr/bin/env python3
from argparse import ArgumentParser
from dataknead import Knead
from reconciler import Reconciler
import logging
import requests
import sys

log = logging.getLogger(__name__)

def get_parser():
    parser = ArgumentParser(
        description = "Reconcile a list of strings to Wikidata items"
    )

    parser.add_argument("-i", "--input", required = True,
        help = "Input file (text, line based)"
    )

    parser.add_argument("-o", "--output", required = True,
        help = "Output file (should be a CSV"
    )

    parser.add_argument("-t", "--type", required = True,
        help = "Items should be an instance of this type"
    )

    parser.add_argument("--test-data", action = "store_true")

    parser.add_argument("-v", "--verbose", action = "store_true",
        help = "Display debug information"
    )

    return parser

def main(args):
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        log.debug("Verbose logging enabled")
        log.debug(f"Arguments given: {args}")

    if len(sys.argv) == 1:
        # No arguments, just display help
        parser.print_help()
        sys.exit()

    if ".csv" not in args.output:
        raise Exception("Output should have a .csv extension")

    reconciler = Reconciler(
        in_file = args.input,
        type_qid = args.type
    )

    if args.test_data:
        test_data = Knead("./test.json").data()
        data = reconciler.reconcile(test_data)
    else:
        data = reconciler.reconcile()

    Knead(data).write(args.output)

if __name__ == "__main__":
    try:
        parser = get_parser()
        args = parser.parse_args()
        main(args)
    except Exception as e:
        # User-caused error, just print and don't show traceback
        error(e)