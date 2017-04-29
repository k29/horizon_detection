import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3 
import matplotlib.pyplot as plt 
from PIL import Image
import cv2

def plotPixelData(old_path, scale):
	#opening and resizing an image in PIL
	img_file = Image.open(old_path)
	[xSize, ySize] = img_file.size
	img_file = img_file.resize((int(xSize/scale),int(ySize/scale)), Image.ANTIALIAS)
	my_new_path = "plot_"+old_path
	img_file.save(my_new_path, optimize=True, quality = 95)
	img_file = Image.open(my_new_path)
	img = img_file.load()

	#size of the new downsampled image
	[xSize, ySize] = img_file.size
	_r = []
	_g = []
	_b = []
	colours = []
	for x in range(0,xSize):
		for y in range(0,ySize):
			[r,g,b] = img[x,y]
			r /= 255.0
			_r.append(r)
			g /= 255.0
			_g.append(g)
			b /= 255.0
			_b.append(b)
			colours.append([r,g,b])
			
	fig = plt.figure()
	ax = p3.Axes3D(fig)
	ax.scatter(_r,_g,_b, c=colours, lw=0)
	ax.set_xlabel('R')
	ax.set_ylabel('G')
	ax.set_zlabel('B')
	fig.add_axes(ax)
	plt.show()
	return

def line(m, b, x, y):
	return y - m*x - b

def detectHorizon(cvImg, xSize, ySize):
	#keeping a resolution of 50 to generate the values of slope and y intercept
	#resolution can be changed by changing this value
	res = 100.0
	slope = np.linspace(-1,1,res)
	# print slope
	inter = np.linspace(0,ySize,res)
	# print inter
	maximum = []
	J_max = 0

	#iterate over all the slope and intercept values
	for m in range(len(slope)):
		for b in range(len(inter)):
			sky = [] #array of pixel values containing sky
			gnd = [] #array of pixel values containing ground

			#iterate over all the pixels in the image and add them to sky and gnd
			for i in range(xSize):
				for j in range(ySize):
					if((line(slope[m],inter[b],i,j)*(-1*inter[b])) > 0):
						sky.append(cvImg[j,i])
					else:
						gnd.append(cvImg[j,i])


			#find covariance of the sky and gnd pixels
			sky = np.transpose(sky)
			gnd = np.transpose(gnd)
			try:
				co_s = np.cov(sky)
				co_g = np.cov(gnd)
				co_sD = np.linalg.det(co_s)
				# print "co__sD", co_sD
				co_gD = np.linalg.det(co_g)
				# print "co__gD", co_gD
				eig_s, _ = np.linalg.eig(co_s)
				# print "eig_s", eig_s
				eig_g, _ = np.linalg.eig(co_g)
				# print "eig_g", eig_g

				J = 1/(co_sD + co_gD + (eig_s[0]+eig_s[1]+eig_s[2])**2 + (eig_g[0]+eig_g[1]+eig_g[2])**2)
				# J = 1/(co_sD + co_gD)
				# print "J: ", J
				if J > J_max:
					J_max = J
					maximum = [slope[m], inter[b]]
					print maximum
					# print maximum[0], maximum[1]
			except Exception:
				pass

	return maximum

def display(window, image):
	cv2.namedWindow( window ) 
	cv2.imshow( window, image );         
	cv2.waitKey(0) 


def plot(cvImg, horizon, path):
	xSize = cvImg.shape[1]
	print "xSize", xSize
	m = horizon[0]
	b = horizon[1]
	y2 = int(m*(xSize-1)+b)
	cv2.line(cvImg, (0,int(b)), (xSize-1, y2), (0,0,255), 2)
	save_path = "myHorizon_"+path
	cv2.imwrite(save_path, cvImg)
	display("horizon", cvImg)
	

#just some constants
# old_path = "image9.png"
old_path = []
# for i in range(10, 34):
# 	k = "image"+`i`+".png"
# 	print k
# 	old_path.append(k)
old.path.append("images/image34.png")

scale = 10.0

for path in old_path:
	#opening the new image in CV
	print "--------------------------------"
	print "Processing image: ", path
	cvImg_original = cv2.imread(path)
	ySize = cvImg_original.shape[0]
	xSize = cvImg_original.shape[1]
	print xSize, ySize
	cvImg = cv2.resize(cvImg_original, (0,0), fx=1/scale, fy=1/scale) 
	new_path = "new_"+path
	cv2.imwrite(new_path, cvImg)
	ySize = cvImg.shape[0]
	xSize = cvImg.shape[1]
	print xSize, ySize
	cvImg = cv2.GaussianBlur(cvImg,(5,5),0)

	horizon = []
	horizon = detectHorizon(cvImg, xSize, ySize)

	horizon[1] *= scale
	plot(cvImg_original, horizon, path)



# #opening the new image in CV
# cvImg_original = cv2.imread(old_path)
# ySize = cvImg_original.shape[0]
# xSize = cvImg_original.shape[1]
# print xSize, ySize
# cvImg = cv2.resize(cvImg_original, (0,0), fx=1/scale, fy=1/scale) 
# cv2.imwrite(new_path, cvImg)
# ySize = cvImg.shape[0]
# xSize = cvImg.shape[1]
# print xSize, ySize

# #plot pixel data
# # plotPixelData(old_path, scale)

# #detect horizon
# horizon = []
# horizon = detectHorizon(cvImg, xSize, ySize)

# #plot the line with the slope and intercept on the original image
# horizon[1] *= scale
# plot(cvImg_original, horizon, old_path)


