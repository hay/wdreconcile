import logging
import requests
import sys

ENDPOINT = "https://www.wikidata.org/w/api.php"
log = logging.getLogger(__name__)

class WikimediaEntityReconciler:
    def __init__(self, language, site):
        self.language = language
        self.site = site
        self.FIELDNAMES = ["query", "id", "label", "description", "status"]

    def entity(self, q):
        log.debug(f"Searching for '{q}'")

        # https://www.wikidata.org/w/api.php?action=wbgetentities&languages=en&uselang=en&titles=Metropolitan+Museum+of+Art&sites=enwiki&sitefilter=enwiki&format=json&props=labels%7Cdescriptions%7Csitelinks

        req = requests.get(ENDPOINT, params = {
            "action" : "wbgetentities",
            "languages" : self.language,
            "uselang" : self.language,
            "titles" : q,
            "sites" : self.site,
            "sitefilter" : self.site,
            "format" : "json",
            "props" : "labels|descriptions|sitelinks"
        })

        if req.status_code != 200:
            return False

        data = req.json()

        if "entities" not in data:
            return False

        # This is pretty ugly
        entity = list(data["entities"].values())[0]

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