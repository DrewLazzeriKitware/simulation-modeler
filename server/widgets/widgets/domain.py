from paraview import simple

from trame import state
from trame.html import vuetify, Element, Div, Span, paraview

from parflow import Run

from visualizations.image import SourceImage
from visualizations.soil import SoilVisualization
from FileDatabase import FileCategories, get_filedb_instance

state.update({
    "domainView": "grid",
    "soils": [],
    "currentSoil": "all",
    "terrainFile": None,
    "indicatorFile": None,
})

view = simple.GetRenderView()
html_view = paraview.VtkRemoteView(view)
soil_viz = None

@state.change("currentSoil")
def updateCurrentSoil(currentSoil, **kwargs):
    if soil_viz is None:
        return

    if currentSoil == "all":
        soil_viz.setSoilVisualizationMode("all")
    else:
        value = soil_viz.soilTypes[currentSoil]["value"]
        soil_viz.setSoilVisualizationMode("selection")
        soil_viz.activateSoil(value)

    html_view.update()

@state.change("domainView")
def on_view_change(domainView, indicatorFile, terrainFile, **kwargs):
    global soil_viz

    if domainView == "grid":
        if soil_viz is not None:
            pass

    elif domainView == "viz":
        if indicatorFile is None or terrainFile is None:
            state.domainView = "grid"
            return

        indicatorFilePath = get_filedb_instance().getEntryPath(indicatorFile)
        terrainFilePath = get_filedb_instance().getEntryPath(terrainFile)

        if indicatorFilePath is not None and terrainFilePath is not None:
            if soil_viz is None:
                configFile = "LW_Test/LW_Test.pfidb"
                parflowConfig = Run.from_definition(configFile)
                parflowImage = SourceImage(parflowConfig, terrainFilePath)
                soil_viz = SoilVisualization(view, parflowImage, parflowConfig)

            soil_viz.indicatorFilename = indicatorFilePath
            soil_viz.parflowImage.elevationFilter.demFilename = terrainFilePath
            soil_viz.activate()

            state.update({
                "soils": ["all"] + list(soil_viz.soilTypes.keys())
            })


def domain_viz():
    return [
        vuetify.VSelect(
            label="Current Soil",
            v_model=("currentSoil",),
            items=("soils",),
        ),
        html_view,
    ]

def domain_parameters(grid_models):
    domainGridRow = vuetify.VRow(classes="ma-6 justify-space-between")
    domainGrid = [Element("H1", "Indicator"), domainGridRow]
    with domainGridRow:
        with Div():
            vuetify.VSelect(
                v_model=("indicatorFile", None),
                placeholder="Select an indicator file",
                items=(f"dbFilesCategoryLookup['{FileCategories.Indicator}']",),
                item_text="name",
                item_value="id",
            )

            with vuetify.VRow():
                with vuetify.VCol():
                    vuetify.VTextField(
                        v_model=(grid_models["LX"], 1.0), label="lx", readonly=True
                    )
                    vuetify.VTextField(
                        v_model=(grid_models["DX"], 1.0), label="dx", readonly=True
                    )
                    vuetify.VTextField(
                        v_model=(grid_models["NX"], 1.0), label="nx", readonly=True
                    )
                with vuetify.VCol():
                    vuetify.VTextField(
                        v_model=(grid_models["LY"], 1.0), label="ly", readonly=True
                    )
                    vuetify.VTextField(
                        v_model=(grid_models["DY"], 1.0), label="dy", readonly=True
                    )
                    vuetify.VTextField(
                        v_model=(grid_models["NY"], 1.0), label="ny", readonly=True
                    )
                with vuetify.VCol():
                    vuetify.VTextField(
                        v_model=(grid_models["LZ"], 1.0), label="lz", readonly=True
                    )
                    vuetify.VTextField(
                        v_model=(grid_models["DZ"], 1.0), label="dz", readonly=True
                    )
                    vuetify.VTextField(
                        v_model=(grid_models["NZ"], 1.0), label="nz", readonly=True
                    )

        with Div(classes="ma-6"):
            Span("Lorem Ipsum documentation for Indicator file")
            vuetify.VTextarea(
                v_if="indicatorFileDescription",
                value=("indicatorFileDescription", ""),
                readonly=True,
                style="font-family: monospace;",
            )

    return domainGrid

def terrain_parameters():
    domainGridRow = vuetify.VRow(classes="ma-6 justify-space-between")
    domainGrid = [Element("H1", "Terrain"), domainGridRow]
    with domainGridRow:
        with Div():
            vuetify.VSelect(
                v_model=("terrainFile",),
                placeholder="Select a terrain file",
                items=(f"dbFilesCategoryLookup['{FileCategories.Terrain}']",),
                item_text="name",
                item_value="id",
            )

    return domainGrid


# TODO Unpythonic
# How does python parameterize an instance?
def domain(grid_models):
    domainGrid = domain_parameters(grid_models)
    terrainGrid = terrain_parameters()
    domainViz = domain_viz()

    element = Div(
        classes="d-flex flex-column fill-height", v_if="currentView=='Domain'"
    )

    with element:
        with vuetify.VToolbar(
            flat=True, classes="fill-width align-center grey lighten-2 flex-grow-0"
        ):
            vuetify.VToolbarTitle("Domain Parameters")
            vuetify.VSpacer()
            with vuetify.VBtnToggle(rounded=True, mandatory=True, v_model=("domainView",)):
                with vuetify.VBtn(small=True, value="grid"):
                    vuetify.VIcon("mdi-format-align-left", small=True, classes="mr-1")
                    Span("Parameters")
                with vuetify.VBtn(small=True, value="viz", disabled=("!indicatorFile || !terrainFile",)):
                    vuetify.VIcon("mdi-eye", small=True, classes="mr-1")
                    Span("Preview")
        Div(
            v_if="domainView=='grid'",
            children=domainGrid + terrainGrid,
            classes="fill-height fill-width flex-grow-1 ma-6",
        )

        vuetify.VContainer(
            v_if="domainView=='viz'",
            fluid=True,
            classes="pa-0 fill-height",
            children=domainViz
        )
    return element
