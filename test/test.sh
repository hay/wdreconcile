#!/bin/bash

# First delete the old stuff
rm output/*

# Then run tests
poetry run wdreconcile -i input/museums.txt -o output/museums.csv -l en
poetry run wdreconcile -i input/museums.txt -o output/museums.json -l en
poetry run wdreconcile -i input/museums.txt -o output/museums-3.csv -l en -li 3
poetry run wdreconcile -i input/museum-qids.csv -o output/museum-matched.csv -rt wdentity -l en
poetry run wdreconcile -i input/museums.txt -o output/museum-articles-qids.csv -rt wmentity -s enwiki -l en -v
poetry run wdreconcile -i input/museums.txt -o output/museum-openrefine.csv -rt openrefine -l en
