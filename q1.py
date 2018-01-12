#!/usr/bin/env python
# coding=utf-8
import colorsys
import numpy as np
from PIL import Image
from utility import *

def run(fileName):
    print "input: "+fileName

    fileName += ".q1hsv"
    compareDistance = [-1]*FILE_COUNT

    with open(fileName) as f:
        fileHistogramList = map(int, f.read().splitlines())
        fileHistogram = np.array(fileHistogramList)
        # print fileHistogram

    for x in xrange(FILE_COUNT):
        with open(convertToPathStr(x)+".q1hsv") as f:
            lines = map(int, f.read().splitlines())
            combine = [abs(item[0]-item[1]) for item in zip(np.array(lines), fileHistogram)]
            for y in xrange(360):
                if combine[y] > 180:
                    combine[y] = (360 - combine[y])*2
                else:
                    combine[y] *= 2
            for y in range(360, 460):
                combine[y] = combine[y]/2
            compareDistance[x] = np.linalg.norm(combine)

    #print "compareDistance: ", compareDistance
    sortArr =  np.argsort(compareDistance)[:10]
    print sortArr
    return [convertToPathStr(ele) for ele in sortArr]


def offlineProcess(i):

    fileName = convertToPathStr(i)
    print fileName

    img = Image.open(fileName)
    pixel = img.load()
    hArr = [0]*360
    sArr = [0]*101
    vArr = [0]*101
    width, height = img.size

    Arr = [pixel[x, y] for x in xrange(width) for y in xrange(height)]
    Hsv = [colorsys.rgb_to_hsv(item[0]/255., item[1]/255., item[2]/255.) for item in Arr]

    # for x in xrange(len(Hsv)):
    #     Hsv[x] = (Hsv[x][0]*360, Hsv[x][1]*100, Hsv[x][2]*100)
    #     Hadjust = int(round(Hsv[x][0]))
    #     if Hadjust==360:
    #         Hadjust = 0
    #     hArr[Hadjust] += 1
    #     sArr[int(round(Hsv[x][1]))] += 1
    #     vArr[int(round(Hsv[x][2]))] += 1

#136
    for item in Hsv:
        Hadjust = int(item[0]*360+0.5)
        if Hadjust == 360:
            Hadjust = 0
        hArr[Hadjust] += 1
        sArr[int(item[1]*100+0.5)] += 1
        vArr[int(item[2]*100+0.5)] += 1


    hsv = open(fileName+".q1hsv", "w")
    for i in hArr+sArr+vArr:
        print>>hsv, i
    hsv.close()

if __name__ == "__main__":
    import time
    t = time.time()
    for x in range(0, FILE_COUNT):
        offlineProcess(x)
    print time.time()-t