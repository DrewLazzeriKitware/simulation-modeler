try:
    from paraview.web import venv
except:
    print("Run with pvpython for visualization support")

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


def validateRun():
    parflow = RunWriter(state.work_dir, FileDatabase())
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

simulation_type = """
<SimulationType
  :shortcuts="simTypeShortcuts"
  v-if="currentView=='Simulation Type'"/>
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

    # Init singletons
    FileDatabase(validated_args.get("datastore"))
    KeyDatabase(validated_args.get("work_dir"))
    entries = FileDatabase().getEntries()

    init.update(
        {
            **validated_args,
            "dbFiles": entries,
            "dbSelectedFile": None if not entries else list(entries.values())[0],
        }
    )

    # Compose layout which depends on databases
    html_simput = simput.Simput(
        KeyDatabase().get_ui_manager(),
        KeyDatabase().get_pdm(),
        prefix="simput",
    )
    layout.root = html_simput
    boundaryConditions = Div(
        [
            simput.SimputItem(itemId=("bcPressureId", KeyDatabase().BCPressure.id)),
            simput.SimputItem(itemId=("patchId", KeyDatabase().Patch.id)),
            simput.SimputItem(itemId=("GeomtId", KeyDatabase().GeomInput.id)),
            simput.SimputItem(itemId=("GeomInputId", KeyDatabase().GeomInput.id)),
        ],
        v_if="currentView=='Boundary Conditions'",
    )
    subSurface = Div(
        [
            simput.SimputItem(itemId=("BcPressureId", KeyDatabase().BCPressure.id)),
            simput.SimputItem(itemId=("PatchId", KeyDatabase().Patch.id)),
            simput.SimputItem(itemId=("GeomtId", KeyDatabase().GeomInput.id)),
            simput.SimputItem(itemId=("GeomInputId", KeyDatabase().GeomInput.id)),
        ],
        v_if="currentView=='Subsurface Properties'",
    )
    solver = Div(
        [simput.SimputItem(itemId=("SolverId", KeyDatabase().Solver.id))],
        v_if="currentView == 'Solver'",
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
