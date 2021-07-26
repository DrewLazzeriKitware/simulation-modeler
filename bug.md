# Bug: Server fails in docker, but runs fine in dev env
## Message
```
 File "/pvw/server/app.py", line 64, in initialize
    self.registerVtkWebProtocol(api.DataFlow(runDirectory=self.runDirectory))
  File "/pvw/server/modeler/api.py", line 10, in __init__
    self.engine = ParflowModelerEngine(runDirectory)
  File "/pvw/server/modeler/engine.py", line 37, in __init__
    self.set_visualizations()
  File "/pvw/server/modeler/engine.py", line 48, in set_visualizations
    self.parflowImage = SourceImage(self.parflowConfig)
  File "/pvw/server/modeler/pipeline/sourceImage.py", line 26, in __init__
    self.addPointArray(self.elevationFilter.getArray())
  File "/pvw/server/modeler/pipeline/elevationFilter.py", line 27, in getArray
    elevation = elevationReader.getDataAsArray()
  File "/usr/local/lib/python3.6/dist-packages/parflowio/pyParflowio.py", line 246, in <lambda>
    __getattr__ = lambda self, name: _swig_getattr(self, PFData, name)
  File "/usr/local/lib/python3.6/dist-packages/parflowio/pyParflowio.py", line 80, in _swig_getattr
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))
AttributeError: 'PFData' object has no attribute 'getDataAsArray'
```
## Things I've looked into
- Calls to PFData.viewDataArray look the same between docker and devEnv
- Library version the same: 3.0.12
