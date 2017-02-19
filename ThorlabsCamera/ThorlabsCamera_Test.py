# Test Thorlabs Camera

import uc480
import matplotlib.pyplot as plt

# create instance and connect to library
cam = uc480.uc480()

# connect to first available camera
cam.connect()

# take a single image
img = cam.acquire()

# clean up
cam.disconnect()

plt.imshow(img[:,:,0], cmap='gray')
plt.colorbar()
plt.show()

print(img.shape)