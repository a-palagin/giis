__author__ = 'drain'

import math
class Line:

	@staticmethod
	def CDA(x1,y1,x2,y2):
		pixels = []
		print x1,y1,x2,y2
		len = max(abs(x2 - x1), abs(y2 - y1))
		dx = (x2 - x1) / len
		dy = (y2 - y1) / len
#		x = x1 + 0.5*math.copysign(1.0,dx)
#		y = y1 + 0.5*math.copysign(1.0,dy)
		x = x1
		y = y1
		i = 1.0
		while i <= len:
			pixels.append((x,y))
			x = x + dx
			y = y + dy
			i += 1.0
		pixels.append((x2,y2))
		return pixels

	@staticmethod
	def Bresenham(x1,y1,x2,y2):
		pixels = []
		dx = x2 - x1
		dy = y2 - y1
		incx = math.copysign(1.0,dx)
		incy = math.copysign(1.0,dy)
		if dx < 0 : dx = -dx
		if dy < 0 : dy = -dy
		if dx > dy :
			pdx = incx
			pdy = 0
			es = dy
			el = dx
		else:
			pdx = 0
			pdy = incy
			es = dx
			el = dy
		x = x1
		y = y1
		pixels.append((x,y))
		err = el/2.0
		t = 0.0
		while t < el:
			t += 1.0
			err -= es
			if err < 0.0:
				err += el
				x += incx
				y += incy
			else:
				x += pdx
				y += pdy
			pixels.append((x,y))
		return pixels

