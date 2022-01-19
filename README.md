# Simulation Modeler
With this app a user can model various runs of the [parflow hydrologic simulator](https://www.parflow.org/). Parflow is a submodule of this repository, so clone with `git clone --recursive [URL to this Git repo]` or after cloning, initialize the submodule with `git submodule update --init`.

# Building and running
First we have to build our vuejs component library which trame will import.
```bash
simulation-modeler $ cd component_lib
client $ npm i
client $ npm run build
client $ cd ..
```

Then we can make our python environment and run the server.
```bash
simulation-modeler $ python3 -m venv .venv # I use python3.9
simulation-modeler $ source .venv/bin/activate
(.venv) simulation-modeler $ pip install -r requirements.txt
(.venv) simulation-modeler $ pip install -e parflow/pftools/python/parflow # Need to build generated.py first, see below
(.venv) simulation-modeler $ mkdir output data share
simulation-modeler $ deactivate # Visualizations require pvpython, which gets deps from venv  
simulation-modeler $ PV_VENV=.venv pvpython server/app.py -O output -D data -S share

```

# Making parflow changes
The code for parflow is [here](https://github.com/parflow/parflow), including a python module and solver definitions this application depends on.

Whenever you change the pf-keys definitions, you have to
1) Remake generated.py for the pftools module
```bash
cd parflow
source .venv/bin/activate
python pf-keys/generators/pf-python.py pftools/python/parflow/tools/database/generated.py
```
This should update automatically if you're using `pip install -e parflow/pftools/python/parflow` for pftools.
2) Generate the simput model from parflow keys
```
source .venv/bin/activate # Use environment with req's from scripts/parflow/requirements.txt
python scripts/parflow/generate_model.py -d parflow/pf-keys/definitions/ -o server/model/
```

# End to end workflow 
Here is a diagram of the whole workflow, from running a simulation, back through editing the run, and starting with generating the simput model.
```
1) Generate simput model (model.yaml) with scripts/parflow/generate_model.py
2) (optional) Read an existing run into a simput save with scripts/parflow/read_run.py
3) Edit with simput components in app.py
4) Export with RunWriter in app.py

  parflow/pf_keys/definitions   ┌─────────────────┐
 ──────────────────────────────►│generate_model.py├──────────────┐
                                └─────────────────┘              │
                                                                 │
                                   model.yaml                    │
              ┌──────────────────────────────────────────────────┘
              │
              │                                    ┌──────┐
              ├───────────────────────────────────►│      │
              │                                    │      │
              │  ┌───────────┐                     │simput├──────┐
              │  │           │  pf_settings.yaml   │      │      │
              └─►│           ├────────────────────►│      │      │
                 │read_run.py│                     └──────┘      │
  LW_test.yaml   │           │                                   │
 ───────────────►│           │                                   │
                 └───────────┘                                   │
                                                                 │
                                   (simput state)                │
              ┌──────────────────────────────────────────────────┘
              │
              │
              │   ┌────────────┐
              └──►│            │  run.yaml+files
  FileDatabase    │RunWriter.py├────────────────────
 ────────────────►│            │
                  └────────────┘

(edit with https://asciiflow.com/#/)
```
