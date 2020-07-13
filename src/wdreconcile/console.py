from . import __version__
from .reconciler import Reconciler
from argparse import ArgumentParser
from dataknead import Knead
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
        help = "Output file"
    )

    parser.add_argument("-rt", "--reconciler_type", default = "wdsearch",
        choices = ("openrefine", "wdentity", "wdsearch", "wdfullsearch"),
        help = "Reconciler type"
    )

    parser.add_argument("-l", "--language", required = True,
        help = "ISO code of the language you're using to reconcile"
    )

    parser.add_argument("-li", "--limit", default = 1,
        help = "How many results to return"
    )

    parser.add_argument("-v", "--verbose", action = "store_true",
        help = "Display debug information"
    )

    return parser

def main(args):
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        log.debug("Verbose logging enabled")
        log.debug(f"Arguments given: {args}")

    reconciler = Reconciler(
        in_file = args.input,
        out_file = args.output,
        language = args.language,
        reconciler_type = args.reconciler_type,
        limit = args.limit
    )

    reconciler.reconcile()
    reconciler.save()

def console():
    parser = get_parser()

    if len(sys.argv) == 1:
        # No arguments, just display help
        parser.print_help()
        sys.exit()

    args = parser.parse_args()
    main(args)