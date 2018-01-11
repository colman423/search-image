#!/usr/bin/env python
# coding=utf-8
import numpy as np
from PIL import Image
import scipy.fftpack
from utility import *


def run(fileName):
    print "input: " + fileName

    fileName += ".q2"
    compareDistance = [-1] * FILE_COUNT
    yArr, cbArr, crArr = [], [], []

    with open(fileName) as f:
        # fileHistogramList = map(int, f.read().splitlines())
        fileHistogramList = f.read().splitlines()
        for item in fileHistogramList:
            y, cb, cr = item.split(' ')
            yArr.append(float(y))
            cbArr.append(float(cb))
            crArr.append(float(cr))

        # fileHistogram = np.array(fileHistogramList)
        # print fileHistogram

    for x in xrange(FILE_COUNT):
        with open(convertToPathStr(x) + ".q2") as f:
            compareFileHistogramList = f.read().splitlines()
            compareYArr, compareCbArr, compareCrArr = [], [], []
            for item in compareFileHistogramList:
                y, cb, cr = item.split(' ')
                compareYArr.append(float(y))
                compareCbArr.append(float(cb))
                compareCrArr.append(float(cr))

            compareDistance[x] = np.linalg.norm(np.array(yArr) - np.array(compareYArr))+np.linalg.norm(np.array(cbArr) - np.array(compareCbArr))+np.linalg.norm(np.array(crArr) - np.array(compareCrArr))

    #print "compareDistance: ", compareDistance
    sortArr =  np.argsort(compareDistance)[:10]
    print sortArr
    return [convertToPathStr(ele) for ele in sortArr]


def convertZigzac(arr):
    newArr = []
    newArr.append(arr[0])
    newArr.append(arr[1])
    newArr.append(arr[8])
    newArr.append(arr[16])
    newArr.append(arr[9])
    newArr.append(arr[2])
    newArr.append(arr[3])
    newArr.append(arr[10])
    newArr.append(arr[17])
    newArr.append(arr[24])
    newArr.append(arr[32])
    newArr.append(arr[25])
    newArr.append(arr[18])
    newArr.append(arr[11])
    newArr.append(arr[4])
    newArr.append(arr[5])
    newArr.append(arr[12])
    newArr.append(arr[19])
    newArr.append(arr[26])
    newArr.append(arr[33])
    newArr.append(arr[40])
    newArr.append(arr[48])
    newArr.append(arr[41])
    newArr.append(arr[34])
    newArr.append(arr[27])
    newArr.append(arr[20])
    newArr.append(arr[13])
    newArr.append(arr[6])
    newArr.append(arr[7])
    newArr.append(arr[14])
    newArr.append(arr[21])
    newArr.append(arr[28])
    newArr.append(arr[35])
    newArr.append(arr[42])
    newArr.append(arr[49])
    newArr.append(arr[56])
    newArr.append(arr[57])
    newArr.append(arr[50])
    newArr.append(arr[43])
    newArr.append(arr[36])
    newArr.append(arr[29])
    newArr.append(arr[22])
    newArr.append(arr[15])
    newArr.append(arr[23])
    newArr.append(arr[30])
    newArr.append(arr[37])
    newArr.append(arr[44])
    newArr.append(arr[51])
    newArr.append(arr[58])
    newArr.append(arr[59])
    newArr.append(arr[52])
    newArr.append(arr[45])
    newArr.append(arr[38])
    newArr.append(arr[31])
    newArr.append(arr[39])
    newArr.append(arr[46])
    newArr.append(arr[53])
    newArr.append(arr[60])
    newArr.append(arr[61])
    newArr.append(arr[54])
    newArr.append(arr[47])
    newArr.append(arr[55])
    newArr.append(arr[62])
    newArr.append(arr[63])
    return newArr

def offlineProcess(i):

    fileName = convertToPathStr(i)
    # fileName = "E:/Porkchop/PycharmProjects/MM_HW03/dataset/ukbench00001.jpg"
    print fileName
    img = Image.open(fileName).convert('YCbCr')
    pixel = img.load()
    width, height = img.size
    blockW, blockH = width/8, height/8

    mosaicArr = []
    for yCount in xrange(8):
        for xCount in xrange(8):
            colArr = []
            countArr = []
            left, right = blockW*xCount, blockW*(xCount+1)
            top, bottom = blockH*yCount, blockH*(yCount+1)
            for x in range(left, right, 1):
                for y in range(top, bottom, 1):
                    tmp = pixel[x, y]
                    colArr.append(tmp)
                    countArr.append(tmp[0]+tmp[1]+tmp[2])

            median = len(countArr)/2
            colIndex = np.argsort(countArr)[median]
            mosaicArr.append(colArr[colIndex])

    dctResult = scipy.fftpack.dct(mosaicArr)
    dctResult = convertZigzac(dctResult)
    # print dctResult

    text = open(fileName+".q2", "w")
    for item in dctResult:
        print>>text, ' '.join(str(e) for e in item)
    text.close()

if __name__ == "__main__":
    for x in range(0, FILE_COUNT):
        offlineProcess(x)
