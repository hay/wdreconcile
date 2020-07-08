# wdreconcile.py
> Map strings to Wikidata QID's using various methods

This is a **work-in-progress** Python command-line tool to align strings to Wikidata items (QID's).

## Install
Right now you need to clone or download this repo.

In the future i'll make a `pyproject.toml` file for easy installation, for now you need these two dependencies:

```bash
pip install dataknead requests
```

## Usage

### Using the search reconciler
Create a text file with strings you want to reconcile, separated by newline. E.g.

`museums.txt`
```csv
Metropolitan Museum of Art
Centraal Museum
Jewish Historical Museum
```

Currently the `wdsearch` reconciler is the most reliable, it gives you back the very first result from the the `wbsearchentities` Wikidata API. This is the same as what you get when using the autocomplete field on the website. You **need** to specify a language in ISO-code form (e.g. `en`)

```bash
wdreconcile.py -i museums.txt -o museums.csv -rt wdsearch -l en
```

This will give you back a filed called `museums.csv` that looks like this:

|query|id|label|description|status|
|-----|--|-----|-----------|------|
|Metropolitan Museum of Art|Q160236|Metropolitan Museum of Art|"major art museum in New York City| United States"|ok|
|Centraal Museum|Q260913|Centraal Museum|"museum in Utrecht| Netherlands"|ok|
|Jewish Historical Museum|Q702726|Jewish Historical Museum|"Jewish history| culture| and religion museum in Amsterdam| Netherlands"|ok|

Note that the `output format` (`-o`) can have any extension that [dataknead](https://github.com/hay/dataknead) supports, so to use `json`, just run the command like this:
```bash
wdreconcile.py -i museums.txt -o museums.json -rt wdsearch -l en
```

### Lookup labels/descriptions by qid
Another use of `wdreconcile` is to map back QID's to labels and descriptions using the `wdentity` reconciler. This will also check if the item exists and might be handy for batch checking of existing QID's.

```bash
wdreconcile.py -i museum-qids.csv -o museum-matched.csv -rt wdentity -l en
```

### Using the `openrefine` reconciler type
This still work in progress and might not work, but you can try it using `-rt openrefine`.

## Troubleshooting
If you add the `-v` (verbose) flag `wdreconcile` will give much more debug information.

## All options
```bash
usage: wdreconcile.py [-h] -i INPUT -o OUTPUT -rt
                      {openrefine,wdentity,wdsearch} -l LANGUAGE [-v]

Reconcile a list of strings to Wikidata items

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file (text, line based)
  -o OUTPUT, --output OUTPUT
                        Output file
  -rt {openrefine,wdentity,wdsearch}, --reconciler_type {openrefine,wdentity,wdsearch}
                        Reconciler type
  -l LANGUAGE, --language LANGUAGE
                        ISO code of the language you're using to reconcile
  -v, --verbose         Display debug information
 ```

## License
MIT &copy; [Hay Kranen](http://www.haykranen.nl)