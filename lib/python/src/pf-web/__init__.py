import os
import json

serve_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "dist"))

serve = {"__parflow": serve_path}
scripts = ["/__parflow/parflow.umd.min.js"]
styles = ["/__parflow/parflow.css"]
