import vtk
from paraview import simple
from parflowio.pyParflowio import PFData


class AbstractVisualization:
    def __init__(self, view, parflowImage, parflowConfig):
        self.loaded = False
        self.view = view
        self.parflowImage = parflowImage
        self.parflowConfig = parflowConfig

        # Viz variables
        self.edgeVisibility = False
        self.allRepresentations = []
        self.edgeRepresentations = []
        self.scaleRepresentations = []
        self.proxyToDelete = []

    # Common to all visualizations
    def setEdgeVisibility(self, visible):
        self.edgeVisibility = visible

        repTypeSurface = "Surface With Edges" if self.edgeVisibility else "Surface"
        repTypeOutline = "Wireframe" if self.edgeVisibility else "Outline"

        for rep in self.edgeRepresentations:
            if "Surface" in str(rep.Representation):
                rep.SetRepresentationType(repTypeSurface)
            else:
                rep.SetRepresentationType(repTypeOutline)
            rep.AmbientColor = [0.2, 0.2, 0.2]
            rep.EdgeColor = [0.2, 0.2, 0.2]

        return self.edgeVisibility

    def setAxesInfoVisibility(self, visibility):
        for rep in self.allRepresentations:
            rep.DataAxesGrid.GridAxesVisibility = 1

    def activate(self, activate=True):
        if activate:
            if not self.loaded:
                self._load()
            self.setEdgeVisibility(self.edgeVisibility)

        visibility = 1 if activate else 0
        for rep in self.allRepresentations:
            rep.Visibility = visibility

    def __del__(self):
        for proxy in self.proxyToDelete:
            simple.Delete(proxy)


class Visualizations(dict):
    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def has_key(self, k):
        return k in self.__dict__

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))
