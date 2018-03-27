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
	labelVolumeID = compositeNode.GetLabelVolumeID()

	dataVolume = slicer.mrmlScene.GetNodeByID(dataVolumeID)
	labelVolume = slicer.mrmlScene.GetNodeByID(labelVolumeID)

	# Immagine con solo il volume MR / ecografia
	compositeNode.SetBackgroundVolumeID(dataVolume.GetID())
	compositeNode.SetForegroundVolumeID(None)
	redController.setLabelMapHidden(True)

	# Salvo l'immagine png
	immagine = redWidget.imageDataConnection()
	writer = vtk.vtkPNGWriter()
	writer.SetInputConnection(immagine)
	writer.SetFileName("/home/eros/Desktop/prova.png")
	writer.Write()

	# Salvo le label
	compositeNode.SetBackgroundVolumeID(None)
	redController.setLabelMapHidden(False)

	immagineLabel = redWidget.imageDataConnection()
	writer.SetInputConnection(immagineLabel)
	writer.SetFileName("/home/eros/Desktop/prova-label.png")
	writer.Write()

	# Per ottenere le coordinate
	sliceNode = redLogic.GetSliceNode()
	sliceNode.GetSliceToRAS()

	# Creo il volume
	volumeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLScalarVolumeNode')
	volumeNode.SetImageDataConnection(immagine)

	volumeLabelNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLScalarVolumeNode')
	volumeLabelNode.SetImageDataConnection(immagineLabel)


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
rotateSlice(1, sliceSelector, lrSlider, paSlider, isSlider, offsetSlider)
rotateSlice(2, sliceSelector, lrSlider, paSlider, isSlider, offsetSlider)




