 # generated using paraview version 5.8.1
 #
 # To ensure correct image size when batch processing, please search 
 # for and uncomment the line `# renderView*.ViewSize = [*,*]`

 #### import the simple module from the paraview
 from paraview.simple import *
 #### disable automatic camera reset on 'Show'
 paraview.simple._DisableFirstRenderCameraReset()

 # create a new 'PFB reader'
 lW_Testoutpress0000 = PFBreader(FileNames=['/home/drew/Desktop/washita/py_scripts/output/LW_Test.out.press.00000.pfb', '/home/drew/Desktop/washita/py_scripts/output/LW_Test.out.press.00001.pfb', '/home/drew/Desktop/washita/py_scripts/output/LW_Test.out.press.00002.pfb', '/home/drew/Desktop/washita/py_scripts/output/LW_Test.out.press.00003.pfb', '/home/drew/Desktop/washita/py_scripts/output/LW_Test.out.press.00004.pfb', '/home/drew/Desktop/washita/py_scripts/output/LW_Test.out.press.00005.pfb', '/home/drew/Desktop/washita/py_scripts/output/LW_Test.out.press.00006.pfb', '/home/drew/Desktop/washita/py_scripts/output/LW_Test.out.press.00007.pfb'])

 # get animation scene
 animationScene1 = GetAnimationScene()

 # get the time-keeper
 timeKeeper1 = GetTimeKeeper()

 # update animation scene based on data timesteps
 animationScene1.UpdateAnimationUsingDataTimeSteps()

 # get active view
 renderView1 = GetActiveViewOrCreate('RenderView')
 # uncomment following to set a specific view size
 # renderView1.ViewSize = [991, 555]

 # get layout
 layout1 = GetLayout()

 # show data in view
 lW_Testoutpress0000Display = Show(lW_Testoutpress0000, renderView1, 'GeometryRepresentation')

 # trace defaults for the display properties.
 lW_Testoutpress0000Display.Representation = 'Outline'
 lW_Testoutpress0000Display.ColorArrayName = ['CELLS', '']
 lW_Testoutpress0000Display.OSPRayScaleFunction = 'PiecewiseFunction'
 lW_Testoutpress0000Display.SelectOrientationVectors = 'None'
 lW_Testoutpress0000Display.ScaleFactor = 4100.0
 lW_Testoutpress0000Display.SelectScaleArray = 'press'
 lW_Testoutpress0000Display.GlyphType = 'Arrow'
 lW_Testoutpress0000Display.GlyphTableIndexArray = 'press'
 lW_Testoutpress0000Display.GaussianRadius = 205.0
 lW_Testoutpress0000Display.SetScaleArray = [None, '']
 lW_Testoutpress0000Display.ScaleTransferFunction = 'PiecewiseFunction'
 lW_Testoutpress0000Display.OpacityArray = [None, '']
 lW_Testoutpress0000Display.OpacityTransferFunction = 'PiecewiseFunction'
 lW_Testoutpress0000Display.DataAxesGrid = 'GridAxesRepresentation'
 lW_Testoutpress0000Display.PolarAxes = 'PolarAxesRepresentation'

 # reset view to fit data
 renderView1.ResetCamera()

 # get the material library
 materialLibrary1 = GetMaterialLibrary()

 # update the view to ensure updated data information
 renderView1.Update()

 # change representation type
 lW_Testoutpress0000Display.SetRepresentationType('Surface')

 # set scalar coloring
 ColorBy(lW_Testoutpress0000Display, ('CELLS', 'press'))

 # rescale color and/or opacity maps used to include current data range
 lW_Testoutpress0000Display.RescaleTransferFunctionToDataRange(True, False)

 # show color bar/color legend
 lW_Testoutpress0000Display.SetScalarBarVisibility(renderView1, True)

 # get color transfer function/color map for 'press'
 pressLUT = GetColorTransferFunction('press')

 # get opacity transfer function/opacity map for 'press'
 pressPWF = GetOpacityTransferFunction('press')

 # Properties modified on animationScene1
 animationScene1.AnimationTime = 1.0

 # Properties modified on animationScene1
 animationScene1.AnimationTime = 2.0

 # Properties modified on animationScene1
 animationScene1.AnimationTime = 3.0

 # Properties modified on animationScene1
 animationScene1.AnimationTime = 4.0

 # Properties modified on animationScene1
 animationScene1.AnimationTime = 5.0

 # Properties modified on animationScene1
 animationScene1.AnimationTime = 6.0

 # Properties modified on animationScene1
 animationScene1.AnimationTime = 7.0

 #### saving camera placements for all active views

 # current camera placement for renderView1
 renderView1.CameraPosition = [11273.144042086713, -66486.47790219051, 70017.2060815514]
 renderView1.CameraFocalPoint = [20500.0, 20500.0, 50.0]
 renderView1.CameraViewUp = [-0.03097803960072764, 0.6284499397914619, 0.777232934350188]
 renderView1.CameraParallelScale = 28991.421144883534

 #### uncomment the following to render all views
 # RenderAllViews()
 # alternatively, if you want to write images, you can use SaveScreenshot(...).
