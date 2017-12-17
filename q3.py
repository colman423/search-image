#!/usr/bin/env python
# coding=utf-8
import numpy as np
import scipy.cluster
from utility import *
import siftpy as sift


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

    print "compareDistance: ", compareDistance
    sortArr =  np.argsort(compareDistance)[:10]
    print sortArr
    return [convertToPathStr(ele) for ele in sortArr]


def createSift(i):

    fileName = convertToPathStr(0)
    print fileName

    sift.process_image(fileName, fileName+'.sift')
    #
    # text = open(fileName+".q2", "w")
    # for item in dctResult:
    #     print>>text, ' '.join(str(e) for e in item)
    # text.close()

def kMeans():
    siftArr = []
    for x in range(0, 1):
        with open(convertToPathStr(x)+'.sift') as f:
            fileIn = f.read().splitlines()
            for item in fileIn:
                print item
        # vq.kmeans()

if __name__ == "__main__":
    for x in range(0, 1):
        createSift(x)
    kMeans()