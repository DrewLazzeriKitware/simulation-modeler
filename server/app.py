import argparse
import sys
import os.path
import yaml

from CommandValidator import CommandValidator
from FileDatabase import FileDatabase
from SimulationManager import SimulationManager

from parflowio.pyParflowio import PFData

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
    trigger,
    get_state,
    flush_state,
)
from trame.layouts import SinglePage
from trame.html import vuetify, Div, Span, simput, Element
import widgets

from simput.core import ProxyManager, UIManager, ProxyDomainManager
from simput.ui.web import VuetifyResolver
from simput.domains import register_domains
from simput.values import register_values

register_domains()
register_values()
layout = SinglePage("Parflow Web")

# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------
init = {
    "showDebug": False,
    "currentView": "Solver",
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
    "dbSelectedFile": {},
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
pdm = ProxyDomainManager()
pxm.add_life_cycle_listener(pdm)
pxm.load_model(yaml_file=os.path.join(BASE_DIR, "model/model.yaml"))
ui_manager.load_ui(xml_file=os.path.join(BASE_DIR, "model/layout.xml"))
ui_manager.load_language(yaml_file=os.path.join(BASE_DIR, "model/model.yaml"))
ui_manager.load_language(yaml_file=os.path.join(BASE_DIR, "model/lang/en.yaml"))

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


@change("indicatorFile")
def updateComputationalGrid(indicatorFile, **kwargs):
    entry = FILEDB.getEntry(indicatorFile)
    update_state("indicatorFileDescription", entry.get("description"))

    filename = FILEDB.getEntryPath(indicatorFile)
    try:
        handle = PFData(filename)
    except:
        print(f"Could not find pfb: {filename}")
    handle.loadHeader()

    update_state("NX", handle.getNX())
    update_state("NY", handle.getNY())
    update_state("NZ", handle.getNZ())

    update_state("LX", handle.getX())
    update_state("LY", handle.getY())
    update_state("LZ", handle.getZ())

    update_state("DX", handle.getDX())
    update_state("DY", handle.getDY())
    update_state("DZ", handle.getDZ())


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
    parflow = SimulationManager(work_dir, FILEDB)
    parflow.read_from_simput(pxm)
    validation = parflow.validate_run()

    update_state("projGenValidation", {"output": validation, "valid": False})


def toggleDebug():
    (showDebug,) = get_state("showDebug")
    update_state("showDebug", not showDebug)


def saveSimput():
    (work_dir,) = get_state("work_dir")
    settings_path = os.path.join(work_dir, "pf_settings.yaml")
    with open(settings_path, "r+") as settings_file:
        settings = yaml.safe_load(settings_file)
        settings["save"] = pxm.save()
        yaml.dump(settings, settings_file)


def initSimputModel(work_dir):
    settings_path = os.path.join(work_dir, "pf_settings.yaml")
    with open(settings_path, "r") as settings_file:
        settings = yaml.safe_load(settings_file)

    grid_id = None
    solver_id = None

    # Either load from previous save or instantiate models
    if settings.get("save"):
        pxm.load(file_content=settings.get("save"))
        [grid] = pxm.get_instances_of_type("Grid")
        [solver] = pxm.get_instances_of_type("Solver")
        grid_id = grid.id
        solver_id = solver.id
    else:
        # Add solver keys with search index
        grid_id = pxm.create("Grid").id
        solver_id = pxm.create("Solver").id

    init.update(
        {
            "simputDomainId": grid_id,
            "simputSolverId": solver_id,
        }
    )


# -----------------------------------------------------------------------------
# Views
# -----------------------------------------------------------------------------
html_simput = simput.Simput(ui_manager, proxy_domain_manager=pdm, prefix="simput")
layout.root = html_simput
layout.title.set_text("Parflow Web")
layout.toolbar.children += [
    vuetify.VSpacer(),
    widgets.NavigationDropDown(v_model="currentView", views=("views",)),
    vuetify.VSpacer(),
    Span("Simput", classes="text mx-1"),
    vuetify.VBtn("Save", click=saveSimput, classes="mx-1"),
    vuetify.VSpacer(),
    vuetify.VBtn("DEBUG", click=toggleDebug),
]

file_database = widgets.FileDatabase(
    files=("dbFiles",),
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

domain = widgets.Domain(
    selected_file_model="indicatorFile",
    grid_models={
        key: key for key in ["LX", "DX", "NX", "LY", "DY", "NY", "LZ", "DZ", "NZ"]
    },
)

boundaryConditions = """
    <BoundaryConditions
      v-if="currentView=='Boundary Conditions'" />
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

layout.content.children += [
    Div("{{simputDomainId}}", v_if="showDebug"),
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
    parser.add_argument(
        "-O", "--output", help="A working directory for the build", required=True
    )
    parser.add_argument(
        "-I", "--input", help="An existing build directory to clone"
    )  # -i taken by paraviewweb
    parser.add_argument(
        "-D", "--datastore", help="A directory for tracking simulation input files"
    )
    args = parser.parse_args()

    # Add validated args to initial state
    validator = CommandValidator(args)
    if not validator.args_valid():
        parser.print_help(sys.stderr)
    validated_args = validator.get_args()
    FILEDB = FileDatabase(validated_args)
    entries = FILEDB.getEntries()

    init.update(
        {
            **validated_args,
            "dbFiles": entries,
            "dbSelectedFile": {} if not entries else list(entries.values())[0],
        }
    )

    initSimputModel(validated_args["work_dir"])

    # Begin
    layout.state = init
    # validateRun()  # For validating without ui
    start(layout)
