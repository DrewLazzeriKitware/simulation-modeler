from paraview.web import venv

import argparse
import sys
import os.path
import yaml

from CommandValidator import CommandValidator
from FileDatabase import FileCategories, FileDatabase, file_category_label
from KeyDatabase import KeyDatabase
from RunWriter import RunWriter

from parflowio.pyParflowio import PFData

from trame import (
    start,
    get_cli_parser,
    trigger,
    state,
    controller as ctrl,
)
from trame.layouts import SinglePage
from trame.html import vuetify, Span, simput, Div

import widgets

FILEDB = None
KEYDB = None

layout = SinglePage("Parflow Web")
layout.logo.click = "$refs.view.resetCamera()"

# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------
init = {
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
    "fileCategories": [
        {"value": cat.value, "text": file_category_label(cat)} for cat in FileCategories
    ],
    "uploadError": "",
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


# -----------------------------------------------------------------------------
# Updates
# -----------------------------------------------------------------------------
@state.change("dbSelectedFile")
def changeCurrentFile(dbSelectedFile, dbFiles, **kwargs):
    if dbSelectedFile is None:
        return

    file_id = dbSelectedFile.get("id")

    if not file_id:
        dbSelectedFile = FILEDB.addNewEntry(dbSelectedFile)
    else:
        currentEntry = FILEDB.getEntry(file_id)
        dbSelectedFile = {**currentEntry, **dbSelectedFile}
        FILEDB.writeEntry(file_id, dbSelectedFile)

    state.dbSelectedFile = dbSelectedFile
    state.flush("dbSelectedFile")
    state.dbFiles = FILEDB.getEntries()


@state.change("indicatorFile")
def updateComputationalGrid(indicatorFile, **kwargs):
    entry = FILEDB.getEntry(indicatorFile)
    state.indicatorFileDescription = entry.get("description")

    filename = FILEDB.getEntryPath(indicatorFile)
    try:
        handle = PFData(filename)
    except:
        print(f"Could not find pfb: {filename}")
    handle.loadHeader()

    state.NX = handle.getNX()
    state.NY = handle.getNY()
    state.NZ = handle.getNZ()

    state.LX = handle.getX()
    state.LY = handle.getY()
    state.LZ = handle.getZ()

    state.DX = handle.getDX()
    state.DY = handle.getDY()
    state.DZ = handle.getDZ()


@state.change("dbFileExchange")
def saveUploadedFile(dbFileExchange=None, dbSelectedFile=None, sharedir=None, **kwargs):
    if dbFileExchange is None or dbSelectedFile is None or sharedir is None:
        return

    fileMeta = {
        key: dbFileExchange.get(key)
        for key in ["origin", "size", "dateModified", "dateUploaded", "type"]
    }
    entryId = dbSelectedFile.get("id")

    try:
        # File was uploaded from the user browser
        if dbFileExchange.get("content"):
            FILEDB.writeEntryData(entryId, dbFileExchange["content"])
        # Path to file already present on the server was specified
        elif dbFileExchange.get("localFile"):
            file_path = os.path.abspath(
                os.path.join(sharedir, dbFileExchange.get("localFile"))
            )
            if os.path.commonpath([sharedir, file_path]) != sharedir:
                raise Exception("Attempting to access a file outside the sharedir.")
            fileMeta["origin"] = os.path.basename(file_path)

            with open(file_path, "rb") as f:
                content = f.read()
                fileMeta["size"] = len(content)
                FILEDB.writeEntryData(entryId, content)
    except Exception as e:
        print(e)
        state.uploadError = "An error occurred uploading the file to the database."
        return

    entry = {**FILEDB.getEntry(entryId), **fileMeta}
    FILEDB.writeEntry(entryId, entry)
    state.dbSelectedFile = entry
    state.flush("dbSelectedFile")


@trigger("updateFiles")
def updateFiles(update, entryId=None):
    if update == "selectFile":
        if state.dbFiles.get(entryId):
            state.dbSelectedFile = FILEDB.getEntry(entryId)

    elif update == "removeFile":
        FILEDB.deleteEntry(entryId)
        state.dbFiles = FILEDB.getEntries()
        if entryId == state.dbSelectedFile.get("id"):
            state.dbSelectedFile = None
            state.flush("dbSelectedFile")
        state.flush("dbFiles")

    elif update == "downloadSelectedFile":
        state.dbFileExchange = FILEDB.getEntryData(entryId)

    state.uploadError = ""


def validateRun():
    parflow = RunWriter(state.work_dir, FILEDB)
    validation = parflow.validate_run()

    state.projGenValidation = {"output": validation, "valid": False}


# -----------------------------------------------------------------------------
# Views
# -----------------------------------------------------------------------------
layout.title.set_text("Parflow Web")
layout.toolbar.children += [
    vuetify.VSpacer(),
    widgets.NavigationDropDown(v_model="currentView", views=("views",)),
    vuetify.VSpacer(),
    Span("Simput", classes="text mx-1"),
    vuetify.VBtn("Save", click=ctrl.saveSimput, classes="mx-1"),
]

file_database = widgets.FileDatabase(
    files=("dbFiles",),
    fileCategories=("fileCategories",),
    error=("uploadError",),
    db_update="updateFiles",
    v_model="dbSelectedFile",
    v_if="currentView == 'File Database'",
)

solver = """
<SimputItem
  v-if="currentView == 'Solver'"
  :itemId="simputSolverId"
  />
"""

simulation_type = """
<SimulationType
  :shortcuts="simTypeShortcuts"
  v-if="currentView=='Simulation Type'"/>
"""

subSurface = """
<SubSurface
  v-if="currentView=='Subsurface Properties'" />
"""

projectGeneration = widgets.ProjectGeneration(
    validation_callback=validateRun,
    validation_output="projGenValidation.output",
    validation_check="!projGenValidation.valid",
    run_variables={
        key: key
        for key in ["BaseUnit", "DumpInterval", "StartCount", "StartTime", "StopTime"]
    },
)


# -----------------------------------------------------------------------------
# Validate command line arguments and run app
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # Add our args to parser
    parser = get_cli_parser()
    parser.add_argument(
        "-O", "--output", help="A working directory for the build", required=True
    )
    parser.add_argument(
        "-I", "--input", help="An existing build directory to clone"
    )  # -i taken by paraviewweb
    parser.add_argument(
        "-D",
        "--datastore",
        help="A directory for tracking simulation input files",
        required=True,
    )
    parser.add_argument(
        "-S",
        "--sharedir",
        help="A shared directory whose files can be selected from the client",
        required=True,
    )
    args = parser.parse_args()

    # Add validated args to initial state
    validator = CommandValidator(args)
    if not validator.args_valid():
        parser.print_help(sys.stderr)
    validated_args = validator.get_args()
    FILEDB = FileDatabase(validated_args.get("datastore"))
    KEYDB = KeyDatabase(validated_args.get("work_dir"))
    entries = FILEDB.getEntries()

    init.update(
        {
            **validated_args,
            "dbFiles": entries,
            "dbSelectedFile": None if not entries else list(entries.values())[0],
        }
    )

    # Compose layout which depends on databases
    html_simput = simput.Simput(
        KEYDB.get_ui_manager(),
        KEYDB.get_pdm(),
        prefix="simput",
    )
    layout.root = html_simput
    boundaryConditions = Div(
        [
            simput.SimputItem(itemId=("bcPressureId", KEYDB.BCPressure.id)),
            simput.SimputItem(itemId=("patchId", KEYDB.Patch.id)),
        ],
        v_if="currentView=='Boundary Conditions'",
    )
    layout.content.children += [
        file_database,
        simulation_type,
        solver,
        widgets.Domain(),
        boundaryConditions,
        subSurface,
        projectGeneration,
    ]

    # Begin
    layout.state = init
    # validateRun()  # For validating without ui
    # print(layout.html) # Debugging
    start(layout)
