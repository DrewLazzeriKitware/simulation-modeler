import sys
import os.path
import yaml

from parflow import Run
from io import StringIO

from pprint import pprint

DEFAULT_KEYS = {"Gravity": 1.0, "Domain.GeomName": "domain"}

TRAME_PARFLOW_MAPPING = {
    "BaseUnit": "TimingInfo.BaseUnit",
    "DumpInterval": "TimingInfo.DumpInterval",
    "StartCount": "TimingInfo.StartCount",
    "StartTime": "TimingInfo.StartTime",
    "StopTime": "TimingInfo.StopTime",
    "LX": "ComputationalGrid.Lower.X",
    "LY": "ComputationalGrid.Lower.Y",
    "LZ": "ComputationalGrid.Lower.Z",
    "NX": "ComputationalGrid.NX",
    "NY": "ComputationalGrid.NY",
    "NZ": "ComputationalGrid.NZ",
    "DX": "ComputationalGrid.DX",
    "DY": "ComputationalGrid.DY",
    "DZ": "ComputationalGrid.DZ",

}


class ParflowWrapper:
    def __init__(self, work_dir):
        self.work_dir = work_dir
        self.key_value_store = DEFAULT_KEYS

    def read_from_simput(self, pxm):
        all_keys = pxm.get_instances_of_type("SearchKey")
        extracted_keys = {
            key.get_property("key")
            .replace("/", "."): key.get_property("value")
            for key in all_keys
        }

        self.key_value_store.update(extracted_keys)

    def read_from_trame(self, trame_state):
        keys = {
            pf_key: trame_state[trame_key]
            for (trame_key, pf_key) in TRAME_PARFLOW_MAPPING.items()
        }
        self.key_value_store.update(keys)

    def validate_run(self):
        path = os.path.join(self.work_dir, "run.yaml")
        with open(path, "w") as runFile:
            yaml.dump(self.key_value_store, runFile)

        run = Run.from_definition(path)

        try:
            # Redirect stdout to capture validation msg
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            run.validate()
        finally:
            sys.stdout = old_stdout

        return mystdout.getvalue()
