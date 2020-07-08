import logging
import requests

ENDPOINT = "https://www.wikidata.org/w/api.php"
log = logging.getLogger(__name__)

class WikidataSearchReconciler:
    def __init__(self, language, limit = 1):
        self.language = language
        self.limit = limit
        self.FIELDNAMES = ["query", "id", "label", "description", "status"]

    def format_result(self, result):
        log.debug(f"Got {result['id']}")

        return {
            "id" : result["id"],
            "label" : result.get("label", None),
            "description" : result.get("description", None),
            "status" : "ok"
        }

    def search(self, q):
        log.debug(f"Searching for '{q}'")

        req = requests.get(ENDPOINT, params = {
            "action" : "wbsearchentities",
            "language" : self.language,
            "uselang" : self.language,
            "search" : q,
            "format" : "json",
            "limit" : self.limit
        })

        if req.status_code != 200:
            return False

        data = req.json()

        if "search" not in data:
            return False

        if len(data["search"]) < 1:
            return False

        return [self.format_result(r) for r in data["search"]]

    def reconcile(self, data):
        results = []

        for line in data:
            query = self.search(line)

            if not query:
                print(f"{line} / {query['status']}")

                results.append({
                    "status" : "error",
                    "query" : line
                })
            else:
                for item in query:
                    print(f"{line} / {item['id']}")
                    item["query"] = line
                    results.append(item)

        return results