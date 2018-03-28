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
reslice.SetInterpolationModeToLinear()

sliceTransform = vtk.vtkTransform()
sliceTransform.Identity()
sliceTransform.RotateX(30)

reslice.SetResliceAxes(sliceTransform.GetMatrix())
reslice.Update()

sliceNode.GetSliceToRAS().DeepCopy(sliceTransform.GetMatrix())
sliceNode.UpdateMatrices()

imageViewer = vtk.vtkImageViewer2()
imageViewer.SetInputConnection(reslice.GetOutputPort())
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
imageViewer.SetupInteractor(renderWindowInteractor);
imageViewer.Render()
imageViewer.GetRenderer().ResetCamera()
imageViewer.Render()
 
renderWindowInteractor.Start()
