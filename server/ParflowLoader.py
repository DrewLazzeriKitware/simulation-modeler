import json
import os.path
import itertools

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEFAULT_KEYS = {
    # All of these were asked for by a call to Run.run() or Run.validate()
    # These are assumed always true
    "Gravity": 1.0,
    # Domain Defaults. TODO Connect these to checkbox shortcut
    "Domain.GeomName": "domain",
    "GeomInput.Names": ["box_input"],
    "GeomInput.box_input.GeomName": ["domain"],
    "GeomInput.box_input.InputType": "Box",
    # TODO Connect these to a checkbox shortcut
    "Cycle.Names": ["constant"],
    "Cycle.constant.Repeat": -1,
    "Cycle.constant.Names": "alltime",
    "Cycle.constant.alltime.Length": 1,
    # TODO Connect these to a checkbox shortcut
    "Phase.Names": "water",
    "Phase.water.Viscosity.Value": 1.0,
    "Phase.water.Density.Type": "Constant",
    "Phase.water.Density.Value": 1.0,
    "Phase.water.Mobility.Type": "Constant",
    "Phase.water.Mobility.Value": 1.0,
}

WASHITA_KEYS = {
    # Most of these were asked for by a call to Run.run() or Run.validate()
    # These may be defaults or may not. They're from Washita
    # They may not all be necessary if I don't set domain as the name
    # TODO Connect these to a checkbox shortcut
    "Contaminants.Names": "",
    # TODO Connect these to a checkbox shortcut
    "Geom.Perm.Names": "",
    "Perm.TensorType": "TensorByGeom",
    "Phase.RelPerm.GeomNames": "",
    "Geom.Perm.TensorByGeom.Names": "",
    "Geom.Porosity.GeomNames": "",
    "SpecificStorage.GeomNames": "",
    "SpecificStorage.Type": "Constant",
    "PhaseSources.water.Type": "Constant",
    "PhaseSources.water.GeomNames": "",
    "TopoSlopesX.GeomNames": "",
    "TopoSlopesX.Type": "Constant",
    "TopoSlopesY.GeomNames": "",
    "TopoSlopesY.Type": "Constant",
    "Mannings.GeomNames": "",
    "Mannings.Type": "Constant",
    "BCPressure.PatchNames": "",
    "Wells.Names": "",
}

DOMAIN_SET_KEYS = {
    # TODO If we really want some keys to always match, set with list?
    "Geom.domain.Lower.X": "ComputationalGrid.Lower.X",
    "Geom.domain.Lower.Y": "ComputationalGrid.Lower.Y",
    "Geom.domain.Lower.Z": "ComputationalGrid.Lower.Z",
    "Geom.domain.Upper.X": "ComputationalGrid.NX",
    "Geom.domain.Upper.Y": "ComputationalGrid.NY",
    "Geom.domain.Upper.Z": "ComputationalGrid.NZ",
}

TRAME_PARFLOW_MAPPING = {
    "BaseUnit": "TimingInfo.BaseUnit",
    "DumpInterval": "TimingInfo.DumpInterval",
    "StartCount": "TimingInfo.StartCount",
    "StartTime": "TimingInfo.StartTime",
    "StopTime": "TimingInfo.StopTime",
    "LX": "ComputationalGrid.Lower.X",
    "LY": "ComputationalGrid.Lower.Y",
    "LZ": "ComputationalGrid.Lower.Z",
    "NX": "ComputationalGrid.NX",
    "NY": "ComputationalGrid.NY",
    "NZ": "ComputationalGrid.NZ",
    "DX": "ComputationalGrid.DX",
    "DY": "ComputationalGrid.DY",
    "DZ": "ComputationalGrid.DZ",
}

FULL_WASHITA = {
    "BCPressure.PatchNames": "x_lower x_upper y_lower y_upper z_lower z_upper",
    "ComputationalGrid.DX": 1000.0,
    "ComputationalGrid.DY": 1000.0,
    "ComputationalGrid.DZ": 2.0,
    "ComputationalGrid.Lower.X": 0.0,
    "ComputationalGrid.Lower.Y": 0.0,
    "ComputationalGrid.Lower.Z": 0.0,
    "ComputationalGrid.NX": 41,
    "ComputationalGrid.NY": 41,
    "ComputationalGrid.NZ": 50,
    "Contaminants.Names": "",
    "Cycle.Names": "constant rainrec",
    "Cycle.constant.Names": "alltime",
    "Cycle.constant.Repeat": -1,
    "Cycle.constant.alltime.Length": 1,
    "Cycle.rainrec.Names": "rain rec",
    "Cycle.rainrec.Repeat": -1,
    "Cycle.rainrec.rain.Length": 10,
    "Cycle.rainrec.rec.Length": 150,
    "Domain.GeomName": "domain",
    "FileVersion": 4,
    "Geom.Perm.Names": "domain s1 s2 s3 s4 s5 s6 s7 s8 s9 g2 g3 g6 g8",
    "Geom.Perm.TensorByGeom.Names": "domain",
    "Geom.Porosity.GeomNames": "domain s1 s2 s3 s4 s5 s6 s7 s8 s9",
    "Geom.domain.ICPressure.RefPatch": "z_upper",
    "Geom.domain.Lower.X": 0.0,
    "Geom.domain.Lower.Y": 0.0,
    "Geom.domain.Lower.Z": 0.0,
    "Geom.domain.Patches": "x_lower x_upper y_lower y_upper z_lower z_upper",
    "Geom.domain.Perm.TensorValX": 1.0,
    "Geom.domain.Perm.TensorValY": 1.0,
    "Geom.domain.Perm.TensorValZ": 1.0,
    "Geom.domain.Perm.Type": "Constant",
    "Geom.domain.Perm.Value": 0.2,
    "Geom.domain.Porosity.Type": "Constant",
    "Geom.domain.Porosity.Value": 0.4,
    "Geom.domain.RelPerm.Alpha": 3.5,
    "Geom.domain.RelPerm.N": 2.0,
    "Geom.domain.Saturation.Alpha": 3.5,
    "Geom.domain.Saturation.N": 2.0,
    "Geom.domain.Saturation.SRes": 0.2,
    "Geom.domain.Saturation.SSat": 1.0,
    "Geom.domain.SpecificStorage.Value": 1e-05,
    "Geom.domain.Upper.X": 41000.0,
    "Geom.domain.Upper.Y": 41000.0,
    "Geom.domain.Upper.Z": 100.0,
    "Geom.g2.Perm.Type": "Constant",
    "Geom.g2.Perm.Value": 0.025,
    "Geom.g3.Perm.Type": "Constant",
    "Geom.g3.Perm.Value": 0.059,
    "Geom.g6.Perm.Type": "Constant",
    "Geom.g6.Perm.Value": 0.2,
    "Geom.g8.Perm.Type": "Constant",
    "Geom.g8.Perm.Value": 0.68,
    "Geom.indi_input.FileName": "IndicatorFile_Gleeson.50z.pfb",
    "Geom.s1.Perm.Type": "Constant",
    "Geom.s1.Perm.Value": 0.269022595,
    "Geom.s1.Porosity.Type": "Constant",
    "Geom.s1.Porosity.Value": 0.375,
    "Geom.s1.RelPerm.Alpha": 3.548,
    "Geom.s1.RelPerm.N": 4.162,
    "Geom.s1.Saturation.Alpha": 3.548,
    "Geom.s1.Saturation.N": 4.162,
    "Geom.s1.Saturation.SRes": 1e-06,
    "Geom.s1.Saturation.SSat": 1.0,
    "Geom.s2.Perm.Type": "Constant",
    "Geom.s2.Perm.Value": 0.043630356,
    "Geom.s2.Porosity.Type": "Constant",
    "Geom.s2.Porosity.Value": 0.39,
    "Geom.s2.RelPerm.Alpha": 3.467,
    "Geom.s2.RelPerm.N": 2.738,
    "Geom.s2.Saturation.Alpha": 3.467,
    "Geom.s2.Saturation.N": 2.738,
    "Geom.s2.Saturation.SRes": 1e-06,
    "Geom.s2.Saturation.SSat": 1.0,
    "Geom.s3.Perm.Type": "Constant",
    "Geom.s3.Perm.Value": 0.015841225,
    "Geom.s3.Porosity.Type": "Constant",
    "Geom.s3.Porosity.Value": 0.387,
    "Geom.s3.RelPerm.Alpha": 2.692,
    "Geom.s3.RelPerm.N": 2.445,
    "Geom.s3.Saturation.Alpha": 2.692,
    "Geom.s3.Saturation.N": 2.445,
    "Geom.s3.Saturation.SRes": 1e-06,
    "Geom.s3.Saturation.SSat": 1.0,
    "Geom.s4.Perm.Type": "Constant",
    "Geom.s4.Perm.Value": 0.007582087,
    "Geom.s4.Porosity.Type": "Constant",
    "Geom.s4.Porosity.Value": 0.439,
    "Geom.s4.RelPerm.Alpha": 0.501,
    "Geom.s4.RelPerm.N": 2.659,
    "Geom.s4.Saturation.Alpha": 0.501,
    "Geom.s4.Saturation.N": 2.659,
    "Geom.s4.Saturation.SRes": 1e-06,
    "Geom.s4.Saturation.SSat": 1.0,
    "Geom.s5.Perm.Type": "Constant",
    "Geom.s5.Perm.Value": 0.01818816,
    "Geom.s5.Porosity.Type": "Constant",
    "Geom.s5.Porosity.Value": 0.489,
    "Geom.s5.RelPerm.Alpha": 0.661,
    "Geom.s5.RelPerm.N": 2.659,
    "Geom.s5.Saturation.Alpha": 0.661,
    "Geom.s5.Saturation.N": 2.659,
    "Geom.s5.Saturation.SRes": 1e-06,
    "Geom.s5.Saturation.SSat": 1.0,
    "Geom.s6.Perm.Type": "Constant",
    "Geom.s6.Perm.Value": 0.005009435,
    "Geom.s6.Porosity.Type": "Constant",
    "Geom.s6.Porosity.Value": 0.399,
    "Geom.s6.RelPerm.Alpha": 1.122,
    "Geom.s6.RelPerm.N": 2.479,
    "Geom.s6.Saturation.Alpha": 1.122,
    "Geom.s6.Saturation.N": 2.479,
    "Geom.s6.Saturation.SRes": 1e-06,
    "Geom.s6.Saturation.SSat": 1.0,
    "Geom.s7.Perm.Type": "Constant",
    "Geom.s7.Perm.Value": 0.005492736,
    "Geom.s7.Porosity.Type": "Constant",
    "Geom.s7.Porosity.Value": 0.384,
    "Geom.s7.RelPerm.Alpha": 2.089,
    "Geom.s7.RelPerm.N": 2.318,
    "Geom.s7.Saturation.Alpha": 2.089,
    "Geom.s7.Saturation.N": 2.318,
    "Geom.s7.Saturation.SRes": 1e-06,
    "Geom.s7.Saturation.SSat": 1.0,
    "Geom.s8.Perm.Type": "Constant",
    "Geom.s8.Perm.Value": 0.004675077,
    "Geom.s8.Porosity.Type": "Constant",
    "Geom.s8.Porosity.Value": 0.482,
    "Geom.s8.RelPerm.Alpha": 0.832,
    "Geom.s8.RelPerm.N": 2.514,
    "Geom.s8.Saturation.Alpha": 0.832,
    "Geom.s8.Saturation.N": 2.514,
    "Geom.s8.Saturation.SRes": 1e-06,
    "Geom.s8.Saturation.SSat": 1.0,
    "Geom.s9.Perm.Type": "Constant",
    "Geom.s9.Perm.Value": 0.003386794,
    "Geom.s9.Porosity.Type": "Constant",
    "Geom.s9.Porosity.Value": 0.442,
    "Geom.s9.RelPerm.Alpha": 1.585,
    "Geom.s9.RelPerm.N": 2.413,
    "Geom.s9.Saturation.Alpha": 1.585,
    "Geom.s9.Saturation.N": 2.413,
    "Geom.s9.Saturation.SRes": 1e-06,
    "Geom.s9.Saturation.SSat": 1.0,
    "GeomInput.Names": "box_input indi_input",
    "GeomInput.box_input.GeomName": "domain",
    "GeomInput.box_input.InputType": "Box",
    "GeomInput.g1.Value": 21,
    "GeomInput.g2.Value": 22,
    "GeomInput.g3.Value": 23,
    "GeomInput.g4.Value": 24,
    "GeomInput.g5.Value": 25,
    "GeomInput.g6.Value": 26,
    "GeomInput.g7.Value": 27,
    "GeomInput.g8.Value": 28,
    "GeomInput.indi_input.GeomNames": "s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 g1 g2 g3 g4 g5 g6 g7 g8",
    "GeomInput.indi_input.InputType": "IndicatorField",
    "GeomInput.s1.Value": 1,
    "GeomInput.s10.Value": 10,
    "GeomInput.s11.Value": 11,
    "GeomInput.s12.Value": 12,
    "GeomInput.s13.Value": 13,
    "GeomInput.s2.Value": 2,
    "GeomInput.s3.Value": 3,
    "GeomInput.s4.Value": 4,
    "GeomInput.s5.Value": 5,
    "GeomInput.s6.Value": 6,
    "GeomInput.s7.Value": 7,
    "GeomInput.s8.Value": 8,
    "GeomInput.s9.Value": 9,
    "Gravity": 1.0,
    "ICPressure.GeomNames": "domain",
    "ICPressure.Type": "Constant",
    "Geom.domain.ICPressure.Value": 1,
    "KnownSolution": "NoKnownSolution",
    "Mannings.Geom.domain.Value": 5.52e-06,
    "Mannings.GeomNames": "domain",
    "Mannings.Type": "Constant",
    "Patch.x_lower.BCPressure.Cycle": "constant",
    "Patch.x_lower.BCPressure.Type": "FluxConst",
    "Patch.x_lower.BCPressure.alltime.Value": 0.0,
    "Patch.x_upper.BCPressure.Cycle": "constant",
    "Patch.x_upper.BCPressure.Type": "FluxConst",
    "Patch.x_upper.BCPressure.alltime.Value": 0.0,
    "Patch.y_lower.BCPressure.Cycle": "constant",
    "Patch.y_lower.BCPressure.Type": "FluxConst",
    "Patch.y_lower.BCPressure.alltime.Value": 0.0,
    "Patch.y_upper.BCPressure.Cycle": "constant",
    "Patch.y_upper.BCPressure.Type": "FluxConst",
    "Patch.y_upper.BCPressure.alltime.Value": 0.0,
    "Patch.z_lower.BCPressure.Cycle": "constant",
    "Patch.z_lower.BCPressure.Type": "FluxConst",
    "Patch.z_lower.BCPressure.alltime.Value": 0.0,
    "Patch.z_upper.BCPressure.Cycle": "rainrec",
    "Patch.z_upper.BCPressure.Type": "OverlandFlow",
    "Patch.z_upper.BCPressure.rain.Value": -0.1,
    "Patch.z_upper.BCPressure.rec.Value": 0.0,
    "Perm.TensorType": "TensorByGeom",
    "Phase.Names": "water",
    "Phase.RelPerm.GeomNames": "domain s1 s2 s3 s4 s5 s6 s7 s8 s9",
    "Phase.RelPerm.Type": "VanGenuchten",
    "Phase.Saturation.GeomNames": "domain s1 s2 s3 s4 s5 s6 s7 s8 s9",
    "Phase.Saturation.Type": "VanGenuchten",
    "Phase.water.Density.Type": "Constant",
    "Phase.water.Density.Value": 1.0,
    "Phase.water.Mobility.Type": "Constant",
    "Phase.water.Mobility.Value": 1.0,
    "Phase.water.Viscosity.Type": "Constant",
    "Phase.water.Viscosity.Value": 1.0,
    "PhaseSources.water.Geom.domain.Value": 0.0,
    "PhaseSources.water.GeomNames": "domain",
    "PhaseSources.water.Type": "Constant",
    "Process.Topology.P": 1,
    "Process.Topology.Q": 1,
    "Process.Topology.R": 1,
    "Solver": "Richards",
    "Solver.AbsTol": 1e-08,
    "Solver.CLM.CLMDumpInterval": 1,
    "Solver.CLM.CLMFileDir": "../../clm_output/",
    "Solver.CLM.EvapBeta": "Linear",
    "Solver.CLM.FieldCapacity": 0.98,
    "Solver.CLM.IrrigationType": "none",
    "Solver.CLM.IstepStart": 1,
    "Solver.CLM.MetFileNT": 24,
    "Solver.CLM.MetFileName": "NLDAS",
    "Solver.CLM.MetFilePath": "../../NLDAS/",
    "Solver.CLM.MetForcing": "3D",
    "Solver.CLM.Print1dOut": False,
    "Solver.CLM.ResSat": 0.1,
    "Solver.CLM.VegWaterStress": "Saturation",
    "Solver.CLM.WiltingPoint": 0.12,
    "Solver.Drop": 1e-20,
    "Solver.LSM": "CLM",
    "Solver.Linear.KrylovDimension": 70,
    "Solver.Linear.MaxRestarts": 2,
    "Solver.Linear.Preconditioner": "PFMG",
    "Solver.MaxConvergenceFailures": 8,
    "Solver.MaxIter": 25000,
    "Solver.Nonlinear.DerivativeEpsilon": 1e-16,
    "Solver.Nonlinear.EtaChoice": "EtaConstant",
    "Solver.Nonlinear.EtaValue": 0.001,
    "Solver.Nonlinear.Globalization": "LineSearch",
    "Solver.Nonlinear.MaxIter": 80,
    "Solver.Nonlinear.ResidualTol": 1e-06,
    "Solver.Nonlinear.StepTol": 1e-30,
    "Solver.Nonlinear.UseJacobian": True,
    "Solver.Nonlinear.VariableDz": False,
    "Solver.PrintMask": True,
    "Solver.PrintPressure": True,
    "Solver.PrintSaturation": True,
    "Solver.PrintSubsurfData": False,
    "Solver.TerrainFollowingGrid": True,
    "SpecificStorage.GeomNames": "domain",
    "SpecificStorage.Type": "Constant",
    "TimeStep.Type": "Constant",
    "TimeStep.Value": 1.0,
    "TimingInfo.BaseUnit": 1.0,
    "TimingInfo.DumpInterval": 1.0,
    "TimingInfo.StartCount": 0.0,
    "TimingInfo.StartTime": 0.0,
    "TimingInfo.StopTime": 1000.0,
    "TopoSlopesX.GeomNames": "",
    "TopoSlopesX.Type": "Constant",
    "TopoSlopesY.GeomNames": "",
    "TopoSlopesY.Type": "Constant",
    "Wells.Names": "",
}


class ParflowLoader:
    def __init__(self, simput, defaultsFile="data/washita_run.json"):
        self.modelFile = os.path.join(BASE_DIR, "model/model.json")
        self.flatModel = None
        self.simput = simput
        self.defaultsFile = defaultsFile
        self.flattenModel()

        self.trame_parflow_mapping = TRAME_PARFLOW_MAPPING
        self.default_keys = FULL_WASHITA  # {**DEFAULT_KEYS, **WASHITA_KEYS}
        self.domain_set_keys = DOMAIN_SET_KEYS

    def load_keys(self):
        """
        Get just the solver keys in the Washita run from the old simput model
        """
        ids = []
        with open(self.defaultsFile) as runDefaults:
            pf_keys = json.load(runDefaults)
            keys = pf_keys.keys()

        solverKeys = {solverKey["id"]: solverKey for solverKey in self.flatModel}

        for key in keys:
            if key.startswith("Solver"):
                solverKey = key.replace(".", "/")
                model = solverKeys.get(solverKey)
                if model and model.get("help"):
                    obj = self.simput.create("SearchKey")
                    self._set(obj.id, "key", solverKey)
                    self._set(obj.id, "description", model.get("help"))
                    ids.append(obj.id)
                else:
                    print("Couldn't place", key)
                    print("corresponding to value", pf_keys[key])
        return ids

    def _set(self, entry_id, name, value):
        self.simput.update([{"id": entry_id, "name": name, "value": value}])

    def generate_search_index(self):
        index = {
            s.id: self.searchText(s)
            for s in self.simput.get_instances_of_type("SearchKey")
        }
        solverSearchIds = list(index.keys())
        return index

    def searchText(self, proxy):
        return proxy.get_property("description") + proxy.get_property("key")

    def flattenModel(self):
        with open(self.modelFile) as mf:
            original = json.load(mf)

        values = original.get("definitions").values()
        parameters = [value.get("parameters") for value in values]
        self.flatModel = itertools.chain(*parameters)
