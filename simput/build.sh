#!/bin/bash
cd `dirname $0`
source venv/bin/activate
mkdir -p type-parflow
cp src/*.js type-parflow/
python src/model_builder.py -d parflow/pf-keys/definitions -o type-parflow
Simput compile -c type-parflow/ -o type-parflow/ -t parflow
cp type-parflow/parflow.js ../public/parflow.js
jq '' < type-parflow/model.json > type-parflow/readable.json
