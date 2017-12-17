import os

FILE_COUNT = 1006

def convertToPathStr(i):
    return os.getcwd()+"\\dataset\\ukbench"+str(i).zfill(5)+".jpg"