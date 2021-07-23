from paraview import simple
from parflow import Run
from pathlib import Path
import os
import re

from modeler.visualizations.soils import SoilVisualization
from modeler.visualizations.grid import ComputationalGridVisualization
from modeler.visualizations.forcing import ForcingVisualization
from modeler.visualizations.common import Visualizations

from modeler.pipeline import SourceImage
from modeler.annotations import CoordinateAnnotation
from modeler.annotations import CompassAnnotation

from modeler.utils.color import black
from modeler.utils.error import ParflowError

# -----------------------------------------------------------------------------
# Engine
# -----------------------------------------------------------------------------


class ParflowModelerEngine:
    def __init__(self, runDirectory):
        self.directory = Path(runDirectory)
        runFile = str(next(filter(self.isRunFile, self.directory.iterdir())))
        try:
            self.parflowConfig = Run.from_definition(runFile)
        except:
            print(f"Cannot read configFile: {runFile}")
            raise ParflowError

        self.files = list(
            map(str, filter(lambda x: not self.isRunFile(x), self.directory.iterdir()))
        )

        # Configure PV view for visualizations
        self.view = simple.GetRenderView()
        self.view.EnableRenderOnInteraction = 0
        self.view.OrientationAxesVisibility = 0
        self.view.Background = [0.7, 0.7, 0.7]

        # Configure PV source for visualizations
        self.parflowImage = SourceImage(self.parflowConfig)

        # Visualizations management
        self.edgeVisibility = False
        self.axesInfoVisibility = False
        self.currentVisualization = None

        # Initialize visualizations
        args = [self.view, self.parflowImage, self.parflowConfig]
        self.visualizations = Visualizations()
        self.visualizations.grid = ComputationalGridVisualization(*args)
        self.visualizations.soil = SoilVisualization(*args)
        self.visualizations.forcing = ForcingVisualization(*args)
        self.activateVisualization("grid")

        # Init annotations
        self.coordinateAnnotation = CoordinateAnnotation(*args)
        self.compassAnnotation = CompassAnnotation(self.view, self.parflowConfig)

        self.resetCamera()

    # -------------------------------------------------------------------------
    # Parflow config
    # -------------------------------------------------------------------------

    def getState(self):
        # Capture parflow configuration
        state = {
            "state": self.parflowConfig.to_dict(),
            "view": self.view.GetGlobalIDAsString(),
            "files": self.files,
        }

        # Capture state from each viz
        for name, viz in self.visualizations.items():
            state[name] = viz.getState()

        return state

    def simputSet(self, update):
        self.parflowConfig.pfset(flat_map=update)

    def runParflow():
        for f in self.directory.iterdir():
            if f.suffix.endswith("pfb"):
                self.parflowConfig.dist(f.name)

        self.parflowConfig.run(working_directory=str(self.directory))

    def setGridState(self, gridState):
        self.visualizations.grid.setState(gridState)

    # -------------------------------------------------------------------------
    # Visualization management
    # -------------------------------------------------------------------------

    def activateVisualization(self, name):
        if name in self.visualizations:
            if self.currentVisualization:
                self.currentVisualization.activate(False)

            viz = self.visualizations[name]
            self.currentVisualization = viz
            self.currentVisualization.activate()
        else:
            print(f"Can not find {name} in Viz")

    # -------------------------------------------------------------------------
    # Common across visualizations
    # -------------------------------------------------------------------------

    def resetCamera(self):
        simple.Render(self.view)
        simple.ResetCamera(self.view)
        try:
            self.view.CenterOfRotation = self.view.CameraFocalPoint
        except:
            pass

    def toggleDarkMode(self):
        if self.view.Background == [0.3, 0.3, 0.3]:
            self.view.Background = [0.7, 0.7, 0.7]
        else:
            self.view.Background = [0.3, 0.3, 0.3]

    def toggleEdgeVisibility(self):
        self.edgeVisibility = not self.edgeVisibility
        for viz in self.visualizations.values():
            viz.setEdgeVisibility(self.edgeVisibility)

    def toggleAxesInfoVisibility(self):
        self.axesInfoVisibility = not self.axesInfoVisibility
        self.coordinateAnnotation.setVisibility(self.axesInfoVisibility)
        for viz in self.visualizations.values():
            viz.setAxesInfoVisibility(self.axesInfoVisibility)

    def setZSpacing(self, zSpace):
        self.parflowImage.setZSpace(zSpace)
        self.resetCamera()
        return zSpace

    def setElevationScale(self, eScale):
        self.parflowImage.setElevationScale(eScale)
        self.resetCamera()
        return eScale

    # -------------------------------------------------------------------------
    # Computational Grid visualization
    # -------------------------------------------------------------------------

    # ...nothing specific yet...

    # -------------------------------------------------------------------------
    # Soil visualization
    # -------------------------------------------------------------------------

    def activateSoil(self, soilValue):
        return self.visualizations.soil.activateSoil(soilValue)

    def setSoilVisualizationMode(self, mode):
        return self.visualizations.soil.setSoilVisualizationMode(mode)

    def setSoilColors(self, colors):
        return self.visualizations.soil.setSoilColors(colors)

    # -------------------------------------------------------------------------
    # Forcing visualization
    # -------------------------------------------------------------------------

    def setForcingMoment(self, moment):
        return self.visualizations.forcing.setMoment(moment)

    def setForcingForce(self, force):
        return self.visualizations.forcing.setForce(force)

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def isRunFile(self, f):
        return any(f.suffix.endswith(suffix) for suffix in ["pfidb", "yaml", "yml"])
