#!/bin/bash 

PARFLOW_DIR=~/Desktop/install-parflow/opt/parflow PV_VENV=.venv pvpython server/app.py  -S share_test/ -O out_test/ -D data_test/ -i 0.0.0.0 --server
