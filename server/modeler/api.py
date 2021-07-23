from wslink import register as exportRpc
from paraview.web import protocols as pv_protocols
from .engine import ParflowModelerEngine
from parflow import Run
import json


class DataFlow(pv_protocols.ParaViewWebProtocol):
    def __init__(self, decode=True, runDirectory="", **kwargs):
        self.engine = ParflowModelerEngine(runDirectory)
        pv_protocols.ParaViewWebProtocol.__init__(self)

    # -----------------------------------------------------
    # State management
    # -----------------------------------------------------

    @exportRpc("parflow.state.get")
    def getState(self):
        return self.engine.getState()

    @exportRpc("parflow.simput.save")
    def simputSave(self, simputView):
        with open("debug_simput.json", "w") as simput:
            simput.write(json.dumps(simputView["debug"], indent=4))
        with open("debug_pfSet.json", "w") as pfset:
            pfset.write(json.dumps(simputView["converted"], indent=4))
        self.engine.simputSet(simputView["converted"])

    @exportRpc("parflow.state.grid.set")
    def setGridState(self, gridState):
        return self.engine.setGridState(gridState)

    # -----------------------------------------------------
    # Run
    # -----------------------------------------------------

    @exportRpc("parflow.simput.run")
    def simputRun(self):
        return self.engine.runParflow()

    # -----------------------------------------------------
    # Common API across viz
    # -----------------------------------------------------

    @exportRpc("parflow.viz.reset.camera")
    def resetCamera(self):
        self.engine.resetCamera()
        self.getApplication().InvokeEvent("UpdateEvent")

    @exportRpc("parflow.viz.axes.toggle")
    def toggleAxesInfoVisibility(self):
        self.engine.toggleAxesInfoVisibility()
        self.getApplication().InvokeEvent("UpdateEvent")

    @exportRpc("parflow.viz.edge.toggle")
    def toggleEdgeVisibility(self):
        self.engine.toggleEdgeVisibility()
        self.getApplication().InvokeEvent("UpdateEvent")

    @exportRpc("parflow.viz.space.set")
    def setZSpacing(self, zSpace):
        s = self.engine.setZSpacing(zSpace)
        self.getApplication().InvokeEvent("UpdateEvent")
        return s

    @exportRpc("parflow.viz.elevation.set")
    def setElevationScale(self, eScale):
        s = self.engine.setElevationScale(eScale)
        self.getApplication().InvokeEvent("UpdateEvent")
        return s

    @exportRpc("parflow.viz.activate")
    def activateVisualization(self, name):
        self.engine.activateVisualization(name)
        self.getApplication().InvokeEvent("UpdateEvent")
        return self.engine.getState()

    @exportRpc("parflow.viz.dark.toggle")
    def toggleDarkMode(self):
        self.engine.toggleDarkMode()
        self.getApplication().InvokeEvent("UpdateEvent")
        return self.engine.getState()

    # -----------------------------------------------------
    # Computational Grid
    # -----------------------------------------------------

    # -----------------------------------------------------
    # Soils
    # -----------------------------------------------------

    @exportRpc("parflow.soil.activate")
    def activateSoil(self, soilValue):
        s = self.engine.activateSoil(soilValue)
        self.getApplication().InvokeEvent("UpdateEvent")
        return s

    @exportRpc("parflow.soil.mode")
    def setSoilVisualizationMode(self, mode):
        result = self.engine.setSoilVisualizationMode(mode)
        self.getApplication().InvokeEvent("UpdateEvent")
        return result

    @exportRpc("parflow.soil.colors.set")
    def setSoilColors(self, colorUpdate):
        s = self.engine.setSoilColors(colorUpdate)
        self.getApplication().InvokeEvent("UpdateEvent")
        return s

    # -----------------------------------------------------
    # Forcing
    # -----------------------------------------------------

    @exportRpc("parflow.forcing.moment.set")
    def setForcingMoment(self, moment):
        valueRange = self.engine.setForcingMoment(moment)
        self.getApplication().InvokeEvent("UpdateEvent")
        return valueRange

    @exportRpc("parflow.forcing.force.set")
    def setForcingForce(self, force):
        valueRange = self.engine.setForcingForce(force)
        self.getApplication().InvokeEvent("UpdateEvent")
        return valueRange


# -----------------------------------------------------------------------------
# Mouse add-on
# -----------------------------------------------------------------------------


class ZoomWheelProtocol(pv_protocols.ParaViewWebProtocol):
    @exportRpc("viewport.mouse.zoom.wheel")
    def updateZoomFromWheel(self, event):
        if "Start" in event["type"]:
            self.getApplication().InvokeEvent("StartInteractionEvent")

        viewProxy = self.getView(event["view"])
        if viewProxy and "spinY" in event:
            rootId = viewProxy.GetGlobalIDAsString()
            zoomFactor = 1.0 - event["spinY"] / 10.0

            fp = viewProxy.CameraFocalPoint
            pos = viewProxy.CameraPosition
            delta = [fp[i] - pos[i] for i in range(3)]
            viewProxy.GetActiveCamera().Zoom(zoomFactor)
            viewProxy.UpdatePropertyInformation()
            pos2 = viewProxy.CameraPosition
            viewProxy.CameraFocalPoint = [pos2[i] + delta[i] for i in range(3)]

        if "End" in event["type"]:
            self.getApplication().InvokeEvent("EndInteractionEvent")
