import random

#funzione a cui passo lo slice e automaticamente lo ruota nel modulo reformat
def rotateSlice(sliceId, sliceSelector, lrSlider, paSlider, isSlider, offsetSlider):
	sliceSelector.setCurrentNodeIndex(sliceId)

	# Genero i valori causali 
	# Dimezzo i limiti per evitare di uscire dal volume
	lrValue = random.uniform(lrSlider.minimum/2, lrSlider.maximum/2)
	paValue = random.uniform(paSlider.minimum/2, paSlider.maximum/2)
	isValue = random.uniform(isSlider.minimum/2, isSlider.maximum/2)
	offsetValue = random.uniform(offsetSlider.minimum/2, offsetSlider.maximum/2)

	# Calcolo lo slice attraverso il modulo Reformat
	lrSlider.setValue(lrValue)
	paSlider.setValue(paValue)
	isSlider.setValue(isValue)
	offsetSlider.setValue(offsetValue)


def export():

	lm = slicer.app.layoutManager()
	redWidget = lm.sliceWidget("Red")
	redController = redWidget.sliceController()

	redLogic = redWidget.sliceLogic()
	compositeNode = redLogic.GetSliceCompositeNode()

	# Ottengo informazioni riguardo i volumi mostrati nella RedView
	dataVolumeID = compositeNode.GetBackgroundVolumeID()
	#labelVolumeID = compositeNode.GetLabelVolumeID()

	dataVolume = slicer.mrmlScene.GetNodeByID(dataVolumeID)
	#labelVolume = slicer.mrmlScene.GetNodeByID(labelVolumeID)

	compositeNode.SetLabelVolumeID(None)

	'''
	# Calcolo un nuovo volume con un solo layer -> immagine / label
	blend = redLogic.GetBlend()
	img = blend.GetOutput()
	arrayData = img.GetPointData().GetArray(0)
	arrayImg = supp.vtk_to_numpy(arrayData)
	arrayImg = arrayImg.reshape(img.GetDimensions()[0], img.GetDimensions()[1], -1)
	'''

	sliceNode = redLogic.GetSliceNode()

	transform = sliceNode.GetSliceToRAS()  # Matrice della trasformazione dello slice
	
	#Centro lo slice
	reformat = slicer.modules.reformat.logic()
	bounds = [0, 0, 0, 0, 0, 0]
	center = [0, 0, 0]
	reformat.GetVolumeBounds(sliceNode, bounds)
	reformat.GetCenterFromBounds(bounds, center)
	transform.SetElement(0, 3, center[0])
	transform.SetElement(1, 3, center[1])	
	transform.SetElement(2, 3, center[2])

	reslice = vtk.vtkImageReslice()
	reslice.SetInputConnection(dataVolume.GetImageDataConnection())
	reslice.SetOutputDimensionality(2)
	reslice.SetOutputExtent(0, 511, 0, 511, 0, 0)
	reslice.SetInterpolationModeToLinear()
	reslice.SetResliceAxes(transform)
	reslice.Update()

	sliceNode.UpdateMatrices()

	shifter = vtk.vtkImageShiftScale()
	shifter.SetOutputScalarTypeToUnsignedShort()
	shifter.SetInputData(reslice.GetOutput())
	imageViewer = vtk.vtkImageViewer2()
	imageViewer.SetInputConnection(shifter.GetOutputPort())  # provare con reslice
	renderWindowInteractor = vtk.vtkRenderWindowInteractor()
	imageViewer.SetupInteractor(renderWindowInteractor);
	imageViewer.Render()
	#imageViewer.GetRenderer().ResetCamera()
	#imageViewer.Render()
	 
	renderWindowInteractor.Start()

	writer = vtk.vtkPNGWriter()
	writer.SetFileName('/Users/eros/Desktop/prova.png')
	writer.SetInputConnection(shifter.GetOutputPort())
	writer.Write()
	'''
	immagine = reslice.GetOutput()
	arrayData = immagine.GetPointData().GetArray(0)
	arrayImg = supp.vtk_to_numpy(arrayData)
	arrayImg = arrayImg.reshape(immagine.GetDimensions()[0], immagine.GetDimensions()[1], -1)
	import numpy as np
	#np.savetxt("/Users/eros/Desktop/img.csv", arrayImg, delimiter=",")
	'''
	'''
	immagineWidget = redLogic.GetBlend().GetOutput()
	arrayData = immagineWidget.GetPointData().GetArray(0)
	arrayImg = supp.vtk_to_numpy(arrayData)
	arrayImg = arrayImg.reshape(immagineWidget.GetDimensions()[0], immagineWidget.GetDimensions()[1], -1)
	np.savetxt("/Users/eros/Desktop/img.csv", arrayImg, delimiter=",")
	'''

	

# Accedo al modulo Reformat integrato in 3D Slicer

reformat = slicer.modules.reformat
# Per poter accedere ai "bottoni" devo creare un nuovo widget che tengo nascosto
reformatWidget = reformat.createNewWidgetRepresentation()
reformatWidget.setMRMLScene(slicer.app.mrmlScene())
#reformatWidget.show()

# Seleziono lo slice che voglio ruotare
sliceSelector = slicer.util.findChild(reformatWidget, "SliceNodeSelector")

# Prendo la sezione che gestisce le rotazioni 
rotationSection = slicer.util.findChild(reformatWidget, "RotationSlidersGroupBox")

# Prendo i riferimenti agli slider di cui devo modificare i valori per poter generare dei nuovi slices
lrSlider = slicer.util.findChild(rotationSection, "LRSlider")
paSlider = slicer.util.findChild(rotationSection, "PASlider")
isSlider = slicer.util.findChild(rotationSection, "ISSlider")

# Prendo il valore di Offset
offsetWidget = slicer.util.findChild(reformatWidget, "OffsetSlidersGroupBox")
offsetSlider = slicer.util.findChild(offsetWidget, "OffsetSlider")

rotateSlice(0, sliceSelector, lrSlider, paSlider, isSlider, offsetSlider)
reformatWidget.centerSliceNode()
rotateSlice(1, sliceSelector, lrSlider, paSlider, isSlider, offsetSlider)
reformatWidget.centerSliceNode()
rotateSlice(2, sliceSelector, lrSlider, paSlider, isSlider, offsetSlider)
reformatWidget.centerSliceNode()

export()

