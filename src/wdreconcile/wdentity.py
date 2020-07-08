import logging
import requests

ENDPOINT = "https://www.wikidata.org/w/api.php"
log = logging.getLogger(__name__)

class WikidataEntityReconciler:
    def __init__(self, language):
        self.language = language

    def entity(self, q):
        log.debug(f"Searching for '{q}'")

        # https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q42&props=labels|descriptions&languages=en

        req = requests.get(ENDPOINT, params = {
            "action" : "wbgetentities",
            "languages" : self.language,
            "uselang" : self.language,
            "ids" : q,
            "format" : "json",
            "props" : "labels|descriptions"
        })

        if req.status_code != 200:
            return False

        data = req.json()

        if "entities" not in data:
            return False

        if q not in data["entities"]:
            return False

        entity = data["entities"][q]

        if "missing" in entity:
            return False

        if "labels" in entity and self.language in entity["labels"]:
            label = entity["labels"][self.language]["value"],
        else:
            label = None

        if "descriptions" in entity and self.language in entity["descriptions"]:
            description = entity["descriptions"][self.language]["value"]
        else:
            description = None

        return {
            "id" : entity["id"],
            "label" : label,
            "description" : description,
            "status" : "ok"
        }

    def reconcile(self, data):
        results = []

        for line in data:
            query = self.entity(line)

            if query:
                query["query"] = line
            else:
                query = {
                    "status" : "error",
                    "query" : line
                }

            if query["status"] == "ok":
                print(f"{line} / {query['label']}")
            else:
                print(f"{line} / {query['status']}")

            results.append(query)

        return results