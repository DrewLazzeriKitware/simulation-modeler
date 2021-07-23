import vtk
from vtk.numpy_interface import dataset_adapter as dsa
from paraview import simple

from parflowio.pyParflowio import PFData
from parflow.tools.fs import get_absolute_path

from modeler.utils.color import blue, white, red, green, black
from modeler.utils.error import ParflowError

from .common import AbstractVisualization


class ForcingVisualization(AbstractVisualization):
    def __init__(self, view, parflowImage, parflowConfig):
        super().__init__(view, parflowImage, parflowConfig)
        self.view = view
        self.parflowImage = parflowImage
        self.parflowConfig = parflowConfig

        self.forcingPrefix = self.parflowConfig.Solver.CLM.MetFileName
        self.forcingDirectory = self.parflowConfig.Solver.CLM.MetFilePath
        self.forcingInterval = self.parflowConfig.Solver.CLM.MetFileNT

        self.force = "Temp"
        self.moment = 0
        self.visibleForce = None
        self.forceArraysByFilename = {}
        self.zSpaceFactor = 1

        # Viz components
        self.source = None
        self.fieldName = "forcing"
        self.cachedForces = {}

    # -------------------------------------------------------------------------
    # Manage State
    # -------------------------------------------------------------------------

    def getState(self):
        state = {}
        if self.visibleForce:
            state = self.visibleForce.toDict()
        state["force"] = self.force
        state["moment"] = self.moment
        return state

    # -------------------------------------------------------------------------
    # Viz setup
    # -------------------------------------------------------------------------

    def _load(self):

        # Mesh mirroring terrain contextualizes forcing
        self.terrainSource = self.parflowImage.getSource()
        self.terrainRep = simple.Show(self.terrainSource, self.view)
        self.terrainRep.SetRepresentationType("Outline")

        cGrid = self.parflowConfig.ComputationalGrid

        # Mesh mirroring pfidb X and Y dimensions
        self.forcingGrid = vtk.vtkImageData()
        self.forcingGrid.SetDimensions(cGrid.NX + 1, cGrid.NY + 1, 2)  # Points
        self.forcingGrid.SetOrigin(
            cGrid.Lower.X,
            cGrid.Lower.Y,
            cGrid.Lower.Z + cGrid.NZ * cGrid.DZ,
        )
        self.forcingGrid.SetSpacing(
            cGrid.DX,
            cGrid.DY,
            cGrid.DZ * 10,
        )

        # Create and attach an array
        self.forcingArray = vtk.vtkFloatArray()
        self.forcingArray.SetName(self.fieldName)
        self.forcingArray.SetNumberOfTuples(cGrid.NX * cGrid.NY)
        self.forcingArray.SetNumberOfComponents(1)
        self.forcingGrid.GetCellData().AddArray(self.forcingArray)

        # Get vtk interface from paraview to pipe dataset
        self.source = simple.TrivialProducer()
        self.vtkProducer = self.source.GetClientSideObject()
        self.vtkProducer.SetOutput(self.forcingGrid)

        self._setForcing(self.force, self.moment)

        # Construct representations
        self.forcingRep = simple.Show(self.source, self.view)
        self.forcingRep.SetRepresentationType("Surface")

        # Set colors
        simple.ColorBy(self.forcingRep, ("CELLS", self.fieldName))

        # Color axes info
        self.terrainRep.DataAxesGrid.XTitle = ""
        self.terrainRep.DataAxesGrid.YTitle = ""
        self.terrainRep.DataAxesGrid.XLabelColor = black
        self.terrainRep.DataAxesGrid.YLabelColor = black
        self.terrainRep.DataAxesGrid.ZLabelColor = black
        self.terrainRep.DataAxesGrid.GridColor = black
        self.terrainRep.DataAxesGrid.FacesToRender = 36

        # Register components for services
        self.allRepresentations.append(self.forcingRep)
        self.allRepresentations.append(self.terrainRep)
        self.edgeRepresentations.append(self.forcingRep)
        self.edgeRepresentations.append(self.terrainRep)
        self.scaleRepresentations.append(self.terrainRep)

        self.proxyToDelete.append(self.forcingRep)
        self.proxyToDelete.append(self.terrainRep)
        self.proxyToDelete.append(self.source)

        self.loaded = True

    def _setForcing(self, force, moment):

        # Time dimension is across several files AND along z-axis within files
        momentWithinFile = moment % self.forcingInterval

        timeRangeStart = (moment // self.forcingInterval) * self.forcingInterval + 1
        timeRangeEnd = (moment // self.forcingInterval + 1) * self.forcingInterval
        timeRange = f"{timeRangeStart:06}_to_{timeRangeEnd:06}"
        filename = f"{self.forcingPrefix}.{force}.{timeRange}.pfb"

        # Cache forcing arrays by filename
        if filename not in self.forceArraysByFilename.keys():
            filepath = get_absolute_path(self.forcingDirectory + filename)

            try:
                forcingFileHandle = PFData(filepath)
            except:
                print(f"Could not find pfb {filepath}")
                raise ParflowError

            forcingFileHandle.loadHeader()
            forcingFileHandle.loadData()

            self.forceArraysByFilename[filename] = forcingFileHandle.moveDataArray()

        # Move forcing data into grid's cell data
        forcingNumpyArray = self.forceArraysByFilename[filename]
        cGrid = self.parflowConfig.ComputationalGrid
        for j in range(cGrid.NY):
            for i in range(cGrid.NX):
                idx = i + j * cGrid.NX
                value = forcingNumpyArray[momentWithinFile, j, i]
                self.forcingArray.SetTuple1(idx, value)

        # Mark pipeline dirty
        self.forcingArray.Modified()
        self.source.MarkModified(self.source)

        # Cache loaded forces
        if force not in self.cachedForces.keys():
            self.cachedForces[force] = Force(force)
        self.visibleForce = self.cachedForces[force]

        # Track highest, lowest values yet loaded
        (minVal, maxVal) = self.forcingArray.GetRange(0)
        self.visibleForce.updateHigh(maxVal)
        self.visibleForce.updateLow(minVal)

        colorMap = simple.GetColorTransferFunction(self.fieldName)
        colorMap.RescaleTransferFunction(
            self.visibleForce.minVisible, self.visibleForce.maxVisible
        )
        colorMap.RGBPoints = self.visibleForce.getRGBPoints()

        return self.visibleForce.toDict()

    def setMoment(self, moment):
        if not self.loaded:
            return
        self.moment = moment
        valueRange = self._setForcing(self.force, self.moment)
        return self.getState()

    def setForce(self, force):
        if not self.loaded:
            return
        self.force = force
        valueRange = self._setForcing(self.force, self.moment)
        return self.getState()


class ColorSeries:
    def __init__(
        self,
        low,
        high,
        mid=None,
    ):
        self.lowColor = low
        self.highColor = high

        if mid is None:
            self.midColor = (
                (self.lowColor[0] + self.highColor[0]) / 2,
                (self.lowColor[1] + self.highColor[1]) / 2,
                (self.lowColor[2] + self.highColor[2]) / 2,
            )
        else:
            self.midColor = mid

    def toDict(self):
        return {"low": self.lowColor, "mid": self.midColor, "high": self.highColor}


class Force:
    # Ref: https://portal.nccs.nasa.gov/lisdata_pub/data/MET_FORCING/NLDAS2/NLDAS2_GESDISC.README
    colorsByForce = {
        # Sync with src/components/Forcing/script.js
        "Temp": ColorSeries(low=blue, mid=white, high=red),
        "APCP": ColorSeries(low=white, high=blue),
        "DLWR": ColorSeries(low=white, high=black),
        "DSWR": ColorSeries(low=white, high=black),
        "Press": ColorSeries(low=blue, mid=white, high=red),
        "SPFH": ColorSeries(low=white, high=green),
    }

    unitsByForce = {
        "Temp": "k",
        "APCP": "kg/m^2",
        "DLWR": "W/m^2",
        "DSWR": "W/m^2",
        "Press": "Pa",
        "SPFH": "kg/kg",
    }

    def __init__(self, name):
        self.name = name
        self.colors = Force.colorsByForce[self.name]
        self.units = Force.unitsByForce[self.name]
        self.minRendered = None
        self.maxRendered = None
        self.minVisible = None
        self.maxVisible = None

    def getRGBPoints(self):
        rgbPoints = []

        rgbPoints.append(self.minVisible)
        rgbPoints.extend(self.colors.lowColor)
        rgbPoints.append(self.midPoint())
        rgbPoints.extend(self.colors.midColor)
        rgbPoints.append(self.maxVisible)
        rgbPoints.extend(self.colors.highColor)

        return rgbPoints

    def midPoint(self):
        return (self.minVisible + self.maxVisible) / 2

    def updateLow(self, newMin):
        self.minVisible = newMin
        if self.minRendered is None or self.minVisible < self.minRendered:
            self.minRendered = self.minVisible

    def updateHigh(self, newMax):
        self.maxVisible = newMax
        if self.maxRendered is None or self.maxVisible > self.maxRendered:
            self.maxRendered = self.maxVisible

    def toDict(self):
        return {
            "name": self.name,
            "minRendered": self.minRendered,
            "maxRendered": self.maxRendered,
            "minVisible": self.minVisible,
            "maxVisible": self.maxVisible,
            "colors": self.colors.toDict(),
            "units": self.units,
        }
