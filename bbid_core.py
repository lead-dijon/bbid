import platform
import os
import time
import numpy
import scipy.ndimage
import matplotlib.image


# Global variables

BLUE     = 2
GREEN    = 1
RED      = 0
ROW      = 1
COLUMN   = 0
ABSCISSA = 1
ORDINATE = 0
MINIMUM  = 1
MAXIMUM  = 0


def image(multiprocessing_, input_, output, width, height, \
		  luminance, size, angle, texture, side, shades, \
		  scale, margin, items, ratio, factor, circles_, bar_, \
		  colors1, colors2, saturation, high, low) :
	
	
	radius = side
	
	
	print("Processing", end = ' ')
	if multiprocessing_ == True :
		import multiprocessing
		print(f"@{multiprocessing.current_process().name}", end = ' ')
	print(f": Luminance #{luminance}, Size #{size}, Angle #{angle}, Texture #{texture}, Side #{side}, Radius #{radius}")
	
	
	# Background generation
						
						
	for shade in shades :

		
		length = 4 * side[MAXIMUM]
		background_ = scale * numpy.ones((margin + 2 * length + height, margin + 2 * length + width))
		
		
		for item in items :
			
			# Circles generation
			shade_ = shade[MINIMUM] + (shade[MAXIMUM] - shade[MINIMUM]) * numpy.random.rand(1)[0]
			radius_ = radius[MINIMUM] + (radius[MAXIMUM] - radius[MINIMUM]) * numpy.random.rand(1)[0]
			abscissa = length * ratio + (factor * width) * numpy.random.rand(1)[0]
			ordinate = length * ratio + (factor * height) * numpy.random.rand(1)[0]
			circles = radius_ * (1 + circles_)
			range_ = [0, 0]
			range_[MINIMUM] = radius_ * (1 - numpy.sqrt(1 - numpy.power(circles_, 2)))
			range_[MAXIMUM] = radius_ * (1 + numpy.sqrt(1 - numpy.power(circles_, 2)))
			for circle in range(0, len(circles_)) :
				for index in range(numpy.round(range_[MINIMUM][circle].astype(numpy.int)), numpy.round(range_[MAXIMUM][circle]).astype(numpy.int)) :
					background_[numpy.ceil(abscissa + index - (numpy.round(radius_ / 2))).astype(numpy.int), numpy.ceil(ordinate + circles[circle]).astype(numpy.int)] = numpy.round(shade_)
			
			# Square generation
			shade_ = shade[MINIMUM] + (shade[MAXIMUM] - shade[MINIMUM]) * numpy.random.rand(1)[0]
			side_ = side[MINIMUM] + (side[MAXIMUM] - side[MINIMUM]) * numpy.random.rand(1)[0]
			base = [0, 0]
			base[ABSCISSA] = length + width * numpy.random.rand(1)
			base[ORDINATE] = length + height * numpy.random.rand(1)
			for abscissa in range((numpy.round(base[ABSCISSA]).astype(numpy.int) - numpy.floor(side_ / 2).astype(numpy.int))[0],
								  (numpy.round(base[ABSCISSA]).astype(numpy.int) +  numpy.ceil(side_ / 2).astype(numpy.int))[0]) :
				for ordinate in range((numpy.round(base[ORDINATE]).astype(numpy.int) - (numpy.floor(side_ / 2)).astype(numpy.int))[0],
									  (numpy.round(base[ORDINATE]).astype(numpy.int) +  (numpy.ceil(side_ / 2)).astype(numpy.int))[0]) :
					background_[ordinate,abscissa] = numpy.round(shade_)
	
	
	background = background_[margin // 2 + length : margin // 2 + length + height, margin // 2 + margin // 2 + length : margin // 2 + margin // 2 + length + width]
	
	
	# Bar generation
	bar = scale * numpy.ones(numpy.shape(background))
	bar[numpy.round(   numpy.shape(background)[ROW] / 2).astype(numpy.int) -  numpy.floor(bar_ / 2).astype(numpy.int) :
		numpy.round(   numpy.shape(background)[ROW] / 2).astype(numpy.int) +   numpy.ceil(bar_ / 2).astype(numpy.int),
		numpy.round(numpy.shape(background)[COLUMN] / 2).astype(numpy.int) - numpy.floor(size / 2).astype(numpy.int) :
		numpy.round(numpy.shape(background)[COLUMN] / 2).astype(numpy.int) +  numpy.ceil(size / 2).astype(numpy.int)] = 1
	
	
	# First color reversal
	for row in range(0, numpy.shape(bar)[ROW]) :
		for column in range(0, numpy.shape(bar)[COLUMN]) :
			if bar[row, column] <  colors1[0][0] :
				bar[row, column] = colors1[0][1]
			if bar[row, column] <  colors1[1][0] :
				bar[row, column] = colors1[1][1]
			if bar[row, column] == colors1[2][0] :
				bar[row, column] = colors1[2][1]
	
	
	# Bar rotation		 
	bar = scipy.ndimage.rotate(bar, -angle, mode = "nearest", reshape = False);
	
	
	# Second color reversal
	for row in range(0, numpy.shape(bar)[ROW]) :
		for column in range(0, numpy.shape(bar)[COLUMN]) :
			if bar[row, column] <  colors2[0][0] :
				bar[row, column] = colors2[0][1]
			if bar[row, column] <  colors2[1][0] :
				bar[row, column] = colors2[1][1]
			if bar[row, column] == colors2[2][0] :
				bar[row, column] = colors2[2][1]
	
	
	# Texture loading
	texture_ = matplotlib.image.imread(os.path.join(input_, texture))
	
	
	# Image generation
	
	image = saturation * numpy.ones(numpy.shape(background))
	
	for row in range(0, numpy.shape(bar)[ROW]) :
		for column in range(0, numpy.shape(bar)[COLUMN]) :
			if bar[row, column] > high :
				image[row, column] = background[row, column]
			if bar[row, column] < low :
				image[row, column] = scale * texture_[row, column, GREEN]


	# Image checking
	if numpy.amin(image) == saturation or numpy.amax(image) == saturation :
		print("Saturation error")


	# Image storage
	matplotlib.image.imsave(os.path.join(output, f"BkGd_Ci {radius[MINIMUM]}-{radius[MAXIMUM]}"
											   + f"_Sq {side[MINIMUM]}-{side[MAXIMUM]}"
											   + f"_lum{shade[MINIMUM]}-{shade[MAXIMUM]}"
											   + f"___Bar Texture_{os.path.splitext(texture)[0].split('_')[1]}"
											   + f"_{size}x100"
											   + f"_r{angle}"
											   + f"_lum{shade_:07.3f}"
											   + f"_v0.png"), image, cmap = "gray")


def images(multiprocessing_, input_, output, width, height, luminances, sizes, angles, textures, sides, shades, scale, margin, items, ratio, factor, circles, bar, colors1, colors2, saturation, high, low) :


	if multiprocessing_ == True :
		import multiprocessing
		with multiprocessing.Pool() as pool :
			pool.starmap(image, [(multiprocessing_, input_, output, width, height, \
								  luminance, size, angle, texture, side, shades, \
								  scale, margin, items, ratio, factor, circles, bar, \
								  colors1, colors2, saturation, high, low) \
								  for side in sides for texture in textures for angle in angles for size in sizes for luminance in luminances])


	else :


		for luminance in luminances :


			for size in sizes :


				for angle in angles :


					for texture in textures :


						for side in sides :
							
							
							image(multiprocessing_, input_, output, width, height, \
								  luminances, size, angle, texture, side, shades, \
								  scale, margin, items, ratio, factor, circles, bar, \
								  colors1, colors2, saturation, high, low)
