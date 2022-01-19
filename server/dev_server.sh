#!/bin/bash 

PARFLOW_DIR=~/Desktop/install-parflow/opt/parflow PV_VENV=.venv pvpython server/app.py  -S share/ -O out/ -D data/ -i 0.0.0.0 --server
