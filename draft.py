# SCRIPT TO RUN LITTLE WASHITA DOMAIN WITH TERRAIN-FOLLOWING GRID
#
# This script has been reorganized and commented on to draft a
# parflow-web interface, but should still function as a script.

from parflow import Run
from parflow.tools.fs import mkdir, cp, get_absolute_path
from parflow.tools.settings import set_working_directory

# -----------------------------------------------------------------------------
#  ____        _            _     _
# | __ )  __ _| | _____  __| |   (_)_ __
# |  _ \ / _` | |/ / _ \/ _` |   | | '_ \
# | |_) | (_| |   <  __/ (_| |   | | | | |
# |____/ \__,_|_|\_\___|\__,_|   |_|_| |_|
#
# Baked in decisions - These are the assumptions for anything built with this interface
# -----------------------------------------------------------------------------


# We require an indicator file through the File Database below
# Assume there is one indicator file and one box around it
LW_Test.GeomInput.Names = "box_input indi_input"

# We base a "domain" box geometry on the required indicator
# through the File Database below
# Normal water (using DomainBuilder.water("domain"))
LW_Test.Gravity = 1.0
LW_Test.Phase.Names = "water"
LW_Test.Phase.water.Density.Type = "Constant"
LW_Test.Phase.water.Density.Value = 1.0
LW_Test.Phase.water.Viscosity.Type = "Constant"
LW_Test.Phase.water.Viscosity.Value = 1.0
LW_Test.Phase.water.Mobility.Type = "Constant"
LW_Test.Phase.water.Mobility.Value = 1.0
LW_Test.PhaseSources.water.Type = "Constant"
LW_Test.PhaseSources.water.GeomNames = "domain"
LW_Test.PhaseSources.water.Geom.domain.Value = 0.0

# -----------------------------------------------------------------------------
#  ____  _                _             _
# / ___|| |__   ___  _ __| |_ ___ _   _| |_ ___
# \___ \| '_ \ / _ \| '__| __/ __| | | | __/ __|
#  ___) | | | | (_) | |  | || (__| |_| | |_\__ \
# |____/|_| |_|\___/|_|   \__\___|\__,_|\__|___/
#
# Shortcuts - Users can pick between these on the shortcuts page
# -----------------------------------------------------------------------------
# TODO Add interface for non-empty options
LW_Test.Contaminants.Names = ""  # Via DomainBuilder.no_contaminants()
LW_Test.Wells.Names = ""  # Via DomainBuilder.no_wells()

# DB.full_saturated() and variably_saturated() are options here too,
# but this script customizes them more so they appear in the solver.

# -----------------------------------------------------------------------------
#  ___       _             __
# |_ _|_ __ | |_ ___ _ __ / _| __ _  ___ ___
#  | || '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
#  | || | | | ||  __/ |  |  _| (_| | (_|  __/
# |___|_| |_|\__\___|_|  |_|  \__,_|\___\___|
#
# -----------------------------------------------------------------------------
# Page for File Database
# -----------------------------------------------------------------------------

mkdir("output")
set_working_directory(get_absolute_path("output"))

# ParFlow Inputs
cp("../../parflow_input/LW.slopex.pfb")
cp("../../parflow_input/LW.slopey.pfb")
cp("../../parflow_input/IndicatorFile_Gleeson.50z.pfb")
cp("../../parflow_input/press.init.pfb")

# CLM Inputs
cp("../../clm_input/drv_clmin.dat")
cp("../../clm_input/drv_vegp.dat")
cp("../../clm_input/drv_vegm.alluv.dat")


# A zip of all of these is one kind of entry in the file database
directories = [
    "qflx_evap_grnd",
    "eflx_lh_tot",
    "qflx_evap_tot",
    "qflx_tran_veg",
    "correct_output",
    "qflx_infl",
    "swe_out",
    "eflx_lwrad_out",
    "t_grnd",
    "diag_out",
    "qflx_evap_soi",
    "eflx_soil_grnd",
    "eflx_sh_tot",
    "qflx_evap_veg",
    "qflx_top_soil",
]
for directory in directories:
    mkdir(f"../../clm_output/{directory}")

# Indicator file is required to advance from File Database
LW_Test.Geom.indi_input.FileName = "IndicatorFile_Gleeson.50z.pfb"
LW_Test.GeomInput.indi_input.InputType = "IndicatorField"
LW_Test = Run("LW_Test", __file__)  # Set by indicator name
LW_Test.FileVersion = 4  # Assumed

# -----------------------------------------------------------------------------
# Page for Geometry
# -----------------------------------------------------------------------------
# We can get N{XYZ} from PFImage("Indicator.pfb").size()
# Initialize xyz to 0, but let them change it
# Initialize D{xyz} to 1000.0, 1000.0, 2.0 - those seem reasonable for land
# -----------------------------------------------------------------------------

LW_Test.ComputationalGrid.Lower.X = 0.0
LW_Test.ComputationalGrid.Lower.Y = 0.0
LW_Test.ComputationalGrid.Lower.Z = 0.0

LW_Test.ComputationalGrid.DX = 1000.0
LW_Test.ComputationalGrid.DY = 1000.0
LW_Test.ComputationalGrid.DZ = 2.0

LW_Test.ComputationalGrid.NX = 41
LW_Test.ComputationalGrid.NY = 41
LW_Test.ComputationalGrid.NZ = 50

# Assume box is domain, lower are 0, upper are multiplied from ComputationalGrid
LW_Test.GeomInput.box_input.InputType = "Box"
LW_Test.GeomInput.box_input.GeomName = "domain"
LW_Test.Domain.GeomName = "domain"
LW_Test.Geom.domain.Lower.X = 0.0
LW_Test.Geom.domain.Lower.Y = 0.0
LW_Test.Geom.domain.Lower.Z = 0.0

LW_Test.Geom.domain.Upper.X = 41000.0
LW_Test.Geom.domain.Upper.Y = 41000.0
LW_Test.Geom.domain.Upper.Z = 100.0
LW_Test.Geom.domain.Patches = "x_lower x_upper y_lower y_upper z_lower z_upper"

LW_Test.TopoSlopesY.GeomNames = "domain"
LW_Test.TopoSlopesX.GeomNames = "domain"

LW_Test.TopoSlopesX.Type = "PFBFile"
LW_Test.TopoSlopesX.FileName = "LW.slopex.pfb"
LW_Test.TopoSlopesY.Type = "PFBFile"
LW_Test.TopoSlopesY.FileName = "LW.slopey.pfb"

LW_Test.Mannings.Type = "Constant"
LW_Test.Mannings.GeomNames = "domain"
LW_Test.Mannings.Geom.domain.Value = 5.52e-6

# -----------------------------------------------------------------------------
# Initial conditions: water pressure
# -----------------------------------------------------------------------------

LW_Test.ICPressure.Type = "PFBFile"
LW_Test.ICPressure.GeomNames = "domain"
LW_Test.Geom.domain.ICPressure.RefPatch = "z_upper"
LW_Test.Geom.domain.ICPressure.FileName = "press.init.pfb"


# -----------------------------------------------------------------------------
# Page for Subsurface
# -----------------------------------------------------------------------------
# Initial Soil properties page allows all inputs to DomainBuilder.homogeneous_subsurface.
# -----------------------------------------------------------------------------
LW_Test.Perm.TensorType = "TensorByGeom"
LW_Test.Geom.domain.Perm.TensorValX = 1.0
LW_Test.Geom.domain.Perm.TensorValY = 1.0
LW_Test.Geom.domain.Perm.TensorValZ = 1.0
# Set if above are set
LW_Test.Geom.Perm.TensorByGeom.Names = "domain"


# -----------------------------------------------------------------------------
# The Values will prefill a table, and names can be added
# -----------------------------------------------------------------------------
LW_Test.GeomInput.s1.Value = 1
LW_Test.GeomInput.s2.Value = 2
LW_Test.GeomInput.s3.Value = 3
LW_Test.GeomInput.s4.Value = 4
LW_Test.GeomInput.s5.Value = 5
LW_Test.GeomInput.s6.Value = 6
LW_Test.GeomInput.s7.Value = 7
LW_Test.GeomInput.s8.Value = 8
LW_Test.GeomInput.s9.Value = 9
LW_Test.GeomInput.s10.Value = 10
LW_Test.GeomInput.s11.Value = 11
LW_Test.GeomInput.s12.Value = 12
LW_Test.GeomInput.s13.Value = 13
LW_Test.GeomInput.g1.Value = 21
LW_Test.GeomInput.g2.Value = 22
LW_Test.GeomInput.g3.Value = 23
LW_Test.GeomInput.g4.Value = 24
LW_Test.GeomInput.g5.Value = 25
LW_Test.GeomInput.g6.Value = 26
LW_Test.GeomInput.g7.Value = 27
LW_Test.GeomInput.g8.Value = 28

# Names will be auto filled by presence of values in table
LW_Test.GeomInput.indi_input.GeomNames = (
    "s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 g1 g2 g3 g4 g5 g6 g7 g8"
)
LW_Test.Geom.Perm.Names = "domain s1 s2 s3 s4 s5 s6 s7 s8 s9 g2 g3 g6 g8"
LW_Test.Geom.Porosity.GeomNames = "domain s1 s2 s3 s4 s5 s6 s7 s8 s9"
LW_Test.Phase.RelPerm.GeomNames = "domain s1 s2 s3 s4 s5 s6 s7 s8 s9"
LW_Test.Phase.Saturation.GeomNames = "domain s1 s2 s3 s4 s5 s6 s7 s8 s9"


# -----------------------------------------------------------------------------
# Permeability (values in m/hr)
# -----------------------------------------------------------------------------

LW_Test.Geom.domain.Perm.Type = "Constant"
LW_Test.Geom.domain.Perm.Value = 0.2

LW_Test.Geom.s1.Perm.Type = "Constant"
LW_Test.Geom.s1.Perm.Value = 0.269022595

LW_Test.Geom.s2.Perm.Type = "Constant"
LW_Test.Geom.s2.Perm.Value = 0.043630356

LW_Test.Geom.s3.Perm.Type = "Constant"
LW_Test.Geom.s3.Perm.Value = 0.015841225

LW_Test.Geom.s4.Perm.Type = "Constant"
LW_Test.Geom.s4.Perm.Value = 0.007582087

LW_Test.Geom.s5.Perm.Type = "Constant"
LW_Test.Geom.s5.Perm.Value = 0.01818816

LW_Test.Geom.s6.Perm.Type = "Constant"
LW_Test.Geom.s6.Perm.Value = 0.005009435

LW_Test.Geom.s7.Perm.Type = "Constant"
LW_Test.Geom.s7.Perm.Value = 0.005492736

LW_Test.Geom.s8.Perm.Type = "Constant"
LW_Test.Geom.s8.Perm.Value = 0.004675077

LW_Test.Geom.s9.Perm.Type = "Constant"
LW_Test.Geom.s9.Perm.Value = 0.003386794

LW_Test.Geom.g2.Perm.Type = "Constant"
LW_Test.Geom.g2.Perm.Value = 0.025

LW_Test.Geom.g3.Perm.Type = "Constant"
LW_Test.Geom.g3.Perm.Value = 0.059

LW_Test.Geom.g6.Perm.Type = "Constant"
LW_Test.Geom.g6.Perm.Value = 0.2

LW_Test.Geom.g8.Perm.Type = "Constant"
LW_Test.Geom.g8.Perm.Value = 0.68


# -----------------------------------------------------------------------------
# Porosity
# -----------------------------------------------------------------------------


LW_Test.Geom.domain.Porosity.Type = "Constant"
LW_Test.Geom.domain.Porosity.Value = 0.4

LW_Test.Geom.s1.Porosity.Type = "Constant"
LW_Test.Geom.s1.Porosity.Value = 0.375

LW_Test.Geom.s2.Porosity.Type = "Constant"
LW_Test.Geom.s2.Porosity.Value = 0.39

LW_Test.Geom.s3.Porosity.Type = "Constant"
LW_Test.Geom.s3.Porosity.Value = 0.387

LW_Test.Geom.s4.Porosity.Type = "Constant"
LW_Test.Geom.s4.Porosity.Value = 0.439

LW_Test.Geom.s5.Porosity.Type = "Constant"
LW_Test.Geom.s5.Porosity.Value = 0.489

LW_Test.Geom.s6.Porosity.Type = "Constant"
LW_Test.Geom.s6.Porosity.Value = 0.399

LW_Test.Geom.s7.Porosity.Type = "Constant"
LW_Test.Geom.s7.Porosity.Value = 0.384

LW_Test.Geom.s8.Porosity.Type = "Constant"
LW_Test.Geom.s8.Porosity.Value = 0.482

LW_Test.Geom.s9.Porosity.Type = "Constant"
LW_Test.Geom.s9.Porosity.Value = 0.442
# -----------------------------------------------------------------------------
# Relative Permeability
# -----------------------------------------------------------------------------

LW_Test.Phase.RelPerm.Type = "VanGenuchten"

LW_Test.Geom.domain.RelPerm.Alpha = 3.5
LW_Test.Geom.domain.RelPerm.N = 2.0

LW_Test.Geom.s1.RelPerm.Alpha = 3.548
LW_Test.Geom.s1.RelPerm.N = 4.162

LW_Test.Geom.s2.RelPerm.Alpha = 3.467
LW_Test.Geom.s2.RelPerm.N = 2.738

LW_Test.Geom.s3.RelPerm.Alpha = 2.692
LW_Test.Geom.s3.RelPerm.N = 2.445

LW_Test.Geom.s4.RelPerm.Alpha = 0.501
LW_Test.Geom.s4.RelPerm.N = 2.659

LW_Test.Geom.s5.RelPerm.Alpha = 0.661
LW_Test.Geom.s5.RelPerm.N = 2.659

LW_Test.Geom.s6.RelPerm.Alpha = 1.122
LW_Test.Geom.s6.RelPerm.N = 2.479

LW_Test.Geom.s7.RelPerm.Alpha = 2.089
LW_Test.Geom.s7.RelPerm.N = 2.318

LW_Test.Geom.s8.RelPerm.Alpha = 0.832
LW_Test.Geom.s8.RelPerm.N = 2.514

LW_Test.Geom.s9.RelPerm.Alpha = 1.585
LW_Test.Geom.s9.RelPerm.N = 2.413

# -----------------------------------------------------------------------------
# Saturation
# -----------------------------------------------------------------------------

LW_Test.Phase.Saturation.Type = "VanGenuchten"

LW_Test.Geom.domain.Saturation.Alpha = 3.5
LW_Test.Geom.domain.Saturation.N = 2.0
LW_Test.Geom.domain.Saturation.SRes = 0.2
LW_Test.Geom.domain.Saturation.SSat = 1.0

LW_Test.Geom.s1.Saturation.Alpha = 3.548
LW_Test.Geom.s1.Saturation.N = 4.162
LW_Test.Geom.s1.Saturation.SRes = 0.000001
LW_Test.Geom.s1.Saturation.SSat = 1.0

LW_Test.Geom.s2.Saturation.Alpha = 3.467
LW_Test.Geom.s2.Saturation.N = 2.738
LW_Test.Geom.s2.Saturation.SRes = 0.000001
LW_Test.Geom.s2.Saturation.SSat = 1.0

LW_Test.Geom.s3.Saturation.Alpha = 2.692
LW_Test.Geom.s3.Saturation.N = 2.445
LW_Test.Geom.s3.Saturation.SRes = 0.000001
LW_Test.Geom.s3.Saturation.SSat = 1.0

LW_Test.Geom.s4.Saturation.Alpha = 0.501
LW_Test.Geom.s4.Saturation.N = 2.659
LW_Test.Geom.s4.Saturation.SRes = 0.000001
LW_Test.Geom.s4.Saturation.SSat = 1.0

LW_Test.Geom.s5.Saturation.Alpha = 0.661
LW_Test.Geom.s5.Saturation.N = 2.659
LW_Test.Geom.s5.Saturation.SRes = 0.000001
LW_Test.Geom.s5.Saturation.SSat = 1.0

LW_Test.Geom.s6.Saturation.Alpha = 1.122
LW_Test.Geom.s6.Saturation.N = 2.479
LW_Test.Geom.s6.Saturation.SRes = 0.000001
LW_Test.Geom.s6.Saturation.SSat = 1.0

LW_Test.Geom.s7.Saturation.Alpha = 2.089
LW_Test.Geom.s7.Saturation.N = 2.318
LW_Test.Geom.s7.Saturation.SRes = 0.000001
LW_Test.Geom.s7.Saturation.SSat = 1.0

LW_Test.Geom.s8.Saturation.Alpha = 0.832
LW_Test.Geom.s8.Saturation.N = 2.514
LW_Test.Geom.s8.Saturation.SRes = 0.000001
LW_Test.Geom.s8.Saturation.SSat = 1.0

LW_Test.Geom.s9.Saturation.Alpha = 1.585
LW_Test.Geom.s9.Saturation.N = 2.413
LW_Test.Geom.s9.Saturation.SRes = 0.000001
LW_Test.Geom.s9.Saturation.SSat = 1.0


# -----------------------------------------------------------------------------
# Solver page
# -----------------------------------------------------------------------------
# The VariablySaturated | FullySaturated shortcut may set some of these following DomainBuilder
# They'll all appear in the Solver page regardless
# -----------------------------------------------------------------------------

LW_Test.Solver = "Richards"
LW_Test.Solver.TerrainFollowingGrid = True
LW_Test.Solver.Nonlinear.VariableDz = False

LW_Test.Solver.MaxIter = 25000
LW_Test.Solver.Drop = 1e-20
LW_Test.Solver.AbsTol = 1e-8
LW_Test.Solver.MaxConvergenceFailures = 8
LW_Test.Solver.Nonlinear.MaxIter = 80
LW_Test.Solver.Nonlinear.ResidualTol = 1e-6

## new solver settings for Terrain Following Grid
LW_Test.Solver.Nonlinear.EtaChoice = "EtaConstant"
LW_Test.Solver.Nonlinear.EtaValue = 0.001
LW_Test.Solver.Nonlinear.UseJacobian = True
LW_Test.Solver.Nonlinear.DerivativeEpsilon = 1e-16
LW_Test.Solver.Nonlinear.StepTol = 1e-30
LW_Test.Solver.Nonlinear.Globalization = "LineSearch"
LW_Test.Solver.Linear.KrylovDimension = 70
LW_Test.Solver.Linear.MaxRestarts = 2

LW_Test.Solver.Linear.Preconditioner = "PFMG"

LW_Test.Solver.PrintSubsurfData = False
LW_Test.Solver.PrintPressure = True
LW_Test.Solver.PrintSaturation = True
LW_Test.Solver.PrintMask = True
LW_Test.KnownSolution = "NoKnownSolution"
LW_Test.TimingInfo.BaseUnit = 1.0
LW_Test.TimingInfo.StartCount = 0.0
LW_Test.TimingInfo.StartTime = 0.0
LW_Test.TimingInfo.StopTime = 1000.0
LW_Test.TimingInfo.DumpInterval = 1.0
LW_Test.TimeStep.Type = "Constant"
LW_Test.TimeStep.Value = 1.0
LW_Test.Process.Topology.P = 1
LW_Test.Process.Topology.Q = 1
LW_Test.Process.Topology.R = 1


#                  _           _     _          _
#  _   _ _ __   __| | ___  ___(_) __| | ___  __| |
# | | | | '_ \ / _` |/ _ \/ __| |/ _` |/ _ \/ _` |
# | |_| | | | | (_| |  __/ (__| | (_| |  __/ (_| |
#  \__,_|_| |_|\__,_|\___|\___|_|\__,_|\___|\__,_|
# -----------------------------------------------------------------------------
# ----------------------------------------------------------------
# CLM Settings:
# ----------------------------------------------------------------

LW_Test.Solver.LSM = "CLM"
LW_Test.Solver.CLM.CLMFileDir = "../../clm_output/"
LW_Test.Solver.CLM.Print1dOut = False
LW_Test.Solver.BinaryOutDir = False
LW_Test.Solver.CLM.CLMDumpInterval = 1

LW_Test.Solver.CLM.MetForcing = "3D"
LW_Test.Solver.CLM.MetFileName = "NLDAS"
LW_Test.Solver.CLM.MetFilePath = "../../NLDAS/"
LW_Test.Solver.CLM.MetFileNT = 24
LW_Test.Solver.CLM.IstepStart = 1

LW_Test.Solver.CLM.EvapBeta = "Linear"
LW_Test.Solver.CLM.VegWaterStress = "Saturation"
LW_Test.Solver.CLM.ResSat = 0.1
LW_Test.Solver.CLM.WiltingPoint = 0.12
LW_Test.Solver.CLM.FieldCapacity = 0.98
LW_Test.Solver.CLM.IrrigationType = "none"
# -----------------------------------------------------------------------------
# Boundary Conditions
# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

LW_Test.BCPressure.PatchNames = LW_Test.Geom.domain.Patches

LW_Test.Patch.x_lower.BCPressure.Type = "FluxConst"
LW_Test.Patch.x_lower.BCPressure.Cycle = "constant"
LW_Test.Patch.x_lower.BCPressure.alltime.Value = 0.0

LW_Test.Patch.y_lower.BCPressure.Type = "FluxConst"
LW_Test.Patch.y_lower.BCPressure.Cycle = "constant"
LW_Test.Patch.y_lower.BCPressure.alltime.Value = 0.0

LW_Test.Patch.z_lower.BCPressure.Type = "FluxConst"
LW_Test.Patch.z_lower.BCPressure.Cycle = "constant"
LW_Test.Patch.z_lower.BCPressure.alltime.Value = 0.0

LW_Test.Patch.x_upper.BCPressure.Type = "FluxConst"
LW_Test.Patch.x_upper.BCPressure.Cycle = "constant"
LW_Test.Patch.x_upper.BCPressure.alltime.Value = 0.0

LW_Test.Patch.y_upper.BCPressure.Type = "FluxConst"
LW_Test.Patch.y_upper.BCPressure.Cycle = "constant"
LW_Test.Patch.y_upper.BCPressure.alltime.Value = 0.0

LW_Test.Patch.z_upper.BCPressure.Type = "OverlandFlow"
LW_Test.Patch.z_upper.BCPressure.Cycle = "rainrec"
LW_Test.Patch.z_upper.BCPressure.rain.Value = -0.1
LW_Test.Patch.z_upper.BCPressure.rec.Value = 0.0000

# -----------------------------------------------------------------------------
# Time Cycles
# -----------------------------------------------------------------------------

LW_Test.Cycle.Names = "constant rainrec"
LW_Test.Cycle.constant.Names = "alltime"
LW_Test.Cycle.constant.alltime.Length = 1
LW_Test.Cycle.constant.Repeat = -1

LW_Test.Cycle.rainrec.Names = "rain rec"
LW_Test.Cycle.rainrec.rain.Length = 10.0
LW_Test.Cycle.rainrec.rec.Length = 150.0
LW_Test.Cycle.rainrec.Repeat = -1


# -----------------------------------------------------------------------------
# Distribute inputs
# -----------------------------------------------------------------------------

LW_Test.dist("LW.slopex.pfb")
LW_Test.dist("LW.slopey.pfb")

LW_Test.dist("IndicatorFile_Gleeson.50z.pfb")
LW_Test.dist("press.init.pfb")

# -----------------------------------------------------------------------------
# Run Simulation
# -----------------------------------------------------------------------------

LW_Test.run()
