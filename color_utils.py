#!/usr/bin/python
# import colorsys could also use this
import math
# http://www.rapidtables.com/convert/color/rgb-to-hsv.htm
# TODO: Switch to LAB color space instead of HSV
# TODO: think of better multiple metrics:
#       Warmness, coldness, closeness to each other, clustering


def rgb2lab ( inputColor ) : # http://stackoverflow.com/a/16020102
   num = 0
   RGB = [0, 0, 0]
   for value in inputColor :
       value = float(value) / 255

       if value > 0.04045 :
           value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
       else :
           value = value / 12.92

       RGB[num] = value * 100
       num = num + 1

   XYZ = [0, 0, 0,]

   X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
   Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
   Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
   XYZ[ 0 ] = round( X, 4 )
   XYZ[ 1 ] = round( Y, 4 )
   XYZ[ 2 ] = round( Z, 4 )

   XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2, Illuminant= D65
   XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
   XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883

   num = 0
   for value in XYZ :

       if value > 0.008856 :
           value = value ** ( 0.3333333333333333 )
       else :
           value = ( 7.787 * value ) + ( 16 / 116 )

       XYZ[num] = value
       num = num + 1

   Lab = [0, 0, 0]

   L = ( 116 * XYZ[ 1 ] ) - 16
   a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
   b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )

   Lab [ 0 ] = round( L, 4 )
   Lab [ 1 ] = round( a, 4 )
   Lab [ 2 ] = round( b, 4 )

   return Lab

def rgb_to_hsv(r, g, b):
	r_prime = r / 255.0
	g_prime = g / 255.0
	b_prime = b / 255.0
	cmax = max([r_prime,g_prime,b_prime])
	cmin = min([r_prime,g_prime,b_prime])
	delta = cmax - cmin
	h = None
	s = None
	v = cmax
	if delta == 0.0:
		h = 0.0
	elif cmax == r_prime:
		h = 60 * (((g_prime - b_prime) / delta) % 6)
	elif cmax == g_prime:
		h = 60 * (((b_prime - r_prime) / delta) + 2)
	else:
		h = 60 * (((r_prime - g_prime) / delta) + 4)
	h = h / 360.0

	if cmax == 0.0:
		s = 0.0
	else:
		s = delta / cmax

	return [h,s,v]

def euclid_hsv(x1, y1, z1, x2, y2, z2):
	x_prime = pow(x2 - x1, 2)
	y_prime = pow(y2 - y1, 2)
	z_prime = pow(z2 - z1, 2)
	return math.sqrt(x_prime + y_prime + z_prime)

def avg_of_list(lst):
    sum = 0.0
    for el in lst:
        sum += el
    return sum / len(lst)

def convert_lab_list(rgb_list):
    lab_list = []
    for color in rgb_list:
        el = color.split('-')
        lab_list.append(rgb2lab([int(el[0]),int(el[1]),int(el[2])]))
    return lab_list

def convert_hsv_list(rgb_list):
    hsv_list = []
    for color in rgb_list:
        el = color.split('-')
        hsv_list.append(rgb_to_hsv(int(el[0]),int(el[1]),int(el[2])))
    return hsv_list

def avg_distance_colors(color_list, t):
    if t == 'hsv':
        hsv_list = convert_hsv_list(color_list)
        final_distance_list = []
        for color in hsv_list:
            distance_list = []
            for other_color in hsv_list:
                if other_color == color:
                    continue
                else:
                    d = euclid_hsv(color[0],color[1],color[2],other_color[0],other_color[1],other_color[2])
                    distance_list.append(d)
            final_distance_list.append(avg_of_list(distance_list))
        return avg_of_list(final_distance_list)
    else:
        lab_list = convert_lab_list(color_list)
        final_distance_list = []
        for color in lab_list:
            distance_list = []
            for other_color in lab_list:
                if other_color == color:
                    continue
                else:
                    d = euclid_hsv(color[0],color[1],color[2],other_color[0],other_color[1],other_color[2])
                    distance_list.append(d)
            final_distance_list.append(avg_of_list(distance_list))
        return avg_of_list(final_distance_list)


