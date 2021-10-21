import sys
import os.path
import yaml

from parflow import Run
from io import StringIO

from pprint import pprint


class ParflowWrapper:
    def __init__(self, work_dir):
        self.work_dir = work_dir

    def extract_run(self, simput):
        all_keys = simput.get_type("SearchKey")
        extracted_keys = {
            key.get("properties").get("key"): key.get("properties").get("value")
            for key in all_keys
        }

        path = os.path.join(self.work_dir, "run.yaml")
        with open(path, "w") as runFile:
            yaml.dump(extracted_keys, runFile)

    def validate_run(self):
        path = os.path.join(self.work_dir, "run.yaml")
        run = Run(path)

        try:
            # Redirect stdout to capture validation msg
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            run.validate()
        finally:
            sys.stdout = old_stdout

        return mystdout.getvalue()
