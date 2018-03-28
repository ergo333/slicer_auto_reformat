lm = slicer.app.layoutManager()
redWidget = lm.sliceWidget("Red")
redController = redWidget.sliceController()

redLogic = redWidget.sliceLogic()
compositeNode = redLogic.GetSliceCompositeNode()

# Ottengo informazioni riguardo i volumi mostrati nella RedView
dataVolumeID = compositeNode.GetBackgroundVolumeID()
labelVolumeID = compositeNode.GetLabelVolumeID()

dataVolume = slicer.mrmlScene.GetNodeByID(dataVolumeID)
#labelVolume = slicer.mrmlScene.GetNodeByID(labelVolumeID)
sliceNode = redLogic.GetSliceNode()

reslice = vtk.vtkImageReslice()
reslice.SetInputConnection(dataVolume.GetImageDataConnection())
reslice.SetOutputDimensionality(2)
reslice.SetOutputExtent(0, 511, 0, 511, 0, 0)
#reslice.SetOutputOrigin(0, 0, 0)
reslice.SetInterpolationModeToLinear()

sliceTransform = vtk.vtkTransform()
sliceTransform.Identity()
#axes = vtk.vtkMatrix4x4()
#axes.DeepCopy(sliceNode.GetXYToRAS())
#reslice.SetResliceAxes(axes) 
sliceTransform.RotateZ(90)
#sliceTransform.Translate([0, 0, 0])
reslice.SetResliceAxes(sliceTransform.GetMatrix())
reslice.Update()



imageViewer = vtk.vtkImageViewer2()
imageViewer.SetInputConnection(reslice.GetOutputPort())
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
imageViewer.SetupInteractor(renderWindowInteractor);
imageViewer.Render()
imageViewer.GetRenderer().ResetCamera()
imageViewer.Render()
 
renderWindowInteractor.Start()

image = reslice.GetOutput()
windowToImageFilter = vtk.vtkWindowToImageFilter()
windowToImageFilter.SetInput(imageViewer);
#windowToImageFilter.SetMagnification(3); //set the resolution of the output image
windowToImageFilter.Update();
 
writer = vtk.vtkPNGWriter();
writer.SetFileName("/Users/eros/Desktop/screenshot2.png");
writer.SetInput(windowToImageFilter.GetOutput());

'''

table = vtk.vtkLookupTable()
table.SetRange(0, 65536)
table.SetValueRange(0.0, 1.0) # from black to white
table.SetSaturationRange(0.0, 0.0) # no color saturation
table.SetRampToLinear()
table.Build()

# Map the image through the lookup table
color = vtk.vtkImageMapToColors()
color.SetLookupTable(table)
color.SetInputConnection(reslice.GetOutputPort())

# Display the image
actor = vtk.vtkImageActor()
#actor.GetMapper().SetInputConnection(color.GetOutputPort())
actor.GetMapper().SetInputConnection(reslice.GetOutputPort())

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)

window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)
window.Render()

image = reslice.GetOutput()
'''

# non funziona -> 

'''
reslicer = vtk.vtkImageReslice()
reslicer.SetInputData(dataVolume.GetImageData())
reslicer.SetOutputDimensionality(2)
reslicer.SetInterpolationModeToLinear()
reslicer.SetOutputSpacing(dataVolume.GetSpacing())
reslicer.ReleaseDataFlagOn()

mapper = vtk.vtkImageMapper()
mapper.SetInputData(reslicer.GetOutput())
mapper.SetColorLevel(65536)
mapper.SetColorWindow(50)

actor = vtk.vtkActor2D()
actor.SetMapper(mapper)

sliceTransform = vtk.vtkTransform()
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)

sliceTransform.Identity()
sliceTransform.Translate(0, 0, 0)  # Traslo al centro

reslicer.SetResliceAxes(sliceTransform.GetMatrix())
reslicer.UpdateInformation()

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)

window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)
window.Render()
'''






















