import sys
import pfweb

# -----------------------------------------------------------------------------
# Virtual Environment handling
# -----------------------------------------------------------------------------

if "--virtual-env" in sys.argv:
    virtualEnvPath = sys.argv[sys.argv.index("--virtual-env") + 1]
    virtualEnv = virtualEnvPath + "/bin/activate_this.py"
    exec(open(virtualEnv).read(), {"__file__": virtualEnv})

# -----------------------------------------------------------------------------
from trame import start, change, update_state, get_app_instance
from trame.layouts import SinglePage
from trame.html import vuetify, Div

# -----------------------------------------------------------------------------
# Web App setup
# -----------------------------------------------------------------------------
app = get_app_instance()
app.enableModule(pfweb)

layout = SinglePage("Parflow Web")
layout.title.content = "Parflow Web"
layout.toolbar.children += [
    vuetify.VSpacer(),
    '<NavigationDropDown v-model="currentView" :views="views"/>',
    vuetify.VSpacer(),
]
layout.state = {
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
# -----------------------------------------------------------------------------
# Main
# /opt/paraview/bin/pvpython ./examples/.../app.py --port 1234 --virtual-env ~/Documents/code/Web/vue-py/py-lib
# -----------------------------------------------------------------------------


@change("currentView")
def logView(currentView, **kwargs):
    print(currentView)


if __name__ == "__main__":
    start(layout)
