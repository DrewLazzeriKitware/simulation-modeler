import os
import os.path
import random
import yaml

from typing import Optional

from enum import Enum

from singleton import Singleton
from trame import state, trigger


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
            raise Exception(
                f"Could not find dataId for entry {entryId} while finding path"
            )

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


@state.change("dbSelectedFile")
def changeCurrentFile(dbSelectedFile, dbFiles, **kwargs):
    if dbSelectedFile is None:
        return

    file_id = dbSelectedFile.get("id")

    if not file_id:
        dbSelectedFile = FileDatabase().addNewEntry(dbSelectedFile)
    else:
        currentEntry = FileDatabase().getEntry(file_id)
        dbSelectedFile = {**currentEntry, **dbSelectedFile}
        FileDatabase().writeEntry(file_id, dbSelectedFile)

    state.dbSelectedFile = dbSelectedFile
    state.flush("dbSelectedFile")
    state.dbFiles = FileDatabase().getEntries()


@state.change("indicatorFile")
def updateComputationalGrid(indicatorFile, **kwargs):
    entry = FileDatabase().getEntry(indicatorFile)
    state.indicatorFileDescription = entry.get("description")

    filename = FileDatabase().getEntryPath(indicatorFile)
    try:
        handle = PFData(filename)
    except:
        print(f"Could not find pfb: {filename}")
        return
    handle.loadHeader()

    state.NX = handle.getNX()
    state.NY = handle.getNY()
    state.NZ = handle.getNZ()

    state.LX = handle.getX()
    state.LY = handle.getY()
    state.LZ = handle.getZ()

    state.DX = handle.getDX()
    state.DY = handle.getDY()
    state.DZ = handle.getDZ()


@state.change("dbFileExchange")
def saveUploadedFile(dbFileExchange=None, dbSelectedFile=None, sharedir=None, **kwargs):
    if dbFileExchange is None or dbSelectedFile is None or sharedir is None:
        return

    fileMeta = {
        key: dbFileExchange.get(key)
        for key in ["origin", "size", "dateModified", "dateUploaded", "type"]
    }
    entryId = dbSelectedFile.get("id")

    try:
        # File was uploaded from the user browser
        if dbFileExchange.get("content"):
            FileDatabase().writeEntryData(entryId, dbFileExchange["content"])
        # Path to file already present on the server was specified
        elif dbFileExchange.get("localFile"):
            file_path = os.path.abspath(
                os.path.join(sharedir, dbFileExchange.get("localFile"))
            )
            if os.path.commonpath([sharedir, file_path]) != sharedir:
                raise Exception("Attempting to access a file outside the sharedir.")
            fileMeta["origin"] = os.path.basename(file_path)

            with open(file_path, "rb") as f:
                content = f.read()
                fileMeta["size"] = len(content)
                FileDatabase().writeEntryData(entryId, content)
    except Exception as e:
        print(e)
        state.uploadError = "An error occurred uploading the file to the database."
        return

    entry = {**FileDatabase().getEntry(entryId), **fileMeta}
    FileDatabase().writeEntry(entryId, entry)
    state.dbSelectedFile = entry
    state.flush("dbSelectedFile")


@trigger("updateFiles")
def updateFiles(update, entryId=None):
    if update == "selectFile":
        if state.dbFiles.get(entryId):
            state.dbSelectedFile = FileDatabase().getEntry(entryId)

    elif update == "removeFile":
        FileDatabase().deleteEntry(entryId)
        state.dbFiles = FileDatabase().getEntries()
        if entryId == state.dbSelectedFile.get("id"):
            state.dbSelectedFile = None
            state.flush("dbSelectedFile")
        state.flush("dbFiles")

    elif update == "downloadSelectedFile":
        state.dbFileExchange = FileDatabase().getEntryData(entryId)

    state.uploadError = ""
