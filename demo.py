def imageReader(file):
	import cv2
	import sys
	import pytesseract
	impath = file
	config = ('-l eng --oem 1 --psm 3')

	im = cv2.imread(impath, cv2.IMREAD_COLOR)
	text = pytesseract.image_to_string(im, config = config)

	return text


