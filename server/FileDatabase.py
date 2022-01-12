import os
import os.path
import random
import yaml

from typing import Optional

from enum import Enum

from singleton import Singleton

class FileCategories(str, Enum):
    Indicator = "INDICATOR"
    Terrain = "TERRAIN"
    Other = "OTHER"

def file_category_label(category: FileCategories) -> str:
    if category is FileCategories.Indicator:
        return "Indicator"
    elif category is FileCategories.Terrain:
        return "Terrain"
    elif category is FileCategories.Other:
        return "Other"
    else:
        raise Exception(f"Unknown file category: {category}")

@Singleton
class FileDatabase:
    def __init__(self, datastore):
        self.datastore = datastore
        self.entries = self._loadEntries()

    def addNewEntry(self, newFile):
        entryId = str(random.getrandbits(32))
        dataId = str(random.getrandbits(32))
        newFile["id"] = entryId
        newFile["dataId"] = dataId
        self.writeEntry(entryId, newFile)
        return newFile

    def writeEntry(self, entryId, metadata):
        self.entries = {**self.entries, entryId: metadata}
        self._writeEntries(self.entries)

    def _writeEntries(self, entries):
        path = self._getDbPath()
        with open(path, "w") as db:
            yaml.dump(entries, db)

    def _loadEntries(self):
        path = self._getDbPath()
        with open(path) as entriesFile:
            return yaml.safe_load(entriesFile) or {}

    def _getDbPath(self):
        return os.path.join(self.datastore, "pf_datastore.yaml")

    def getEntry(self, entryId):
        return self.entries.get(entryId)

    def getEntries(self):
        return self.entries

    def getEntryPath(self, entryId):
        if entryId is None:
            raise Exception("Failed to find path for empty entryId")
        entry = self.entries[entryId]
        dataId = entry.get("dataId")

        if dataId is None:
            raise Exception(f"Could not find dataId for entry {entryId} while finding path")

        return os.path.join(self.datastore, dataId)

    def getEntryData(self, entryId):
        path = self.getEntryPath(entryId)
        with open(path, "rb") as entryFile:
            return entryFile.read()

    def writeEntryData(self, entryId, content):
        path = self.getEntryPath(entryId)

        with open(path, "wb") as entryFile:
            entryFile.write(content)

    def deleteEntry(self, entryId):
        path = self.getEntryPath(entryId)

        entries = {**self.entries}
        del entries[entryId]
        self.entries = entries
        self._writeEntries(self.entries)

        try:
            os.remove(path)
        except FileNotFoundError:
            print("The underlying file did not exist.")
