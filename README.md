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

# Making parflow changes
If you change the parflow keys, you have to
1) Remake the pftools module
```bash
cd parflow
source .venv/bin/activate
python pf-keys/generators/pf-python.py pftools/python/parflow/tools/database/generated.py
```
This should update automatically if you're using `pip install -e parflow/pftools/python/parflow` for pftools.
2) Remake anything depending on pf-keys