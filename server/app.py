import argparse
import sys
import pfweb
import yaml

import os.path as path

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
    }

    parser = get_cli_parser()
    parser.add_argument("-I", "--input")  # -i taken by paraviewweb
    parser.add_argument("-D", "--datastore")
    parser.add_argument("-O", "--output")

    args = parser.parse_args()
    validator = ArgumentValidator(args)
    if not validator.args_valid():
        # Crash app and show usage
        parser.parse_args("--invalid-args-show-usage")

    newState.update(validator.get_args())
    layout.state = newState

    start(layout)
