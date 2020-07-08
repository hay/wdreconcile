from dataknead import Knead
from urllib.parse import quote_plus
import json
import logging
import requests

log = logging.getLogger(__name__)

# https://tools.wmflabs.org/wikidata-reconcile/?queries=
"""
[
    {"query"+:+"Cambridge",+"type"+:+"Q3918"},
    {"query"+:+"Oxford",+"type"+:+"Q3918"}
]
"""

class OpenrefineReconciler:
    def __init__(self, language):
        self.language = language
        self.endpoint = f"https://wdreconcile.toolforge.org/{self.language}/api"

    def construct_query(self, data):
        query = {}
        log.debug(f"Got {len(data)} items")

        for index, line in enumerate(data):
            query[index] = {
                "query" : line
            }

        return query

    def do_query(self):
        log.debug(f"Doing a request: {self.endpoint}")
        query = 'queries=' + json.dumps(self.query)
        print(self.endpoint, query)
        req = requests.post(self.endpoint, data = query)
        log.debug("Done")

        if req.status_code != 200:
            d = req.json()
            msg = f"ERROR {req.status_code} - {d['message']} : {d['details']}"
            raise Exception(msg)
        else:
            return req.json()

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
                    result.get("name", None),
                    result["match"]
                ])

        return ret

    def reconcile(self, data):
        self.query = self.construct_query(data)

        log.debug(f"reconcilation query: {self.query}")
        results = self.do_query()
        return self.parse_results(results)