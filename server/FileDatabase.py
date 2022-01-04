import os.path
import random
import yaml


class FileDatabase:
    def __init__(self, state):
        self.datastore = state.get("datastore")
        path = os.path.join(self.datastore, "pf_datastore.yaml")
        with open(path) as entriesFile:
            self.entries = yaml.safe_load(entriesFile) or {}

    def addNewEntry(self, newFile):
        entryId = str(random.getrandbits(32))
        dataId = str(random.getrandbits(32))
        newFile["id"] = entryId
        newFile["dataId"] = dataId
        self.writeEntry(entryId, newFile)
        return newFile

    def writeEntry(self, entryId, metadata):
        self.entries = {**self.entries, entryId: metadata}
        # Update data on disk
        path = os.path.join(self.datastore, "pf_datastore.yaml")
        with open(path, "w") as db:
            yaml.dump(self.entries, db)

    def getEntry(self, entryId):
        return self.entries.get(entryId)

    def getEntries(self):
        return self.entries

    def getEntryPath(self, entryId):
        if entryId is None:
            print("Failed to find path for empty entryId")
            return
        entry = self.entries[entryId]
        dataId = entry.get("dataId")

        if dataId is None:
            print("Could not find dataId for entry while finding path", entryId)
            return

        return os.path.join(self.datastore, dataId)

    def getEntryData(self, entryId):
        path = self.getEntryPath(entryId)
        with open(path, "rb") as entryFile:
            return entryFile.read()

    def writeEntryData(self, entryId, content):
        if entryId is None:
            print("Failed to write data to empty entryId")
            return

        entry = self.entries[entryId]
        dataId = entry.get("dataId")

        if dataId is None:
            print("Could not find dataId for entry while writing data", entryId)
            return

        path = os.path.join(self.datastore, dataId)
        with open(path, "wb") as entryFile:
            entryFile.write(content)

    def deleteEntry(self, entryId):
        pass
