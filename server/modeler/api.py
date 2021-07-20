from wslink import register as exportRpc
from paraview.web import protocols as pv_protocols
from parflow import Run
from pathlib import Path
import json


class DataFlow(pv_protocols.ParaViewWebProtocol):
    def __init__(self, decode=True, runDirectory="", **kwargs):
        isRunFile = lambda f: any(
            f.suffix.endswith(suffix) for suffix in ["pfidb", "yaml", "yml"]
        )
        self.directory = Path(runDirectory)
        self.runFile = str(next(filter(isRunFile, self.directory.iterdir())))
        self.parflowConfig = Run.from_definition(self.runFile)

        pv_protocols.ParaViewWebProtocol.__init__(self)

        self.files = list(
            map(str, filter(lambda x: not isRunFile(x), self.directory.iterdir()))
        )

    @exportRpc("parflow.state.get")
    def getState(self):
        state = self.parflowConfig.to_dict()
        return {"state": state, "files": self.files}

    @exportRpc("parflow.simput.save")
    def simputSave(self, simputView):
        with open("debug_simput.json", "w") as simput:
            simput.write(json.dumps(simputView["debug"], indent=4))
        with open("debug_pfSet.json", "w") as pfset:
            pfset.write(json.dumps(simputView["converted"], indent=4))
        self.parflowConfig.pfset(flat_map=simputView["converted"])

    @exportRpc("parflow.simput.run")
    def simputRun(self):
        for f in self.directory.iterdir():
            if f.suffix.endswith("pfb"):
                self.parflowConfig.dist(f.name)

        self.parflowConfig.run(working_directory=str(self.directory))
