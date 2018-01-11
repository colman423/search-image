#!/usr/bin/env python
# coding=utf-8
import numpy as np
from PIL import Image
import scipy.fftpack as fft
from utility import *


def run(fileName):
    print "input: " + fileName

    fileName += ".q2"
    compareDistance = [-1] * FILE_COUNT

    with open(fileName) as f:
        fileData = [item.split(' ') for item in f.read().splitlines()]
        f.close()
        yArr = [float(j[0]) for j in fileData]
        cbArr = [float(j[1]) for j in fileData]
        crArr = [float(j[2]) for j in fileData]


    for x in xrange(FILE_COUNT):
        with open(convertToPathStr(x) + ".q2") as f:


            print "comparing file "+convertToPathStr(x) + ".q2"
            compareData = [item.split(' ') for item in f.read().splitlines()]
            f.close()
            compY = [float(j[0]) for j in compareData]
            compCb = [float(j[1]) for j in compareData]
            compCr = [float(j[2]) for j in compareData]


            disY, disCb, disCr = 0, 0, 0
            for k in xrange(64):
                disY += pow(yArr[k] - compY[k], 2)
                disCb += pow(cbArr[k] - compCb[k], 2)
                disCr += pow(crArr[k] - compCr[k], 2)

            compareDistance[x] = pow(disY, 0.5) + pow(disCb, 0.5) + pow(disCr, 0.5)


    #print "compareDistance: ", compareDistance
    sortArr =  np.argsort(compareDistance)[:10]
    print sortArr
    return [convertToPathStr(ele) for ele in sortArr]


def convertZigzac(arr):
    convert = [[0, 1, 5, 6, 14, 15, 27, 28],
            [2, 4, 7, 13, 16, 26, 29, 42],
            [3, 8, 12, 17, 25, 30, 41, 43],
            [9, 11, 18, 24, 31, 40, 44, 53],
            [10, 19, 23, 32, 39, 45, 52, 54],
            [20, 22, 33, 38, 46, 51, 55, 60],
            [21, 34, 37, 47, 50, 56, 59, 61],
            [35, 36, 48, 49, 57, 58, 62, 63]]
    data=[None]*64
    for i in xrange(8):
        for j in xrange(8):
            data[convert[i][j]] = arr[i][j]
    # print "convertEnd"
    # print data
    return data

def _ycc(r, g, b): # in (0,255) range
    y = .299*r + .587*g + .114*b
    cb = 128 -.168736*r -.331364*g + .5*b
    cr = 128 +.5*r - .418688*g - .081312*b
    return y, cb, cr

def getSide(x, y):
    if x==7:
        return getSide(6, y)
    elif y==7:
        return getSide(x, 6)
    else:
        return x, y


def doColorLayout(pixel, width, height, xStart=0, yStart=0):
    # print "start doing color layout!, x, y start = ", xStart, yStart
    blockW, blockH = width/8, height/8
    representY = [[0 for i in range(8)] for j in range(8)]
    representCb = [[0 for i in range(8)] for j in range(8)]
    representCr = [[0 for i in range(8)] for j in range(8)]
    for xBlock in xrange(8):
        for yBlock in xrange(8):
            xBase = blockW*xBlock+xStart
            yBase = blockH*yBlock+yStart
            # print "block: ", xBlock, yBlock, "Base: ", xBase, yBase

            pixArr = []
            for x in xrange(blockW):
                for y in xrange(blockH):
                    try:
                        pixArr.append(pixel[x+xBase, y+yBase])
                    except:
                        pass

            # pixArr = [ pixel[x+xBase, y+yBase] for x in xrange(blockW) for y in xrange(blockH)]
            if len(pixArr)!=0:
                colR = sum([col[0] for col in pixArr]) / float(len(pixArr))
                colG = sum([col[1] for col in pixArr]) / float(len(pixArr))
                colB = sum([col[2] for col in pixArr]) / float(len(pixArr))
                # print "RGB:", colR, colG, colB

                colY, colCb, colCr = _ycc(colR, colG, colB)
                representY[xBlock][yBlock] = colY
                representCb[xBlock][yBlock] = colCb
                representCr[xBlock][yBlock] = colCr
            else:
                x, y = getSide(xBlock, yBlock)
                representY[xBlock][yBlock] = representY[x][y]
                representCb[xBlock][yBlock] = representCb[x][y]
                representCr[xBlock][yBlock] = representCr[x][y]

    # print "block success"

    dctY = fft.dct(representY)
    dctCb = fft.dct(representCb)
    dctCr = fft.dct(representCr)
    return convertZigzac(dctY), convertZigzac(dctCb), convertZigzac(dctCr)

def offlineProcess(i):

    fileName = convertToPathStr(i)
    # fileName = "E:/Porkchop/PycharmProjects/MM_HW03/dataset/ukbench00001.jpg"
    print fileName
    img = Image.open(fileName)
    pixel = img.load()
    width, height = img.size
    dataY, dataCb, dataCr = doColorLayout(pixel, width, height)

    text = open(fileName + ".q2", "w")
    for i in xrange(64):
        print>> text, str(dataY[i]) + ' ' + str(dataCb[i]) + ' ' + str(dataCr[i])
    text.close()



if __name__ == "__main__":
    for x in range(0, FILE_COUNT):
        offlineProcess(x)
