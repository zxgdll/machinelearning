#!/usr/bin/env python
#coding=utf-8
#BP神经网络模型实现
#作者：zxgao
#BP神经网络原理：http://www.hankcs.com/ml/back-propagation-neural-network.html
import math
import random
random.seed(0)

def rand(a,b):
	"""
	生成一个(a,b)范围内的随机数
	"""
	return (b-a)*random.random()+a
def makeMatrix(m,n,fill=0.0):
	"""
	创建矩阵，行数为：m,列数为：n
	填充 0.0
	"""
	res=[]
	for x in range(m):
		res.append([fill]*n)
	return res
def randomMatrix(matrix,a,b):
	"""
	随机初始矩阵
	"""
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			matrix[i][j]=random.uniform(a,b)
def sigmoid(x):
	"""
	BP神经网络使用的激励函数：单极性神经网络
	f(x)=1/(1+exp(-x))
	"""
	return 1.0/(1.0+math.exp(-x))
def dsigmoid(y):
	"""
	单极性sigmoid激励函数的求导结果
	"""
	return y*(1-y)

class BPnn:
	"""
	BP神经网络的具体实现
	BP神经网络分为三层：输入层、隐藏层、输出层
	ni:输入层节点个数，
	nh:隐藏层节点个数
	no:输出节点个数
	"""
	def __init__(self,ni,nh,no):
		#输入的节点数 需要多加一个偏置节点
		self.ni=ni+1 
		self.nh=nh
		self.no=no

		#输出值
		self.ai=[1.0]*self.ni
		self.ah=[1.0]*self.nh
		self.ao=[1.0]*self.no

		#权重矩阵
		self.wi=makeMatrix(self.ni,self.nh)
		self.wo=makeMatrix(self.nh,self.no)

		#随机化权重
		randomMatrix(self.wi,-0.2,0.2)
		randomMatrix(self.wo,-2.0,2.0)

		#权重矩阵的上次梯度
		self.ci=makeMatrix(self.ni,self.nh)
		self.co=makeMatrix(self.nh,self.no)

	def run(self,inputs):
		"""
		前向传播
		"""
		if len(inputs)!=self.ni-1:
			print "incorrect number of inputs!"
		#输入值等于x_i
		for i in range(self.ni-1):
			self.ai[i]=inputs[i]
		#得到隐藏层节点值
		for j in range(self.nh):
			sum=0.0
			for x in range(self.ni):
				sum+=(self.wi[x][j]*self.ai[x])
			self.ah[j]=sigmoid(sum)
		#得到输出节点值
		for k in range(self.no):
			sum=0.0
			for x in range(self.nh):
				sum+=(self.ah[x]*self.wo[x][k])
			self.ao[k]=sigmoid(sum)
		return self.ao
	def bp(self,target,N,M):
		"""
		反向传播算法，从输出层开始
		"""
		#输出层delta
		out_delta=[0.0]*self.no
		for x in range(self.no):
			error=target[x]-self.ao[x]
			out_delta[x]=error*dsigmoid(self.ao[x])
		#更新输出权值矩阵
		for j in range(self.nh):
			for k in range(self.no):
				change=out_delta[k]*self.ah[j]
				self.wo[j][k]+=N*change+M*self.co[j][k]
				self.co[j][k]=change
		#隐藏层delta
		hidden_delta=[0.0]*self.nh
		for x in range(self.nh):
			error=0.0
			for j in range(self.no):
				error+=out_delta[j]*self.wo[x][j]
			hidden_delta[x]=error*dsigmoid(self.ah[x])
		#更新隐藏层权值矩阵
		for i in range(self.ni):
			for j in range(self.nh):
				change=hidden_delta[j]*self.ai[i]
				self.wi[i][j]+=N*change+M*self.ci[i][j]
				self.ci[i][j]=change
		#计算总误差
		error=0.0
		for x in range(len(target)):
			error=0.5*(target[x]-self.ao[k])**2
		return error
	def weight(self):
		"""
		打印权值矩阵
		"""
		print "输入权值矩阵："
		for i in range(self.ni):
			print self.wi[i]
		print "输出权值矩阵："
		for x in range(self.nh):
			print self.wo[i]
	def test(self,patterns):
		"""
		测试文件
		"""
		for p in patterns:
			input=p[0]
			print 'Input:',p[0],'--->',self.run(input),'\ttarget',p[1]
	def train(self,patterns,max_iterations=1000,N=0.5,M=0.1):
		"""
		训练
		"""
		for i in range(max_iterations):
			for p in patterns:
				input=p[0]
				target=p[1]
				self.run(input)
				error=self.bp(target,N,M)
			if i%50==0:
				print "Combined error",error
		self.test(patterns)
def main():
	pat=[
	[[0,0],[1]],
	[[0,1],[1]],
	[[1,0],[1]],
	[[1,1],[0]]
	]
	myNN=BPnn(2,2,1)
	myNN.train(pat)
	myNN.test([[[2,1],[1]]])
if __name__ == '__main__':
	main()
		
