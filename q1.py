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
            combine = list(map(lambda x: abs(x[0]-x[1]), zip(np.array(lines), fileHistogram)))
            for y in xrange(360):
                if combine[y] > 180:
                    combine[y] = (360 - combine[y])*2
            for y in range(360, 460):
                combine[y] = combine[y]/2
            compareDistance[x] = np.linalg.norm(combine)

    #print "compareDistance: ", compareDistance
    sortArr =  np.argsort(compareDistance)[:10]
    print sortArr
    return [convertToPathStr(ele) for ele in sortArr]


def offlineProcess(i):
    #colorsys.rgb_to_hsv(R, G, B)

    fileName = convertToPathStr(i)
    # fileName = "E:/Porkchop/PycharmProjects/MM_HW03/dataset/ukbench00220.jpg"
    # fileName = "C:/Users/Stanley/Documents/search-image/dataset/ukbench00220.jpg"
    print fileName
    img = Image.open(fileName)
    pixel = img.load()
    #rArr = [0]*256
    #gArr = [0]*256
    #bArr = [0]*256
    hArr = [0]*360
    sArr = [0]*101
    vArr = [0]*101
    Arr = []
    Hsv = []
    width, height = img.size
    # print img.size
    # print pixel

    for x in xrange(width):
        for y in xrange(height):
            color = pixel[x, y]
            # print x, y, color
            #rArr[color[0]] += 1
            #gArr[color[1]] += 1
            #bArr[color[2]] += 1
            Arr.append(color)

    for x in xrange(len(Arr)):
        Hsv.append(colorsys.rgb_to_hsv(Arr[x][0]/255., Arr[x][1]/255., Arr[x][2]/255.))
    for x in xrange(len(Hsv)):
        Hsv[x] = (Hsv[x][0]*360, Hsv[x][1]*100, Hsv[x][2]*100)
        Hadjust = 0
        if int(round(Hsv[x][0])) != 360:
            Hadjust = int(round(Hsv[x][0]))
        hArr[Hadjust] += 1
        sArr[int(round(Hsv[x][1]))] += 1
        vArr[int(round(Hsv[x][2]))] += 1

    # print rArr+gArr+bArr
    # print rArr
    # print gArr
    # print bArr
    #text = open(fileName+".q1", "w")
    #for i in rArr+gArr+bArr:
    #    print>>text, i
    # text.write("{}".format(rArr+gArr+bArr))
    #text.close()

    hsv = open(fileName+".q1hsv", "w")
    for i in hArr+sArr+vArr:
        print>>hsv, i
    hsv.close()

if __name__ == "__main__":
    for x in range(0, FILE_COUNT):
        offlineProcess(x)
