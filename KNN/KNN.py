from numpy import *
import operator
def createDataset():
	groups=array([[1.0,1.1],[1.0,1.0],[0.0,0.0],[0,0.1]])
	labels=['A','A','B','B']
	return groups,labels
def classify0(inX,dataset,labels,k):
	datasetSize=inX.shape[0]
	