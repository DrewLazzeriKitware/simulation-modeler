import argparse
import random
import yaml
import sys
import pfweb
import time
import os.path as path

from pprint import pprint
from ArgumentValidator import ArgumentValidator

from simput.core import ObjectManager, UIManager
from simput.ui.web import VuetifyResolver
from simput.pywebvue.modules import SimPut

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
from trame.html import vuetify, Div, simput


# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------
init = {
    "showDebug": False,
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
    "dbSelectedFile": None,
    "dbFileExchange": None,
    "keyIds": [],
    "solverSearchIndex": {},
    "solverSearchIds": [],
}

# Load Simput models and layouts
obj_manager = ObjectManager()
ui_resolver = VuetifyResolver()
ui_manager = UIManager(obj_manager, ui_resolver)
BASE_DIR = path.abspath(path.dirname(__file__))
obj_manager.load_model(yaml_file=path.join(BASE_DIR, "model/model.yaml"))
ui_manager.load_ui(xml_file=path.join(BASE_DIR, "model/layout.xml"))
ui_manager.load_language(yaml_file=path.join(BASE_DIR, "model/model.yaml"))
ui_manager.load_language(yaml_file=path.join(BASE_DIR, "model/lang/en.yaml"))

# Test simput
obj_manager.create("ParflowKey")
ids = list(map(lambda k: k.get("id"), obj_manager.get_type("ParflowKey")))
init.update({"keyIds": ids})

# Add search index for solver
obj = obj_manager.create("SearchKey")
obj_manager.update(
    [
        {"id": obj.get("id"), "name": "key", "value": "/Solver/Option1"},
        {"id": obj.get("id"), "name": "value", "value": "4"},
        {
            "id": obj.get("id"),
            "name": "description",
            "value": "This is the first option",
        },
    ]
)

obj = obj_manager.create("SearchKey")
obj_manager.update(
    [
        {"id": obj.get("id"), "name": "key", "value": "/Solver/Option2"},
        {"id": obj.get("id"), "name": "value", "value": "8"},
        {
            "id": obj.get("id"),
            "name": "description",
            "value": "This is the second option",
        },
    ]
)

obj = obj_manager.create("SearchKey")
obj_manager.update(
    [
        {"id": obj.get("id"), "name": "key", "value": "/Solver/Option3"},
        {"id": obj.get("id"), "name": "value", "value": "2"},
        {
            "id": obj.get("id"),
            "name": "description",
            "value": "This is the very lastoption",
        },
    ]
)


def text(key):
    props = key.get("properties")
    return props.get("description") + props.get("key")


index = {s.get("id"): text(s) for s in obj_manager.get_type("SearchKey")}
solverSearchIds = list(index.keys())
init.update({"solverSearchIndex": index, "solverSearchIds": solverSearchIds})

# -----------------------------------------------------------------------------
# Updates
# -----------------------------------------------------------------------------
def toggleDebug():
    (showDebug,) = get_state("showDebug")
    update_state("showDebug", not showDebug)


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
            update_state("dbFileExchange", selected.read())


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
# Views
# -----------------------------------------------------------------------------
html_simput = simput.Simput(ui_manager, prefix="ab")
enable_module(pfweb)

layout = SinglePage("Parflow Web")
layout.root = html_simput
layout.title.content = "Parflow Web"
layout.toolbar.children += [
    vuetify.VSpacer(),
    '<NavigationDropDown v-model="currentView" :views="views"/>',
    vuetify.VSpacer(),
    vuetify.VBtn("DEBUG", click=toggleDebug),
]
file_database = """
<FileDatabase :files="dbFiles" v-model="dbSelectedFile" db-update="updateFiles" /> 
"""
solver = """
<Solver search="solverSearchIndex" ids="solverSearchIds" />
"""
compact_styles = {
    "hide_details": True,
    "dense": True,
}


simput_test = [
    vuetify.VList(
        **compact_styles,
        children=[
            vuetify.VListItemGroup(
                color="primary",
                children=[
                    vuetify.VListItem(
                        v_for="(id, i) in keyIds",
                        key="i",
                        value=["id"],
                        children=[
                            vuetify.VListItemContent(
                                vuetify.VListItemTitle(
                                    simput.SimputItem(
                                        itemId="id",
                                    )
                                )
                            )
                        ],
                    )
                ],
            )
        ],
    )
]

layout.content.children += [Div("Debug", v_if="showDebug")]
layout.content.children += [solver]
# layout.content.children += simput_test

# -----------------------------------------------------------------------------
# Validate command line arguments and run app
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # Add our args to parser
    parser = get_cli_parser()
    parser.add_argument("-O", "--output", help="A working directory for the build")
    parser.add_argument(
        "-I", "--input", help="An existing build directory to clone"
    )  # -i taken by paraviewweb
    parser.add_argument(
        "-D", "--datastore", help="A directory for tracking simulation input files"
    )
    args = parser.parse_args()

    # Add validated args to initial state
    validator = ArgumentValidator(args)
    if not validator.args_valid():
        # Crash app and show usage
        parser.parse_args("\t")
    init.update(validator.get_args())

    # Begin
    layout.state = init
    start(layout)
