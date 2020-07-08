#!/bin/bash
poetry run wdreconcile -i museums.txt -o museums.csv -rt wdsearch -l en
poetry run wdreconcile -i museums.txt -o museums.json -rt wdsearch -l en