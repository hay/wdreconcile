from .openrefine import OpenrefineReconciler
from .wdentity import WikidataEntityReconciler
from .wdsearch import WikidataSearchReconciler
from dataknead import Knead
from pathlib import Path
import logging

log = logging.getLogger(__name__)

class Reconciler:
    def __init__(self, in_file, out_file, language, reconciler_type):
        self.in_file = in_file
        self.out_file = out_file
        self.language = language
        self.results = []

        if reconciler_type == "openrefine":
            self.reconciler = OpenrefineReconciler(self.language)
        elif reconciler_type == "wdsearch":
            self.reconciler = WikidataSearchReconciler(self.language)
        elif reconciler_type == "wdentity":
            self.reconciler = WikidataEntityReconciler(self.language)

    def reconcile(self):
        data = Knead(self.in_file, read_as = "txt").data()
        log.debug(f"Got {len(data)} items")
        self.results = self.reconciler.reconcile(data)
        log.debug(f"Got {len(self.results)} results")

    def save(self):
        if Path(self.out_file).suffix == ".csv":
            Knead(self.results).write(
                self.out_file,
                fieldnames = ["query", "id", "label", "description", "status"]
            )
        else:
            Knead(self.results).write(self.out_file)

        print(f"Written to '{self.out_file}'")

