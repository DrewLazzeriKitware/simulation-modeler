import sys
import os.path
import yaml

from parflow import Run
from io import StringIO

from pprint import pprint


class SimulationManager:
    def __init__(self, work_dir, loader, filedb):
        self.work_dir = work_dir
        self.key_value_store = loader.default_keys
        self.trame_parflow_mapping = loader.trame_parflow_mapping
        self.domain_set_keys = loader.domain_set_keys

    def read_from_simput(self, pxm):
        all_keys = pxm.get_instances_of_type("SearchKey")
        extracted_keys = {
            key.get_property("key").replace("/", "."): key.get_property("value")
            for key in all_keys
        }

        self.key_value_store.update(extracted_keys)

    def read_from_trame(self, trame_state):
        trame_keys = {
            pf_key: trame_state[trame_key]
            for (trame_key, pf_key) in self.trame_parflow_mapping.items()
        }
        self.key_value_store.update(trame_keys)

        domain_set_keys = {
            domain_key: self.key_value_store[trame_key]
            for domain_key, trame_key in self.domain_set_keys.items()
        }
        self.key_value_store.update(domain_set_keys)

    def validate_run(self):
        path = os.path.join(self.work_dir, "run.yaml")
        with open(path, "w") as runFile:
            yaml.dump(self.key_value_store, runFile)

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
