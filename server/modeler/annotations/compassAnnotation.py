from paraview import simple
from modeler.utils.color import black


class CompassAnnotation:
    def __init__(self, view, parflowConfig):
        self.view = view
        self.parflowConfig = parflowConfig
        self.visible = False
        self._loaded = False

    def _load(self):
        grid = self.parflowConfig.ComputationalGrid
        (northX, northY) = (grid.DX * grid.NX / 2, grid.DY * grid.NY * 1.5)
        (southX, southY) = (grid.DX * grid.NX / 2, grid.DY * grid.NY * -0.5)
        (eastX, eastY) = (grid.DX * grid.NX * 1.5, grid.DY * grid.NY / 2)
        (westX, westY) = (grid.DX * grid.NX * -0.5, grid.DY * grid.NY / 2)

        # Stick coordinates at origin
        northAnnotation = simple.Text()
        northAnnotation.Text = "N"
        southAnnotation = simple.Text()
        southAnnotation.Text = "S"
        eastAnnotation = simple.Text()
        eastAnnotation.Text = "E"
        westAnnotation = simple.Text()
        westAnnotation.Text = "W"

        # Make representations
        self.north = simple.Show(northAnnotation, self.view)
        self.north.TextPropMode = "Billboard 3D Text"
        self.north.Color = black
        self.south = simple.Show(southAnnotation, self.view)
        self.south.TextPropMode = "Billboard 3D Text"
        self.south.Color = black
        self.east = simple.Show(eastAnnotation, self.view)
        self.east.TextPropMode = "Billboard 3D Text"
        self.east.Color = black
        self.west = simple.Show(westAnnotation, self.view)
        self.west.TextPropMode = "Billboard 3D Text"
        self.west.Color = black

        # Position compass
        self.north.BillboardPosition = [northX, northY, 0.0]
        self.south.BillboardPosition = [southX, southY, 0.0]
        self.east.BillboardPosition = [eastX, eastY, 0.0]
        self.west.BillboardPosition = [westX, westY, 0.0]

        self._loaded = True

    def setVisibility(self, visible=False):
        self.visible = visible
        if not self._loaded:
            self._load()

        self.north.Visibility = self.visible
        self.south.Visibility = self.visible
        self.east.Visibility = self.visible
        self.west.Visibility = self.visible
