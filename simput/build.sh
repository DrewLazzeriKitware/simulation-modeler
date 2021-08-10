#!/bin/bash

# Run this script where it is stored
cd `dirname $0`

# Use our model building python virtualenv
source venv/bin/activate

# Make room for the simput model and copy files over
mkdir -p build
cp type-parflow/src/*.js build/

# Generate model.json from our parflow generator and keys
python parflow/pf-keys/generators/simput_model.py \
  -d parflow/pf-keys/definitions \
  -o build

# Compile model.json with other input files
Simput compile -c build -o build -t parflow

# Include the newly built module in our app
cp build/parflow.js ../public/parflow.js

# Make a debug version of the model.json
jq '' < build/model.json > build/readable.json
