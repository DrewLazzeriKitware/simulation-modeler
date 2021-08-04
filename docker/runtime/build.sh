#!/usr/bin/env bash

SCRIPT_DIR=`dirname "$0"`
docker build -t simulation-modeler-runtime $SCRIPT_DIR
