#!/usr/bin/env python
# coding=utf-8
import numpy as np
from utility import *

def run(fileName):
    print "input: " + fileName

    fileName += ".q4"
    compareDistance = [0] * FILE_COUNT

    with open(fileName) as f:
        featureList = map(int, f.read().split(' '))
        print featureList

    for x in xrange(FILE_COUNT):
        with open(convertToPathStr(x) + ".q4") as f:
            compareFeatureList = map(int, f.read().split(' '))
            for i in xrange(K_COUNT):
                compareDistance[x] += pow((featureList[i] - compareFeatureList[i]), 2)

    #print "compareDistance: ", compareDistance
    sortArr = np.argsort(compareDistance)[:10]
    print sortArr
    return [convertToPathStr(ele) for ele in sortArr]
