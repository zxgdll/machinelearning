import KNN
import KNN2
def main():
	groups,labels=KNN.createDataset()
	res=KNN.classify0([0,0],groups,labels,3)
	dataMat,datalabel=KNN.file2matrix('datingTestSet2.txt')
	dataNM,rangeNM,dataminNM=KNN.autoNorm(dataMat)
	# KNN.dataClassTest()
	KNN.personClass()
	#print dataNM
	# print dataMat,type(dataMat)
#main()
# testMat=KNN.img2vec('digits/testDigits/0_13.txt')
# print testMat[0,0:31],'\n',testMat[0,32:63]
print KNN2.handwritingClassTest()