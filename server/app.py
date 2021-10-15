import argparse
import random
import yaml
import sys
import pfweb
import time
import os.path as path

from pprint import pprint
from ArgumentValidator import ArgumentValidator

# -----------------------------------------------------------------------------
# Virtual Environment handling
# -----------------------------------------------------------------------------

if "--virtual-env" in sys.argv:
    virtualEnvPath = sys.argv[sys.argv.index("--virtual-env") + 1]
    virtualEnv = virtualEnvPath + "/bin/activate_this.py"
    exec(open(virtualEnv).read(), {"__file__": virtualEnv})

# -----------------------------------------------------------------------------
from trame import (
    start,
    change,
    update_state,
    get_cli_parser,
    enable_module,
    trigger,
    get_state,
    flush_state,
)
from trame.layouts import SinglePage
from trame.html import vuetify, Div

# -----------------------------------------------------------------------------
# Web App setup
# -----------------------------------------------------------------------------
enable_module(pfweb)

layout = SinglePage("Parflow Web")
layout.title.content = "Parflow Web"
layout.toolbar.children += [
    vuetify.VSpacer(),
    '<NavigationDropDown v-model="currentView" :views="views"/>',
    vuetify.VSpacer(),
]
file_database = """
<FileDatabase :files="dbFiles" v-model="dbSelectedFile" db-update="updateFiles" /> 
"""
layout.content.children += [file_database]


@change("currentView")
def logView(currentView, **kwargs):
    pprint(currentView)


@trigger("updateFiles")
def updateFiles(update, fileId=None):
    (dbFiles, dbSelectedFile) = get_state("dbFiles", "dbSelectedFile")

    if update == "selectFile":
        if dbFiles.get(fileId):
            update_state("dbSelectedFile", dbFiles[fileId])
    elif update == "removeFile":
        del dbFiles[fileId]
        flush_state("dbFiles")
    elif update == "downloadSelectedFile":
        with open(dbSelectedFile.get("path"), "rb") as selected:
            update_state("dbFileExchange", dbSelectedFile.selected.read())
    elif update == "resetSelectedFile":
        print(dbSelectedFile)
        flush_state("dbSelectedFile")


@change("dbSelectedFile")
def changeCurrentFile(dbSelectedFile, work_dir, dbFiles, dbFileExchange, **kwargs):

    # This might be a new file
    file_id = dbSelectedFile.get("id")
    if not file_id:
        file_id = work_dir + str(random.getrandbits(32))
        dbSelectedFile = {**dbSelectedFile, "id": file_id, "path": file_id}

    update_state("dbSelectedFile", dbSelectedFile)
    newFiles = {**dbFiles, file_id: dbSelectedFile}
    update_state("dbFiles", newFiles)

    # Update File Database
    with open(path.join(work_dir, "pf_datastore.yaml"), "w") as db:
        yaml.dump(newFiles, db)


@change("dbFileExchange")
def changeFileExchange(dbFileExchange, dbSelectedFile, **kwargs):

    # Update on disk if updated in shared state
    if dbFileExchange is not None and dbFileExchange.get("content"):
        with open(dbSelectedFile.get("path"), "wb") as selected:
            selected.write(dbFileExchange["content"])


# -----------------------------------------------------------------------------
# Main
# /opt/paraview/bin/pvpython ./examples/.../app.py --port 1234 --virtual-env ~/Documents/code/Web/vue-py/py-lib
# -----------------------------------------------------------------------------


if __name__ == "__main__":
    newState = {
        "currentView": "File Database",
        "views": [
            "File Database",
            "Simulation Type",
            "Domain",
            "Boundary Conditions",
            "Subsurface Properties",
            "Solver",
            "Project Generation",
        ],
        "dbFiles": {},
        ##"dbFiles": {
        ##    "key1": {
        ##        "name": "MyIndicator",
        ##        "description": "This is my indicator. I made it. There are many like it, but this one is mine.",
        ##        "origin": "/oldDrive/oldFolder/originalProject",
        ##        "path": "/opt/fileDatabases/filedb1",
        ##        "size": 672716,
        ##        "dateModified": time.time(),
        ##        "dateUploaded": time.time(),
        ##        "type": "file",
        ##        "gridSize": [50, 50, 2],
        ##        "category": "Indicator",
        ##    },
        ##    "key2": {
        ##        "name": "Rain Forcing",
        ##        "description": "This simulates heavy rain across the entire surface. It was made by...",
        ##        "origin": "/oldDrive/oldFolder/otherProject",
        ##        "path": "/opt/fileDatabases/filedb1",
        ##        "size": 5321298,
        ##        "dateModified": time.time(),
        ##        "dateUploaded": time.time(),
        ##        "type": "zip",
        ##        "gridSize": None,
        ##        "category": "CLM",
        ##    },
        ##},
        "dbSelectedFile": None,
        "dbFileExchange": None,
    }

    parser = get_cli_parser()
    parser.add_argument("-O", "--output", help="A working directory for the build")
    parser.add_argument(
        "-I", "--input", help="An existing build directory to clone"
    )  # -i taken by paraviewweb
    parser.add_argument(
        "-D", "--datastore", help="A directory for tracking simulation input files"
    )

    args = parser.parse_args()
    validator = ArgumentValidator(args)
    if not validator.args_valid():
        # Crash app and show usage
        parser.parse_args("\t")

    newState.update(validator.get_args())
    layout.state = newState

    start(layout)
