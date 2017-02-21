# Test Thorlabs Camera

import uc480
import matplotlib.pyplot as plt
import time
import numpy as np

# Take single image test ----------------------------------------
if False:
	# create instance and connect to library
	cam = uc480.uc480()

	# connect to first available camera
	cam.connect()

	# take a single image
	img = cam.acquire()

	# clean up
	cam.disconnect()

	plt.imshow(img[:,:])#, cmap='gray')
	plt.colorbar()
	plt.show()

	print(img.shape)

# Multiple image test -------------------------------------------

if True:
	imgList = []
	exposure = np.linspace(100,1000,5)

	# create instance and connect to library
	cam = uc480.uc480()

	# connect to first available camera
	cam.connect()

	for i in range(len(exposure)):
		cam.set_exposure(exposure[i])
		time.sleep(0.5)
		img = cam.acquire()
		imgList.append(img)
		plt.figure()
		plt.imshow(imgList[-1], cmap='gray')

	cam.disconnect()

	plt.show()

