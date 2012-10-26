__author__ = 'apalagin'

import math

import numpy

class Curve:

	@staticmethod
	def Bresenham(x1,y1,x2,y2):
		pixels = []
		radius = round(math.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2))
		x = 0.0
		y = radius
		delta = 2.0 - 2*radius
		error = 0.0
		while y >= 0 :
			pixels.append((x1 + x,y1 + y))
			pixels.append((x1 + x,y1 - y))
			pixels.append((x1 - x,y1 + y))
			pixels.append((x1 - x,y1 - y))
			error = 2.0*(delta + y) - 1.0
			if delta < 0.0 or error <= 0:
				x += 1.0
				delta += 2.0*x + 1
				continue
			error = 2.0*(delta - x) - 1.0
			if delta > 0.0 or error > 0.0:
				y -= 1.0
				delta += 1 - 2*y
				continue
			x += 1.0
			delta += 2*(x - y)
		return pixels

	@staticmethod
	def threePointsCircle(points):
		pixels = []
		x1 = points[0][0]
		y1 = points[0][1]
		x2 = points[1][0]
		y2 = points[1][1]
		x3 = points[2][0]
		y3 = points[2][1]
		e = 10.0**-10
		m12 = (x2 - x1)/(y2 - y1 + e)
		m23 = (x2 - x3)/(y2 - y3 + e)
		A = numpy.matrix([[1,m12],[1,m23]])
		V = 0.5 * numpy.matrix([[y1 + y2 + (x1 + x2)*m12], [y3 + y2 + (x3 + x2)*m23]])
		xC = ((A**-1)*V)[0]
		yC = ((A**-1)*V)[1]
		R = numpy.sqrt((xC - x1)**2 + (yC - y1)**2)
		delta = numpy.pi/12.0
		x = 1.0
		y = 0.0
		k = 1
		print type(xC)
		while k <= 2.0*numpy.pi/delta:
			k += 1









