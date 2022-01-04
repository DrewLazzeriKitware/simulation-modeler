import sys
import os.path
import yaml

from parflow import Run
from io import StringIO


class SimulationManager:
    def __init__(self, work_dir, filedb):
        self.work_dir = work_dir
        self.run = {}

    def read_from_simput(self, pxm):
        extracted_keys = {}

        for proxy_type in pxm.types():
            print(proxy_type)
            definition = pxm.get_definition(proxy_type)
            for proxy in pxm.get_instances_of_type(proxy_type):
                for (prop_name, prop) in proxy.definition.items():
                    if prop_name.startswith("_"):
                        continue
                    value = proxy.get_property(prop_name)
                    if value is not None:
                        if definition.get("_exportPrefix"):
                            name = (
                                prop["_exportPrefix"]
                                + proxy.get_property("name")
                                + prop["_exportSuffix"]
                            )
                        else:
                            name = prop["_exportSuffix"]
                        extracted_keys[name] = value

        self.run.update(extracted_keys)

    def validate_run(self):
        path = os.path.join(self.work_dir, "run.yaml")
        with open(path, "w") as runFile:
            yaml.dump(self.run, runFile)

        run = Run.from_definition(path)
        run.dist("IndicatorFile_Gleeson.50z.pfb")
        run.run()

        try:
            # Redirect stdout to capture validation msg
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            valid = run.validate() == 0

            if valid:
                print("Validation passed.")
        finally:
            sys.stdout = old_stdout

        return mystdout.getvalue()
