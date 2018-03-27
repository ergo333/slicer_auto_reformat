lm = slicer.app.layoutManager()
redWidget = lm.sliceWidget("Red")
redController = redWidget.sliceController()

redLogic = redWidget.sliceLogic()
compositeNode = redLogic.GetSliceCompositeNode()

# Ottengo informazioni riguardo i volumi mostrati nella RedView
dataVolumeID = compositeNode.GetBackgroundVolumeID()
labelVolumeID = compositeNode.GetLabelVolumeID()

dataVolume = slicer.mrmlScene.GetNodeByID(dataVolumeID)
labelVolume = slicer.mrmlScene.GetNodeByID(labelVolumeID)
sliceNode = redLogic.GetSliceNode()

reslice = vtk.vtkImageReslice()
reslice.SetInputConnection(dataVolume.GetImageDataConnection())
reslice.SetOutputDimensionality(2)
reslice.SetOutputExtent(0, 511, 0, 511, 0, 0)
reslice.SetOutputOrigin(0, 0, 0)
reslice.SetInterpolationModeToLinear()
axes = vtk.vtkMatrix4x4()
axes.DeepCopy(transformation.GetMatrix())
reslice.SetResliceAxes(axes)	