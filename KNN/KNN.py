#coding=utf-8
'''
date:2017.04
author:zxgao
'''
from numpy import *
import operator
def createDataset():
	groups=array([[1.0,1.1],[1.0,1.0],[0.0,0.0],[0,0.1]])
	labels=['A','A','B','B']
	return groups,labels

def classify0(inX,dataset,labels,k):
	datasetSize=inX.shape[0]
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



	