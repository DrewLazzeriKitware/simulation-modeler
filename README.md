# Simulation Modeler
With this app a user can model various runs of the [parflow hydrologic simulator](https://www.parflow.org/).

# Building and running
First we have to build vuejs components which trame will import.
```bash
simulation-modeler $ cd lib/client 
client $ npm i   
client $ npm run build
client $ cd ..
```

Then we can make our python environment and run the server.
```bash
simulation-modeler $ python3 -m venv .venv # I use python3.8
simulation-modeler $ source .venv/bin/activate
(.venv) simulation-modeler $ pip install -r requirements.txt 
(.venv) simulation-modeler $ pip install -e lib/python 
(.venv) simulation-modeler $ python server/app.py      
(.venv) simulation-modeler $ mkdir output
(.venv) simulation-modeler $ python server/app.py -O output 
```

# Required files
## washita_run.json
This describes a run of the little washita project. It is needed to set default values for the solver keys.

## flattened_pf_keys.json
This comes from the simput generator that is part of parflow's pf-keys. It has all of the domains and documentation for the keys.


