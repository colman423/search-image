#!/usr/bin/env python
# coding=utf-8
import numpy as np
from PIL import Image
from utility import *


def run(fileName):
    print "input: "+fileName

    fileName += ".q1"
    compareDistance = [-1]*FILE_COUNT

    with open(fileName) as f:
        fileHistogramList = map(int, f.read().splitlines())
        fileHistogram = np.array(fileHistogramList)
        # print fileHistogram

    for x in xrange(FILE_COUNT):
        with open(convertToPathStr(x)+".q1") as f:
            lines = map(int, f.read().splitlines())
            compareDistance[x] = np.linalg.norm(np.array(lines) - fileHistogram)

    print "compareDistance: ", compareDistance
    sortArr =  np.argsort(compareDistance)[:10]
    print sortArr
    return [convertToPathStr(ele) for ele in sortArr]


def offlineProcess(i):

    fileName = convertToPathStr(i)
    # fileName = "E:/Porkchop/PycharmProjects/MM_HW03/dataset/ukbench00220.jpg"
    print fileName
    img = Image.open(fileName)
    pixel = img.load()
    rArr = [0]*256
    gArr = [1]*256
    bArr = [2]*256
    width, height = img.size
    # print img.size
    # print pixel

    for x in xrange(width):
        for y in xrange(height):
            color = pixel[x, y]
            # print x, y, color
            rArr[color[0]] += 1
            gArr[color[1]] += 1
            bArr[color[2]] += 1


    # print rArr+gArr+bArr
    # print rArr
    # print gArr
    # print bArr
    text = open(fileName+".q1", "w")
    for i in rArr+gArr+bArr:
        print>>text, i
    # text.write("{}".format(rArr+gArr+bArr))
    text.close()

if __name__ == "__main__":
    for x in range(0, FILE_COUNT):
        offlineProcess(x)