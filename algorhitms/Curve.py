__author__ = 'apalagin'

import math

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








