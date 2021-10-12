import argparse
import sys
import pfweb
import yaml
import time

from ArgumentValidator import ArgumentValidator

# -----------------------------------------------------------------------------
# Virtual Environment handling
# -----------------------------------------------------------------------------

if "--virtual-env" in sys.argv:
    virtualEnvPath = sys.argv[sys.argv.index("--virtual-env") + 1]
    virtualEnv = virtualEnvPath + "/bin/activate_this.py"
    exec(open(virtualEnv).read(), {"__file__": virtualEnv})

# -----------------------------------------------------------------------------
from trame import start, change, update_state, get_cli_parser, enable_module
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
layout.content.children += [
    '<FileDatabase :files="files" v-model="currentFileIndex" />'
]


@change("currentView")
def logView(currentView, **kwargs):
    print(currentView)


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
        "files": [
            {
                "name": "MyIndicator",
                "description": "This is my indicator. I made it. There are many like it, but this one is mine.",
                "origin": "/oldDrive/oldFolder/originalProject",
                "path": "/opt/fileDatabases/filedb1",
                "size": 672716,
                "dateCreated": time.time(),
                "dateUploaded": time.time(),
                "type": "file",
                "gridSize": [50, 50, 2],
                "category": "Indicator",
            },
            {
                "name": "Rain Forcing",
                "description": "This simulates heavy rain across the entire surface. It was made by...",
                "origin": "/oldDrive/oldFolder/otherProject",
                "path": "/opt/fileDatabases/filedb1",
                "size": 5321298,
                "dateCreated": time.time(),
                "dateUploaded": time.time(),
                "type": "zip",
                "gridSize": None,
                "category": "CLM",
            },
        ],
        "currentFileIndex": 0,
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
