import logging
import requests

ENDPOINT = "https://www.wikidata.org/w/api.php"
log = logging.getLogger(__name__)

class WikidataFullSearchReconciler:
    def __init__(self, language, limit = 1):
        self.language = language
        self.limit = limit
        self.FIELDNAMES = ["query", "id", "label", "description", "status"]

    def format_result(self, result):
        qid = result["title"]
        log.debug(f"Got {qid}")

        # We need another call to get an actual label
        item = self.get_entity(qid)

        return {
            "id" : result["title"],
            "label" : item["label"],
            "description" : item["description"],
            "status" : "ok"
        }

    def get_entity(self, qid):
        req = requests.get(ENDPOINT, params = {
            "action" : "wbgetentities",
            "format" : "json",
            "ids" : qid,
            "props" : "labels|descriptions",
            "languages" : self.language
        })

        data = req.json()
        item = data["entities"][qid]
        ret = {
            "qid" : qid,
            "label" : None,
            "description" : None
        }

        if "labels" in item and self.language in item["labels"]:
            ret["label"] = item["labels"][self.language]["value"]

        if "descriptions" in item and self.language in item["descriptions"]:
            ret["description"] = item["descriptions"][self.language]["value"]

        return ret

    def search(self, q):
        log.debug(f"Searching for '{q}'")

        req = requests.get(ENDPOINT, params = {
            "action" : "query",
            "list" : "search",
            "srnamespace" : "0",
            "srlimit" : self.limit,
            "language" : self.language,
            "uselang" : self.language,
            "srsearch" : q,
            "format" : "json"
        })

        if req.status_code != 200:
            return False

        data = req.json()

        if "query" not in data:
            return False

        if "search" not in data["query"]:
            return False

        if len(data["query"]["search"]) == 0:
            return False

        return [self.format_result(r) for r in data["query"]["search"]]

    def reconcile(self, data):
        results = []

        for line in data:
            query = self.search(line)

            if not query:
                print(f"'{line}' gave an error")

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