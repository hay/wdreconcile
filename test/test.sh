#!/bin/bash

# First delete the old stuff
rm museums.csv
rm museum-matched.csv
rm museum-openrefine.csv
rm museums.json
rm museums-3.csv

# Then run tests
poetry run wdreconcile -i museums.txt -o museums.csv -l en
poetry run wdreconcile -i museums.txt -o museums.json -l en
poetry run wdreconcile -i museums.txt -o museums-3.csv -l en -li 3
poetry run wdreconcile -i museum-qids.csv -o museum-matched.csv -rt wdentity -l en
poetry run wdreconcile -i museums.txt -o museum-openrefine.csv -rt openrefine -l en