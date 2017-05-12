#coding=utf-8
from numpy import *
import operator
import os
def classify0(inX,dataset,labels,k):
    datasetSize=dataset.shape[0]
    diffMat=tile(inX,(datasetSize,1))-dataset   #tile 为扩充数组函数，两个参数，第一个参数为扩充的元素，第二参数为一个二元元组，表示扩充的行和列
    sqDiffMat=diffMat**2
    sqDistances=sqDiffMat.sum(axis=1)      #axis 表示计算每一行
    distances=sqDistances**0.5
    sortedDisIndices=distances.argsort()   #.argsort() 表示从小到大排序，输出为元素原始的角标
    classCount={}
    for i in range(k):
        indicslabel=labels[sortedDisIndices[i]]
        classCount[indicslabel]=classCount.get(indicslabel,0)+1
    sortedLabels=sorted(classCount.items(),key=lambda d:d[1],reverse=True)
    return sortedLabels[0][0]
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

def handwritingClassTest(testdata):
    hwLabels = []
    trainingFileList = os.listdir('digits/trainingDigits')           
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i] 
        classNumStr = int(fileNameStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('digits/trainingDigits/%s' % fileNameStr)
    # testFileList = os.listdir('digits/testDigits')        
    errorCount = 0.0
    # mTest = len(testFileList)
    # for i in range(mTest):
    #     fileNameStr = testFileList[i]   
    #     classNumStr = int(fileNameStr.split('_')[0])
    # vectorUnderTest = img2vector(Testdata)
    classifierResult = classify0(array(testdata), trainingMat, hwLabels, 3)
    return classifierResult
    # print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
    # if (classifierResult != classNumStr): errorCount += 1.0
    # print "\nthe total number of errors is: %d" % errorCount
    # print "\nthe total error rate is: %f" % (errorCount/float(mTest))



def train(training_data_Array):
    for data in training_data_Array:
	   with open('digits/trainingDigits/%d_%d.txt'%(data['label'],random.randint(500,1000)),'w') as f:
            for i in range(0,993,32):
                line=''.join([str(j) for j in data['y0'][i:i+32]])
                f.write(line+'\n')
            f.close()
            print "data is saved!!!!"