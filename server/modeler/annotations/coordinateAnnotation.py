from paraview import simple
from modeler.utils.color import black


class CoordinateAnnotation:
    def __init__(self, view, parflowImage, parflowConfig):
        self.view = view
        self.parflowImage = parflowImage
        self.parflowConfig = parflowConfig
        self.visible = False
        self._loaded = False

        self.vScale = 1
        self.eScale = 0
        self.zPosition = 0.0

    def _load(self):
        # Format coordinates
        latitude = str(self.parflowConfig.Solver.CLM.Vegetation.Map.Latitude.Value)
        longitude = str(self.parflowConfig.Solver.CLM.Vegetation.Map.Longitude.Value)
        if latitude[0] != "-":
            latitude = "+" + latitude
        if longitude[0] != "-":
            longitude = "+" + longitude
        coordinates = f"{latitude}, {longitude}"

        # Stick coordinates at origin
        coordinateAnnotation = simple.Text()
        coordinateAnnotation.Text = coordinates

        self.coordinatesRep = simple.Show(coordinateAnnotation, self.view)
        self.coordinatesRep.TextPropMode = "Billboard 3D Text"
        self.coordinatesRep.Color = black

        self.coordinatesRep.FontSize = 14
        coordinatesHeight = (
            self.parflowConfig.ComputationalGrid.NZ
            * self.parflowConfig.ComputationalGrid.DZ
        )
        self.coordinatesRep.BillboardPosition = [
            0.0,
            0.0,
            coordinatesHeight * 10,
        ]  # 10 to render above surface

        self._loaded = True

    def setVisibility(self, visible=False):
        self.visible = visible
        if not self._loaded:
            self._load()
        self.coordinatesRep.Visibility = self.visible

    def setElevationScale(self, eScale):
        self.eScale = eScale
        self.updatePosition()

    def updatePosition(self):
        minElevation = self.parflowImage.minElevation()
        self.zPosition = float(-1 * self.eScale * self.vScale * minElevation)
        if self._loaded:
            self.coordinatesRep.Position = [0.0, 0.0, self.zPosition]
