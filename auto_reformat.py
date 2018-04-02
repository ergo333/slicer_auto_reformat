''' Se mancano dei packages:
	> import pip
	> pip.main(['install', 'pillow==2.9.0'])
'''

import random
import numpy as np
import os, sys, dicom
from PIL import Image

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

def createDICOM(dataFile, labelFile, coord):

	outDataName = dataFile + '.dcm'
	outLabelName = labelFile + '.dcm'

	# Salvo il DICOM del dato

	ds = dicom.dataset.Dataset()
	ds.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.7' # CT Image Storage
	ds.MediaStorageSOPInstanceUID = "1.2.3"
	ds.ImplementationClassUID = "1.2.3.4"
	ds1 = dicom.dataset.FileDataset(outDataName, {}, file_meta=ds, preamble='\0'*128)
	ds1.PatientName = 'Patient1'
	ds1.PatientId = '1234'
	dataImg = Image.open(dataFile + '.jpg')
	ds1.PixelData = dataImg.tobytes()

	# The problem is that pixel data is ordered incorrectly. It will display using PIL as a raw buffer 
	# but if you want to use a DICOM viewer, you're going to make some modifications

	ds1.is_little_endian = True
	ds1.is_implicit_VR = True
	ds1.PixelRepresentation = 0
	ds1.BitsAllocated = 8
	ds1.SamplesPerPixel = 1
	ds1.NumberOfFrames = 1
	ds1.Columns = dataImg.size[0]
	ds1.Rows = dataImg.size[1]

	# Aggiungo il tag privato con le coordinate RAS (mm)
	ds1.add_new(0x0033, 'LO', coord.__str__())

	ds1.save_as(outDataName)

	# Salvo il dicom della segmentazione

	ds = dicom.dataset.Dataset()
	ds.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.7' # CT Image Storage
	ds.MediaStorageSOPInstanceUID = "1.2.3"
	ds.ImplementationClassUID = "1.2.3.4"
	ds1 = dicom.dataset.FileDataset(outLabelName, {}, file_meta=ds, preamble='\0'*128)
	ds1.PatientName = 'Patient1'
	ds1.PatientId = '1234'
	dataImg = Image.open(labelFile + '.jpg')
	ds1.PixelData = dataImg.tobytes()

	# The problem is that pixel data is ordered incorrectly. It will display using PIL as a raw buffer 
	# but if you want to use a DICOM viewer, you're going to make some modifications

	ds1.is_little_endian = True
	ds1.is_implicit_VR = True
	ds1.PixelRepresentation = 0
	ds1.BitsAllocated = 8
	ds1.SamplesPerPixel = 1
	ds1.NumberOfFrames = 1
	ds1.Columns = dataImg.size[0]
	ds1.Rows = dataImg.size[1]

	# Aggiungo il tag privato con le coordinate RAS (mm)
	ds1.add_new(0x0033, 'LO', coord.__str__())

	ds1.save_as(outLabelName)


def export(fileName, dataFolder, labelFolder):
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
	writer = vtk.vtkJPEGWriter()
	writer.SetInputConnection(immagine)
	writer.SetFileName(dataFolder + fileName + ".jpg")
	writer.Write()

	# Salvo le label
	compositeNode.SetBackgroundVolumeID(None)
	redController.setLabelMapHidden(False)

	immagineLabel = redWidget.imageDataConnection()
	writer = vtk.vtkJPEGWriter()
	writer.SetInputConnection(immagineLabel)
	writer.SetFileName(labelFolder + fileName + "-label.jpg")
	writer.Write()

	# Per ottenere le coordinate
	sliceNode = redLogic.GetSliceNode()
	ras = sliceNode.GetSliceToRAS()

	matrix = np.zeros((4, 4))

	for i in range(0, 4):
		for j in range(0, 4):
			matrix[i][j] = ras.GetElement(i, j)

	'''
	# Creo il volume
	volumeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLScalarVolumeNode')
	volumeNode.SetImageDataConnection(immagine)

	volumeLabelNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLScalarVolumeNode')
	volumeLabelNode.SetImageDataConnection(immagineLabel)
	'''
	compositeNode.SetBackgroundVolumeID(dataVolume.GetID())
	redController.setLabelMapHidden(False)

	createDICOM(dataFolder + fileName, labelFolder + fileName + '-label', matrix)


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

for i in range(0, 3000):
	rotateSlice(0, sliceSelector, lrSlider, paSlider, isSlider, offsetSlider)
	#rotateSlice(1, sliceSelector, lrSlider, paSlider, isSlider, offsetSlider)
	#rotateSlice(2, sliceSelector, lrSlider, paSlider, isSlider, offsetSlider)
	export("MRI-%05d" % i, "/home/eros/Desktop/prova/data/", "/home/eros/Desktop/prova/label/")






