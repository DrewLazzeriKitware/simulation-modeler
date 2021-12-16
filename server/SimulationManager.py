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
        extracted_keys = { }

        for proxy_type in pxm.types():
            for proxy in pxm.get_instances_of_type(proxy_type):
                for (prop_name, prop) in proxy.definition.items():
                    value = proxy.get_property(prop_name)
                    if value is not None:
                        extracted_keys[prop['_parflowId']] = value

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
