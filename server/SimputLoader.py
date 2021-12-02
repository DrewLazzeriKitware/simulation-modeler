import json


class SimputLoader:
    def __init__(self, simput, keyFile="data/washita_run.json", modelFile="data/flattened_pf_keys.json"):
        self.simput = simput
        self.keyFile = keyFile
        self.modelFile = modelFile

    def load_keys(self):
        """
        Get just the solver keys in the Washita run from the old simput model
        """
        ids = []
        with open(self.keyFile) as runKeys:
            keys = json.load(runKeys).keys()

        with open(self.modelFile) as flatModel:
            solverKeys = {
                solverKey["id"]: solverKey for solverKey in json.load(flatModel)
            }

        for key in keys:
            if key.startswith("Solver"):
                solverKey = key.replace(".", "/")
                model = solverKeys.get(solverKey)
                if model and model.get("help"):
                    obj = self.simput.create("SearchKey")
                    self.set(obj.get("id"), "key", solverKey)
                    self.set(obj.get("id"), "description", model.get("help"))
                    ids.append(obj.get("id"))
                else:
                    print("Couldn't place ", key)
        return ids

    def set(self, entry_id, name, value):
        self.simput.update([{"id": entry_id, "name": name, "value": value}])

    def generate_search_index(self):
        index = {
            s.get("id"): self.searchText(s) for s in self.simput.get_type("SearchKey")
        }
        solverSearchIds = list(index.keys())
        return index

    def searchText(self, key):
        props = key.get("properties")
        return props.get("description") + props.get("key")
