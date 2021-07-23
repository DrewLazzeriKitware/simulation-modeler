import vtk
from paraview import simple

from parflow.tools.fs import get_absolute_path

from .common import AbstractVisualization
from modeler.utils.color import black


class ComputationalGridVisualization(AbstractVisualization):
    def __init__(self, view, parflowImage, parflowConfig):
        super().__init__(view, parflowImage, parflowConfig)
        self.parflowImage = parflowImage

        grid = self.parflowConfig.ComputationalGrid
        self.cellMaxes = (grid.NZ, grid.NY, grid.NX)
        self.fieldName = "processId"

        # Viz variables
        self.source = None
        self.distribution = None
        self.zSpaceFactor = 1

    # -------------------------------------------------------------------------
    # Manage State
    # -------------------------------------------------------------------------

    def getState(self):
        """Set of properties that are specific to this viz"""
        process = self.parflowConfig.Process
        grid = self.parflowConfig.ComputationalGrid
        return {
            "P": process.Topology.P,
            "Q": process.Topology.Q,
            "R": process.Topology.R,
            "OX": grid.Lower.X,
            "OY": grid.Lower.Y,
            "OZ": grid.Lower.Z,
            "DX": grid.DX,
            "DY": grid.DY,
            "DZ": grid.DZ,
            "NX": grid.NX,
            "NY": grid.NY,
            "NZ": grid.NZ,
        }

    # -------------------------------------------------------------------------
    # Viz setup
    # -------------------------------------------------------------------------

    def _load(self):

        # Attach array for process ids of distributed computational grid
        self.distributionArray = vtk.vtkFloatArray()
        self.distributionArray.SetName(self.fieldName)
        self.distributionArray.SetNumberOfComponents(1)
        (kCellMax, jCellMax, iCellMax) = self.cellMaxes
        self.distributionArray.SetNumberOfTuples(iCellMax * jCellMax * kCellMax)
        self.parflowImage.addCellArray(self.distributionArray)

        self.source = self.parflowImage.getSource()

        # Construct representations
        self.distribution = simple.Show(self.source, self.view)
        self.distribution.SetRepresentationType("Surface")
        self._distributeGrid()

        # Color grid and array
        simple.ColorBy(self.distribution, ("CELLS", self.fieldName))
        self.distribution.EdgeColor = [0.2, 0.2, 0.2]
        self.loaded = True

        # Color axes info
        self.distribution.DataAxesGrid.XTitle = ""
        self.distribution.DataAxesGrid.YTitle = ""
        self.distribution.DataAxesGrid.XLabelColor = black
        self.distribution.DataAxesGrid.YLabelColor = black
        self.distribution.DataAxesGrid.ZLabelColor = black
        self.distribution.DataAxesGrid.GridColor = black
        self.distribution.DataAxesGrid.FacesToRender = 36

        # Register components for services
        self.allRepresentations.append(self.distribution)
        self.edgeRepresentations.append(self.distribution)
        self.scaleRepresentations.append(self.distribution)

        self.proxyToDelete.append(self.distribution)

    def _distributeGrid(self):
        # Fill array with grid distribution process ids
        top = self.parflowConfig.Process.Topology
        (p, q, r) = (top.P, top.Q, top.R)
        (kCellMax, jCellMax, iCellMax) = self.cellMaxes
        for k in range(kCellMax):
            k_pqr = int(r * k / kCellMax)
            for j in range(jCellMax):
                j_pqr = int(q * j / jCellMax)
                for i in range(iCellMax):
                    i_pqr = int(p * i / iCellMax)
                    value = i_pqr + j_pqr * p + k_pqr * p * q
                    idx = i + j * iCellMax + k * iCellMax * jCellMax
                    self.distributionArray.SetTuple1(idx, value)

        # Mark pipeline dirty #FIXME I don't understand the differences between these
        self.distributionArray.Modified()
        self.source.MarkModified(self.source)
        self.source.UpdatePipeline()

        colorMap = simple.GetColorTransferFunction(self.fieldName)
        colorMap.RescaleTransferFunction(0, p * q * r - 1)
