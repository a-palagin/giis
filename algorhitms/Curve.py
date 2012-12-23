from __future__ import division
__author__ = 'apalagin'

import math


class Circle:

    @staticmethod
    def getPixels(points):
        x1 = int(points[0][0])
        y1 = int(points[0][1])
        x2 = int(points[1][0])
        y2 = int(points[1][1])
        pixels = []
        def reflect(points):
            length = len(points) - 1
            firstXPoint = points[0][0]
            firstYPoint = points[length][1]
            while length >= 0:
                length -= 1
                rx = points[length][0]
                ry = points[length][1]
                points.append((-rx + 2 * firstXPoint, ry))
                points.append((-rx + 2 * firstXPoint, -ry + 2 * firstYPoint))
                points.append((rx, -ry + 2 * firstYPoint))
            return points
        radius = int(round(math.sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2))))
        print radius
        x = 0
        y = radius
        delta = 3 - 2 * radius
        sigma = 0
        pixels.append((x + x1,y + y1))
        while y > 0:
            if delta > 0:
                sigma = 2 * delta - 2 * x - 1
                if sigma <= 0:
                    x += 1
                    y -= 1
                    delta = delta + 2 * x - 2 * y + 2
                    pixels.append((x + x1, y + y1))
                else:
                    y -= 1
                    delta = delta - 2 * y + 1
                    pixels.append((x + x1,y + y1))
            elif delta < 0:
                sigma = 2 * delta + 2 * y - 1
                if sigma > 0:
                    x += 1
                    y -= 1
                    delta = delta + 2 * x - 2 * y + 2
                    pixels.append((x + x1, y + y1))
                else:
                    x += 1
                    delta = delta + 2 * x + 1
                    pixels.append((x + x1, y + y1))
            else:
                x += 1
                y -= 1
                delta = delta + 2 * x - 2 * y + 2
                points.append((x + x1, y + y1))
        pixels = reflect(pixels)
        pixels.append((x1 - radius,y1))
        pixels.append((x1 + radius,y1))
        #pixels.append((x2,y2))
        return pixels


class Parabola:

    @staticmethod
    def getPixels(points):
        x2 = points[0][0]
        x1 = points[1][0]
        y2 = points[0][1]
        y1 = points[1][1]

        if x1 < x2:
            inverse = -1
        else:
            inverse = 1
        if x1 == x2:
            p = 9999999999999999.9
        else:
            p = float((y1 - y2)**2.0/float((2.0*inverse*(x1 - x2))))

        x = 0
        y = 0
        d = 2*p-1
        e = 0
        pixels = []
        for i in xrange(99):
            pixels.append((x2 + inverse*x, y2 + y))
            pixels.append((x2 + inverse*x, y2 - y))
            if d>0:
                e=abs((y+1)*(y+1)-2*p*(x+1))-abs((y+1)*(y+1)-2*p*x)
                if e>0:
                    y+=1
                    d=d-2*y-1
                    continue

            if d<0:
                e=abs(y*y-2*p*(x+1))-abs((y+1)*(y+1)-2*p*(x+1))
                if e<=0 :
                    x+=1
                    d+=2*p
                    continue
            x+=1
            y+=1
            d=d-2*y-1+2*p
        return pixels

class Bezie:

    @staticmethod
    def calculateX(x1,x2,x3,x4,t):
        return round(pow((1 - t), 3)
                     * x1 + 3 * t * pow((1 - t), 2)
                     * x2 + 3 * pow(t, 2) * (1 - t)
                     * x3 + pow(t, 3)
                     * x4)

    @staticmethod
    def calculateY(y1,y2,y3,y4,t):
        return round(pow((1 - t), 3)
                     * y1 + 3 * t * pow((1 - t), 2)
                     * y2 + 3 * pow(t, 2) * (1 - t)
                     * y3 + pow(t, 3)
                     * y4 )

    @staticmethod
    def getPixels(controlPoints) :
        calculatedPoints=[]
        step = 0.2
        t = 0

        x1 = controlPoints[0][0]
        x2 = controlPoints[1][0]
        x3 = controlPoints[2][0]
        x4 = controlPoints[3][0]

        y1 = controlPoints[0][1]
        y2 = controlPoints[1][1]
        y3 = controlPoints[2][1]
        y4 = controlPoints[3][1]

        x = x1
        y = y1

        while t < 1:
            calculatedPoints.append((x, y))
            px = x
            py = y
            step2 = step

            while True:
                step2 = step2 / 2
                x = Bezie.calculateX(x1,x2,x3,x4,t+step2)
                y = Bezie.calculateY(y1,y2,y3,y4,t+step2)
                offset = int(abs(px - x)) | int(abs(py - y))

                if offset == 0 or offset == 1:
                    break
            t += step2
        calculatedPoints.append((x4,y4))
        return calculatedPoints


class BSpline:

    @staticmethod
    def getPixels(points, m, step):
        '''
            points - control points
        m - degree of B-splines
        '''
        M = len(points) - 1
        n = M - m + 1
        knots = [0] * m + [k / n for k in xrange(n + 1)] + [1] * m

        def curve(t):
            if t == 1:
                return points[-1]

            k = m + int(math.floor(t * n))
            # values of N[m, k-m],...,N[m, k] at t
            Nk = [1] + [0] * m

            V = lambda m, i, t: (t - knots[i]) / (knots[i + m] - knots[i]) if knots[i] != knots[i + m] else 0

            for i in xrange(1, m + 1):
                for j in xrange(i, -1, -1):
                    # count N[i, k-j]
                    if j:
                        Nk[j] = Nk[j - 1] * (1 - V(i, k - j + 1, t)) + Nk[j] * V(i, k - j, t)
                    else:
                        Nk[j] = Nk[j] * V(i, k - j, t)

            Nk.reverse()

            return [sum(p[j] * N for p, N in zip(points[k-m:k+1], Nk)) for j in (0, 1)]

        return curve









