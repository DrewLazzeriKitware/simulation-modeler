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


# Parflow fixes 
1) The current simput generator for pf-keys ignores top level keys, like Solver.
2) There are missing domains, like Geom.Domain should have a domains.EnumDomains.location.

# Questions
## What is the simplest CLM setup you might use?

## When is there no indicator file? When is a domain not a box?
We assume that they have an indicator file (.pfb) which we can derive geometry from. It will be a child of indi_input.
> Can a solidfile (.pfsol) be the indicator? 
- It seems a pfsol file describes patches but not indications (subsections). 
We assume that we can derive a box domain which is based on the required indicator file. According to the keys, Domain.GeomName is mandatory and must have patches that equal the entire domain surface.
> Can the indicator be the domain? 
- It seems an indicator file does not describe patches, which the domain must, so we'll use a box.
> Can a solidfile be the domain?
- Yes, and sandtank does this. I don't know a way to render pfsol files in paraview though. I'm assuming this is hard, until I get an answer about  about rendering pfsol. 

## When would you want sides / bottom that are not zero flux? 
> When would you use multiple cycles?

## When is geometry different than the indicator file?
We assume most geometry can be inferred from the indicator file.
It's possible that the d{xyz} can't be, but documentations suggests it should. I also have a reasonable guess if we can't get anything from the file.
We want have the domain here, since it can validate with the other spacial pfbs. They all must match the required indicator file. 

## When would you want complicated surface conditions?
We assume boundary conditions on top is either a OverlandFlow or const

## When might you want hydroStaticPatches or hydroStaticDeptch in your initial conditions? What about an NC file?

# Answered
> What does a researcher want out of this? A python file that will run through pftools? On what setup? 
- I assume there is a zip folder structure that makes sense at the end to export. It will have the file database and a python script describing the run (so, dist files etc.). I'll have a docker image with a --data that expects exactly this format and runs the simulation, outputting in the same directory. And if people need, we can put all these apps in the same launcher (conceptual-modeler, simulation-modeler, post-processing). 

> How does one make a pfb file? (Is it hard, so people prefer to make one then assign indices/indications?)
- It's strange

> Do I draw every component?
- Yes. Don't leave anything for when you're coding.

> Do I list every "validity" condition?
- Yes. If they're too much for you on paper, wouldn't they be too much for the researcher?

> What validation info do I have?
- MandatoryValue keys are one source. My own requirements ("Have an indicator") is another. We can add more to the keys, if we know more and want to.

> Can paraview render a pfsol file?
- I'm assuming there's no reader, or it would have been in the parflow plugin. 

> Should  I hide pages? Or grey them?  Should two controls ungrey CLM eg?
- Let's grey pages, and let two controls ungrey CLM if they are in good places. 

> We assume that the user is only using water. Anecdotally, Reed said other phases were rare. Also, the docs for Solver say that both Richards and Impes assume they are not multi-phase.
> I will just add __simput__ keys when I need to indicate that, say, "these pfkeys are grouped on the CLM page."



