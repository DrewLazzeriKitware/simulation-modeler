import argparse
import sys
import os.path

from simput.core import ProxyManager, UIManager
from simput.ui.web import VuetifyResolver
from simput.pywebvue.modules import SimPut

from ArgumentValidator import ArgumentValidator
from SimputLoader import SimputLoader
from FileDatabase import FileDatabase
from ParflowWrapper import ParflowWrapper

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
from trame.html import vuetify, Div, Span, simput

import pfweb

enable_module(pfweb)
layout = SinglePage("Parflow Web")

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
pxm = ProxyManager()
ui_resolver = VuetifyResolver()
ui_manager = UIManager(pxm, ui_resolver)
pxm.load_model(yaml_file=os.path.join(BASE_DIR, "model/model.yaml"))
ui_manager.load_ui(xml_file=os.path.join(BASE_DIR, "model/layout.xml"))
ui_manager.load_language(yaml_file=os.path.join(BASE_DIR, "model/model.yaml"))
ui_manager.load_language(yaml_file=os.path.join(BASE_DIR, "model/lang/en.yaml"))

# Add solver keys with search index
loader = SimputLoader(pxm)
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


def validateRun():
    (work_dir,) = get_state("work_dir")
    parflow = ParflowWrapper(work_dir)
    parflow.read_from_simput(pxm)
    parflow.read_from_trame(layout.state)
    validation = parflow.validate_run()

    update_state("projGenValidation", {"output": validation, "valid": False})


def toggleDebug():
    (showDebug,) = get_state("showDebug")
    update_state("showDebug", not showDebug)


# -----------------------------------------------------------------------------
# Views
# -----------------------------------------------------------------------------
html_simput = simput.Simput(ui_manager, prefix="ab")
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

domain = Div(classes="d-flex flex-column fill-height", v_if="currentView=='Domain'")
with domain:
    with vuetify.VToolbar(flat=True, classes = "fill-width align-center grey lighten-2 flex-grow-0"):
        vuetify.VToolbarTitle("Domain Parameters")
        vuetify.VSpacer()
        with vuetify.VBtnToggle(rounded=True, mandatory=True):
            with vuetify.VBtn(small=True):
                vuetify.VIcon("mdi-format-align-left", small=True, classes = "mr-1" )
                Span("Parameters")
            with vuetify.VBtn(small=True):
                vuetify.VIcon("mdi-eye", small=True, classes = "mr-1" )
                Span("Preview")
    with Div(classes="fill-height fill-width flex-grow-1"):
        vuetify.VSelect(v_model=("indicatorFile", "select file"), items=("Object.values(dbFiles)",), item_text="name", item_value="id", style=("window.coffee = this;"))

boundaryConditions = """
<BoundaryConditions
  v-if="currentView=='Boundary Conditions'" />
"""

subSurface = """
<SubSurface
  v-if="currentView=='Subsurface Properties'" />
"""

projectGeneration = Div(
    classes="d-flex flex-column fill-height justify-space-around",
    v_if="currentView=='Project Generation'",
)
with projectGeneration:
    with Div(v_if="!projGenValidation.valid", classes="mx-6"):
        with vuetify.VCard(outlined=True, classes="pa-2 my-4"):
            vuetify.VCardTitle("Run variables")
            vuetify.VTextField(v_model=("BaseUnit", 1.0), label="TimingInfo.BaseUnit")
            vuetify.VTextField(
                v_model=("DumpInterval", 1.0),
                label="TimingInfo.DumpInterval",
            )
            vuetify.VTextField(v_model=("StartCount", 0), label="TimingInfo.StartCount")
            vuetify.VTextField(v_model=("StartTime", 0.0), label="TimingInfo.StartTime")
            vuetify.VTextField(
                v_model=("StopTime", 1000.0), label="TimingInfo.StopTime"
            )
        with vuetify.VCard(dark=True, outlined=True, classes="pa-2 my-4"):
            vuetify.VCardTitle("Validation console output")
            vuetify.VDivider()
            vuetify.VTextarea(
                value=("projGenValidation.output",),
                dark=True,
                readonly=True,
                style="font-family: monospace;",
            )
        vuetify.VSpacer()

    with Div(v_if="projGenValidation.valid", classes="mx-6"):
        Span("Run Validated", classes="text-h5")
    with Div(classes="d-flex justify-end ma-6"):
        vuetify.VBtn("Validate", click=validateRun, color="primary", classes="mx-2")
        vuetify.VBtn("Generate", disabled=("!projGenValidation.valid"), color="primary")

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
