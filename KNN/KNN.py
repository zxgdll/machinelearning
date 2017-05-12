#coding=utf-8
'''
date:2017.04
author:zxgao
'''
from numpy import *
import operator
import os
def createDataset():
	groups=array([[1.0,1.1],[1.0,1.0],[0.0,0.0],[0,0.1]])
	labels=['A','A','B','B']
	return groups,labels

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

#真实数据 约会网站决策
#文本解析
def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())         #get the number of lines in the file
    returnMat = zeros((numberOfLines,3))        #prepare matrix to return
    classLabelVector = []                       #prepare labels return   
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector
    
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))   
    return normDataSet, ranges, minVals
   
def dataClassTest():
    hoRatio = 0.50      
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')       
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))
    print errorCount
    
def personClass():
	resultlist=['not at all','in small doses','in large doses']
	pTa=float(raw_input("percentage game:"))
	fymile=float(raw_input('mile:'))
	icemuch=float(raw_input('how much:'))
	datingMat,datingLabels=file2matrix('datingTestSet2.txt')
	normMat,ranges,minVals=autoNorm(datingMat)
	inArr=array([fymile,pTa,icemuch])
	classResult=classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
	print 'the decision:%s'%(resultlist[classResult-1])

def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

def handwritingClassTest():
    hwLabels = []
    trainingFileList = os.listdir('digits/trainingDigits')           
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i] 
        classNumStr = int(fileNameStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('digits/trainingDigits/%s' % fileNameStr)
    testFileList = os.listdir('digits/testDigits')        
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]   
        classNumStr = int(fileNameStr.split('_')[0])
        vectorUnderTest = img2vector('digits/testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
        if (classifierResult != classNumStr): errorCount += 1.0
    print "\nthe total number of errors is: %d" % errorCount
    print "\nthe total error rate is: %f" % (errorCount/float(mTest))

	