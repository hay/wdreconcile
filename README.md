# wdreconcile.py
> Map strings to Wikidata QID's using various methods

This is a **work-in-progress** Python command-line tool to align strings to Wikidata items (QID's).

## Install
Clone this repo and use [poetry](https://python-poetry.org/) to install dependencies:

```bash
poetry install
```

Then run `poetry run wdreconcile`.

## Usage

### Using the search reconciler
Create a text file with strings you want to reconcile, separated by newline. E.g.

`museums.txt`
```csv
Metropolitan Museum of Art
Centraal Museum
Jewish Historical Museum
```

By default `wbsearch.py` uses the `wdsearch` reconciler. This gives you back the very first result from the the `wbsearchentities` Wikidata API. This is the same as what you get when using the autocomplete field on the website. You **need** to specify a language in ISO-code form (e.g. `en`)

```bash
poetry run wdreconcile -i museums.txt -o museums.csv -l en
```

This will give you back a filed called `museums.csv` that looks like this:

|query|id|label|description|status|
|-----|--|-----|-----------|------|
|Metropolitan Museum of Art|Q160236|Metropolitan Museum of Art|major art museum in New York City, United States|ok|
|Centraal Museum|Q260913|Centraal Museum|museum in Utrecht, Netherlands|ok|
|Jewish Historical Museum|Q702726|Jewish Historical Museum|Jewish history, culture, and religion museum in Amsterdam, Netherlands|ok|

Note that the `output format` (`-o`) can have any extension that [dataknead](https://github.com/hay/dataknead) supports, so to use `json`, just run the command like this:
```bash
poetry run wdreconcile -i museums.txt -o museums.json -l en
```

If you want more than the first result you can use the `-li` (limit) parameter to change the number of results.

```bash
poetry run wdreconcile -i museums.txt -o museums-3.csv -l en -li 3
```

You can also use the Wikidata fulltext search, which will give you the same results as the [Special:Search](https://www.wikidata.org/wiki/Special:Search) page. Specify `wdfullsearch` using the `-rt` argument. The `wdfullsearch` reconciler is about half as slow as the default `wdsearch` reconciler.

```bash
poetry run wdreconcile -i museums.txt -o museums.csv -l en -rt wdfullsearch
```

And you can also use the [Wikidata reconciler as used by OpenRefine](https://wdreconcile.toolforge.org/), using the `-rt` (reconciler type) parameter.

```bash
poetry run wdreconcile -i museums.txt -o museum-openrefine.csv -rt openrefine -l en
```

### Lookup labels/descriptions by qid
Another use of `wdreconcile` is to map back QID's to labels and descriptions using the `wdentity` reconciler. This will also check if the item exists and might be handy for batch checking of existing QID's.

```bash
poetry run wdreconcile -i museum-qids.csv -o museum-matched.csv -rt wdentity -l en
```

### Lookup QIDs by Wikimedia page title
You can also go from Wikimedia project pages (like articles on Wikipedia) to QIDs using the `wmentity` reconciler type. This will also check for existence of the page title. This requires the `-s` (site) argument, which is the projectname like `enwiki`, `commonswiki` or `eswikinews`. For a full list of all possible sites see the [API docs](https://www.wikidata.org/w/api.php?action=help&modules=wbgetentities).

```bash
poetry run wdreconcile -i museums.txt -o museum-articles-qids.csv -rt wmentity -s enwiki -l en -v
```

## Reconcilers
Here are all reconcilers in a handy table:

| id | name | usage |
| -- | ---- | ----- |
| `openrefine` | OpenRefine reconcilation | This is the [OpenRefine Wikidata reconcilation service](https://wikidata.reconci.link/) |
| `wdentity` | Wikidata Entity | This will map QID's to their respective labels and descriptions and check for existence |
| `wdsearch` | Wikidata Search | This uses the first result from the `wbsearchentities` API, which is equivalent to the 'autocomplete' box on the Wikidata site. **This is the default**. |
| `wdfullsearch` | Wikidata Fullsearch | This uses the regular Wikidata [[search engine](https://www.wikidata.org/wiki/Special:Search)]. About half as slow as `wdsearch` |
| `wmentity` | Wikimedia Entity | This maps page titles from a Wikimedia project to their respective QIDs. |

## Troubleshooting
If you add the `-v` (verbose) flag `wdreconcile` will give much more debug information.

## All options
```bash
usage: wdreconcile [-h] -i INPUT -o OUTPUT
                   [-rt {openrefine,wdentity,wdsearch,wdfullsearch,wmentity}]
                   -l LANGUAGE [-li LIMIT] [-s SITE] [-v]

Reconcile a list of strings to Wikidata items

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file (text, line based)
  -o OUTPUT, --output OUTPUT
                        Output file
  -rt {openrefine,wdentity,wdsearch,wdfullsearch,wmentity}, --reconciler_type {openrefine,wdentity,wdsearch,wdfullsearch,wmentity}
                        Reconciler type
  -l LANGUAGE, --language LANGUAGE
                        ISO code of the language you're using to reconcile
  -li LIMIT, --limit LIMIT
                        How many results to return
  -s SITE, --site SITE  Site (like enwiki)
  -v, --verbose         Display debug information
 ```

## License
MIT &copy; [Hay Kranen](http://www.haykranen.nl)