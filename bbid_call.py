import argparse
import os
import sys
import shutil
import numpy
import zipfile
import bbid_core


# Processing
MULTIPROCESSING = True

# Paths
INPUT  = "/home/lead/www/bbid/res"
OUTPUT = "/home/lead/www/bbid/wk"

# Parameters
WIDTH        = 140
HEIGHT       = 140
LUMINANCES   = [128]
SIZES        = [4, 6, 9, 15, 24, 42]
ANGLES_MIN   = 0
ANGLES_MAX   = 90
ANGLES_STEP  = 10
TEXTURES     = ["Texture_1.png", "Texture_2.png", "Texture_3.png"]
SIDES        = [(10, 4), (16, 10), (22, 16)]
SHADES       = [(1, 64), (65, 128), (129, 192), (193, 255)]
SCALE        = 256
MARGIN       = 10
ITEMS        = 1000
RATIO        = 4.0 / 5.0
FACTOR       = 1.1
CIRCLES_MIN  = -1
CIRCLES_MAX  = 1
CIRCLES_STEP = 0.01
BAR          = 100
COLORS1      = [(10, 999), (300, 0), (999, 256)] # [(3, 999), (257, 0), (999, 256)]
COLORS2      = [(10, 999), (300, 1), (999, 256)] # [(3, 999), (257, 0), (999, 256)]
SATURATION   = 999
HIGH         = 250
LOW          = 5


# Module call


argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("-id" , "--identifier"                  , type = str  , help = "Multiprocessing" , default = 0)
argumentParser.add_argument("-mp" , "--multiprocessing"             , type = bool , help = "Multiprocessing" , default = MULTIPROCESSING)
argumentParser.add_argument("-in" , "--input"	                    , type = str  , help = "Input directory" , default = INPUT)
argumentParser.add_argument("-out", "--output"                      , type = str  , help = "Output directory", default = OUTPUT)
argumentParser.add_argument("-wt" , "--width"                       , type = int  , help = "Image width"     , default = WIDTH)
argumentParser.add_argument("-ht" , "--height"                      , type = int  , help = "Image height"    , default = HEIGHT)
argumentParser.add_argument("-lm" , "--luminances"      , nargs="+" , type = int  , help = "Luminances"      , default = LUMINANCES)
argumentParser.add_argument("-sz" , "--sizes"           , nargs="+" , type = int  , help = "Sizes"           , default = SIZES)
argumentParser.add_argument("-an" , "--angles_min"                  , type = int  , help = "Angle minimum"   , default = ANGLES_MIN)
argumentParser.add_argument("-ax" , "--angles_max"                  , type = int  , help = "Angle maximum"   , default = ANGLES_MAX)
argumentParser.add_argument("-as" , "--angles_step"                 , type = int  , help = "Angle step"      , default = ANGLES_STEP)
argumentParser.add_argument("-t"  , "--textures"        , nargs="+"               , help = "Textures"        , default = TEXTURES)
argumentParser.add_argument("-si" , "--sides"           , nargs="+"               , help = "Sides"           , default = SIDES)
argumentParser.add_argument("-sd" , "--shades"          , nargs="+"               , help = "Shades"          , default = SHADES)
argumentParser.add_argument("-sc" , "--scale"                       , type = int  , help = "Scale"           , default = SCALE)
argumentParser.add_argument("-mg" , "--margin"                      , type = int  , help = "Margin"          , default = MARGIN)
argumentParser.add_argument("-it" , "--items"                       , type = int  , help = "Items"           , default = ITEMS)
argumentParser.add_argument("-r"  , "--ratio"                       , type = float, help = "Ratio"           , default = RATIO)
argumentParser.add_argument("-f"  , "--factor"                      , type = float, help = "Items"           , default = FACTOR)
argumentParser.add_argument("-cn" , "--circles_min"                 , type = int  , help = "Circles"         , default = CIRCLES_MIN)
argumentParser.add_argument("-cx" , "--circles_max"                 , type = int  , help = "Circles"         , default = CIRCLES_MAX)
argumentParser.add_argument("-cs" , "--circles_step"                , type = int  , help = "Circles"         , default = CIRCLES_STEP)
argumentParser.add_argument("-b"  , "--bar"                         , type = int  , help = "Bar"             , default = BAR)
argumentParser.add_argument("-c1" , "--colors1"         , nargs="+"               , help = "Colors1"         , default = COLORS1)
argumentParser.add_argument("-c2" , "--colors2"         , nargs="+"               , help = "Colors2"         , default = COLORS2)
argumentParser.add_argument("-st" , "--saturation"                  , type = int  , help = "Saturation"      , default = SATURATION)
argumentParser.add_argument("-hg" , "--high"                        , type = int  , help = "High"            , default = HIGH)
argumentParser.add_argument("-lw" , "--low"                         , type = int  , help = "Low"             , default = LOW)
arguments = argumentParser.parse_args()


if arguments.identifier != 0 :
	output = OUTPUT.replace('wk', arguments.identifier)
	os.mkdir(output)
else :
	output = OUTPUT

if arguments.sides != SIDES :
	sides   = [list(map(int, side.split('_')))  for side in arguments.sides]
else :
	sides = SIDES
if arguments.shades != SHADES :
	shades  = [list(map(int, shade.split('_'))) for shade in arguments.shades]
else :
	shades = SHADES
if arguments.colors1 != COLORS1 :
	colors1 = [list(map(int, color.split('_'))) for color in arguments.colors1]
else :
	colors1 = COLORS1
if arguments.colors2 != COLORS2 :
	colors2 = [list(map(int, color.split('_'))) for color in arguments.colors2]
else :
	colors2 = COLORS2	


bbid_core.images(arguments.multiprocessing,                                                          \
				 arguments.input,                                                                    \
				 output,                                                                             \
				 arguments.width,                                                                    \
				 arguments.height,                                                                   \
				 arguments.luminances,                                                               \
				 arguments.sizes,                                                                    \
				 range(arguments.angles_min, arguments.angles_max, arguments.angles_step),           \
				 arguments.textures,                                                                 \
				 sides,                                                                              \
				 shades,                                                                             \
				 arguments.scale,                                                                    \
				 arguments.margin,                                                                   \
				 range(0, arguments.items),                                                          \
				 arguments.ratio,                                                                    \
				 arguments.factor,                                                                   \
				 numpy.arange(arguments.circles_min, arguments.circles_max, arguments.circles_step), \
				 arguments.bar,                                                                      \
				 colors1,                                                                            \
				 colors2,                                                                            \
				 arguments.saturation,                                                               \
				 arguments.high,                                                                     \
				 arguments.low                                                                       )
				 

result = arguments.identifier + ".zip"
print(output)
os.chdir(output)
print(os.getcwd())
with zipfile.ZipFile(result, 'w') as handle :
	for image in [file_ for file_ in os.listdir(os.getcwd()) if file_.endswith(".png")] :
		handle.write(image)
		os.remove(image)
shutil.move(result, OUTPUT)
shutil.rmtree(output)
