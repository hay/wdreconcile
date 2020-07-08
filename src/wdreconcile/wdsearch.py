import logging
import requests

ENDPOINT = "https://www.wikidata.org/w/api.php"
log = logging.getLogger(__name__)

class WikidataSearchReconciler:
    def __init__(self, language):
        self.language = language

    def search(self, q):
        log.debug(f"Searching for '{q}'")

        req = requests.get(ENDPOINT, params = {
            "action" : "wbsearchentities",
            "language" : self.language,
            "uselang" : self.language,
            "search" : q,
            "format" : "json",
            "limit" : 1
        })

        if req.status_code != 200:
            return False

        data = req.json()

        if "search" not in data:
            return False

        if len(data["search"]) < 1:
            return False

        result = data["search"][0]

        log.debug(f"Got {result['id']}")

        return {
            "id" : result["id"],
            "label" : result["label"],
            "description" : result["description"],
            "status" : "ok"
        }

    def reconcile(self, data):
        results = []

        for line in data:
            query = self.search(line)

            if query:
                query["query"] = line
            else:
                query = {
                    "status" : "error",
                    "query" : line
                }

            if query["status"] == "ok":
                print(f"{line} / {query['id']}")
            else:
                print(f"{line} / {query['status']}")

            results.append(query)

        return results