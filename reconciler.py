from dataknead import Knead
from urllib.parse import quote_plus
import json
import logging

ENDPOINT = "https://tools.wmflabs.org/wikidata-reconcile/?queries="
log = logging.getLogger(__name__)

# https://tools.wmflabs.org/wikidata-reconcile/?queries=
"""
[
    {"query"+:+"Cambridge",+"type"+:+"Q3918"},
    {"query"+:+"Oxford",+"type"+:+"Q3918"}
]
"""

class Reconciler:
    def __init__(self, in_file, type_qid):
        self.in_file = in_file
        self.type_qid = type_qid

    def construct_query(self):
        def fn(q):
            return {
                "query" : q,
                "type" : self.type_qid
            }

        self.query = Knead(self.in_file).map(fn).data()

    def do_query(self):
        query = json.dumps(self.query)
        url = ENDPOINT + quote_plus(query)
        log.debug(f"URL: {url}")
        return query

    def parse_results(self, results):
        # Define fieldnames first
        ret = [
            ["query", "qid", "score", "name", "match"]
        ]

        for index in results:
            query = self.query[int(index)]["query"]
            result_list = results[index]["result"]

            for result in result_list:
                ret.append([
                    query,
                    result["id"],
                    result["score"],
                    result["name"],
                    result["match"]
                ])

        return ret

    def reconcile(self, reconcile_data = False):
        self.construct_query()

        log.debug(f"reconcilation query: {self.query}")

        if reconcile_data:
            log.debug("Using reconcile data provided")
            results = reconcile_data
        else:
            results = self.do_query()

        return self.parse_results(results)