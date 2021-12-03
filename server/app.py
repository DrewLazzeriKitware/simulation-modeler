import argparse
import sys
import os.path

from simput.core import ObjectManager, UIManager
from simput.ui.web import VuetifyResolver
from simput.pywebvue.modules import SimPut

from ArgumentValidator import ArgumentValidator
from SimputLoader import SimputLoader
from FileDatabase import FileDatabase
from ParflowWrapper import ParflowWrapper

from pprint import pprint  # Debug

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

import pfweb
enable_module(pfweb)

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
    "solverSearchIndex": {},
    "solverSearchIds": [],
    "simTypeShortcuts": {
        "wells": False,
        "climate": True,
        "contaminants": False,
        "saturated": "Variably Saturated",
    },
    "projGenValidation": {
        "valid": False,
        "output": "Parflow run did not validate.\nSolver.TimeStep must be type Int, found 3.14159",
    },
}

FILEDB = None
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Load Simput models and layouts
obj_manager = ObjectManager()
ui_resolver = VuetifyResolver()
ui_manager = UIManager(obj_manager, ui_resolver)
obj_manager.load_model(yaml_file=os.path.join(BASE_DIR, "model/model.yaml"))
ui_manager.load_ui(xml_file=os.path.join(BASE_DIR, "model/layout.xml"))
ui_manager.load_language(yaml_file=os.path.join(BASE_DIR, "model/model.yaml"))
ui_manager.load_language(yaml_file=os.path.join(BASE_DIR, "model/lang/en.yaml"))

# Add solver keys with search index
loader = SimputLoader(obj_manager)
solverSearchIds = loader.load_keys()
index = loader.generate_search_index()

init.update({"solverSearchIndex": index, "solverSearchIds": solverSearchIds})

# -----------------------------------------------------------------------------
# Updates
# -----------------------------------------------------------------------------
@change("dbSelectedFile")
def changeCurrentFile(dbSelectedFile, dbFiles, **kwargs):
    file_id = dbSelectedFile.get("id")

    if not file_id:
        dbSelectedFile = FILEDB.addNewEntry(dbSelectedFile)
    else:
        FILEDB.writeEntry(file_id, dbSelectedFile)

    flush_state("dbSelectedFile")
    update_state("dbSelectedFile", dbSelectedFile)
    update_state("dbFiles", FILEDB.getEntries())


@change("dbFileExchange")
def saveUploadedFile(dbFileExchange, dbSelectedFile, **kwargs):
    if dbFileExchange is not None and dbFileExchange.get("content"):
        FILEDB.writeEntryData(dbSelectedFile.get("id"), dbFileExchange["content"])


@trigger("updateFiles")
def updateFiles(update, entryId=None):
    (dbFiles, dbSelectedFile) = get_state("dbFiles", "dbSelectedFile")

    if update == "selectFile":
        if dbFiles.get(entryId):
            update_state("dbSelectedFile", FILEDB.getEntry(entryId))

    elif update == "removeFile":
        FILEDB.deleteEntry(entryId)
        del dbFiles[entryId]
        flush_state("dbFiles")

    elif update == "downloadSelectedFile":
        update_state("dbFileExchange", FILEDB.getEntryData())


@trigger("validateRun")
def validateRun():
    (work_dir,) = get_state("work_dir")
    parflow = ParflowWrapper(work_dir)
    parflow.read_from_simput(obj_manager)
    validation = parflow.validate_run()

    update_state("projGenValidation", {"output": validation, "valid": False})


def toggleDebug():
    (showDebug,) = get_state("showDebug")
    update_state("showDebug", not showDebug)


# -----------------------------------------------------------------------------
# Views
# -----------------------------------------------------------------------------
html_simput = simput.Simput(ui_manager, prefix="ab")

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
<FileDatabase 
  :files="dbFiles" 
  v-model="dbSelectedFile" 
  db-update="updateFiles" 
  v-if="currentView == 'File Database'"/> 
"""
solver = """
<Solver 
  search="solverSearchIndex" 
  ids="solverSearchIds" 
  v-if="currentView == 'Solver'"/>
"""
simulation_type = """
<SimulationType 
  :shortcuts="simTypeShortcuts"
  v-if="currentView=='Simulation Type'"/>
"""

domain = """
<Domain
  v-if="currentView=='Domain'" />
"""

boundaryConditions = """
<BoundaryConditions
  v-if="currentView=='Boundary Conditions'" />
"""

subSurface = """
<SubSurface
  v-if="currentView=='Subsurface Properties'" />
"""

projectGeneration = """
<ProjectGeneration
  :validation="projGenValidation"
  validateOn="validateRun"
  v-if="currentView=='Project Generation'" />
"""


layout.content.children += [
    Div("Debug", v_if="showDebug"),
    file_database,
    simulation_type,
    solver,
    domain,
    boundaryConditions,
    subSurface,
    projectGeneration,
]

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

    FILEDB = FileDatabase(init)

    # Begin
    layout.state = init
    start(layout)
