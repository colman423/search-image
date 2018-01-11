#!/usr/bin/env python
# coding=utf-8
import numpy as np
import scipy.cluster.vq as vq
from utility import *
import siftpy as sift
import math

def run(fileName):
    print "input: " + fileName

    fileName += ".q3"
    compareDistance = [0] * FILE_COUNT

    with open(fileName) as f:
        featureList = map(int, f.read().split(' '))
        print featureList

    for x in xrange(FILE_COUNT):
        with open(convertToPathStr(x) + ".q3") as f:
            compareFeatureList = map(int, f.read().split(' '))
            for i in xrange(K_COUNT):
                compareDistance[x] += pow((featureList[i]-compareFeatureList[i]), 2)

    #print "compareDistance: ", compareDistance
    sortArr =  np.argsort(compareDistance)[:10]
    print sortArr
    return [convertToPathStr(ele) for ele in sortArr]


def createSift(i):

    fileName = convertToPathStr(i)
    print fileName

    sift.process_image(fileName, fileName+'.sift')
    #
    # text = open(fileName+".q2", "w")
    # for item in dctResult:
    #     print>>text, ' '.join(str(e) for e in item)
    # text.close()
def doKMeans(siftArr):
    result = vq.kmeans(np.array(siftArr), K_COUNT, check_finite=False)
    print result

    with open("result.txt", "w") as f:
        for item in result[0]:
            print>>f, ' '.join(str(num) for num in item)
        f.close()
    with open("distortion.txt", "w") as f:
        print>>f, result[1]
        f.close()

def countFreq(arr):
    freq = [0]*K_COUNT
    for ele in arr:
        freq[ele] += 1
    return np.argsort(freq)[-int(K_COUNT/20):]


def kMeans():
    siftArr = []
    fileLength = []
    for x in range(0, FILE_COUNT):
        with open(convertToPathStr(x)+'.sift') as f:
            print convertToPathStr(x)
            fileIn = f.read().splitlines()
            fileIn = [(lambda ele: map(float, ele.split())) (item) for item in fileIn]
            fileLength.append(len(fileIn))
            siftArr += fileIn

    # print siftArr
    siftArr = np.array(siftArr)
    print fileLength
    siftArr = vq.whiten(siftArr, check_finite=False)
    print siftArr

    doKMeans(siftArr)

    disArr = []
    with open("result.txt") as f:
        fileIn = f.read().splitlines()
        data = [(lambda ele: map(float, ele.split()[:2]))(item) for item in fileIn]
        print "data: "
        print data
    for item in siftArr:
        x, y = item[:2]
        distances = [ (lambda d: math.hypot(x-d[0], y-d[1]))(d)for d in data ]
        disArr.append(np.argmin(np.array(distances)))

    freqList = countFreq(disArr)
    print freqList

    for i in xrange(len(fileLength)):
        length = fileLength[i]
        featureArr = [0]*K_COUNT

        ls = disArr[:length]
        disArr = disArr[length:]
        for j in ls:
            featureArr[j] += 1
        with open(convertToPathStr(i)+'.q3', 'w') as f:
            print>> f, ' '.join(str(num) for num in featureArr)
            f.close()


        stopFeatureArr = [0]*K_COUNT
        for j in ls:
            stopFeatureArr[j] += 1
        for item in freqList:
            stopFeatureArr[item] = 0
        with open(convertToPathStr(i) + '.q4', 'w') as f:
            print>> f, ' '.join(str(num) for num in stopFeatureArr)
            f.close()


if __name__ == "__main__":
    for x in range(0, FILE_COUNT):
        createSift(x)
    kMeans()
