#!/bin/bash 
# SCRIPT_DIR=`dirname "$0"`
# ROOT_DIR=$SCRIPT_DIR/..
#/opt/paraview/bin/pvpython $SCRIPT_DIR/app.py --port 1234 --virtual-env pylib

PARFLOW_DIR=~/Desktop/install-parflow/opt/parflow python server/app.py -O out_test/ -i 0.0.0.0 -D out_test/ --server

