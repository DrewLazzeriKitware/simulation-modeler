#!/bin/bash 
SCRIPT_DIR=`dirname "$0"`
ROOT_DIR=$SCRIPT_DIR/..

/opt/paraview/bin/pvpython $SCRIPT_DIR/app.py --port 1234 --virtual-env pylib
