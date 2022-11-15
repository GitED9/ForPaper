import numpy as np
from random import choices
import operator
import functools
import sys
import random 

"""
This class alows to create a complex and simple disease models. To get a Simple model, set all the weights to 1.
"""
class DisaeseModel():

	"""
	Constractor.
	____________
	@ paths: A list where each element represents the number of genes in the path [List].
	@ numberOfCoreGenes: A list where each element represents the number of core genes in the corresponding path [List].
	@ numOfCorePaths: The number of core paths in the model [Int].
	@ numberOfSubTypes: Number of subtypes models in the data set. Each one will have a permutation of the weights.[Int] 
	@ maxDefectiveGenes: A list, compitable to the length of the size list, where each element represents
	  the maximum defective genes allowd in the compitable path before it is considered defective [List].
	@ maxDefectivePaths: The maximum number of defective paths allowed befor the genome is considered sick [Int].
	"""
	def __init__(self, paths, numberOfCoreGenes, numOfCorePaths, weightOfRegularGenes , weightOfRegularPaths 
		, weightOfCorePaths , weightOfCoreGenes, maxPaths , maxGenes , numberOfSubTypes = 1):

		#Convert the paths into a np array.
		self.paths = np.asarray([np.asarray(path) for path in paths])


		self.maxDefectivePaths = maxPaths
		self.maxDefectiveGenes = np.asarray( [ maxGenes for path_length in self.paths])
		
		self.numOfCorePaths = numOfCorePaths
		self.numberOfCoreGenes = numberOfCoreGenes 
		
		self.numberOfSubTypes = numberOfSubTypes

		self.regularPathsWeight = weightOfRegularPaths
		self.regularGenesWeight = weightOfRegularGenes

		self.corePathsWeight = weightOfCorePaths
		self.coreGenesWeight = weightOfCoreGenes

		self.weights = {"GenesWeight":[], "pathsWieght":[]}

		self.calculateWeights(numOfCorePaths,numberOfCoreGenes)
	

	def calculateWeights(self,numOfCorePaths,numberOfCoreGenes):
		#Calculate the wieghts for each path and gene.
		#self.calculateWeights(numOfCorePaths,,genesWeightRange)
		self.calculatePathsWeights(numOfCorePaths)
		self.calculateGenesWeights(numberOfCoreGenes)

		#random.seed(613)
		#print('PAY ATTENTION: The Random might be seeded!')
		for i in range (1, self.numberOfSubTypes):
			self.weights["pathsWieght"].append(np.random.permutation(self.weights["pathsWieght"][0]))
			self.weights["GenesWeight"].append(np.asarray([np.random.permutation(x) for x in self.weights["GenesWeight"][0]]))
			
		print(self.weights)

	
	def calculatePathsWeights(self, numOfCorePaths):
		"""Creating a list for the weights for each path.
	   		The weights for non core paths : 1
		"""	

		self.weights["pathsWieght"].append( [self.corePathsWeight] * numOfCorePaths )		

		#The non core paths will have a weight of 1
		numberOfRegularPaths = len(self.paths) - numOfCorePaths

		self.weights["pathsWieght"][0].extend( [self.regularPathsWeight] * ( numberOfRegularPaths ) )
		

		#random.seed(613)
		#random.shuffle(self.weights["pathsWieght"][0])
		self.weights["pathsWieght"][0] = np.asarray(self.weights["pathsWieght"][0])


	def calculateGenesWeights(self,numberOfCoreGenes):
		"""Creating a matrix for the weights for each gene in each path.
	   		The weights for non core genes in a path: 1
		"""
		self.weights["GenesWeight"].append([])
		
		for i, path_length in enumerate(self.paths):

			current_path_weights = [(self.coreGenesWeight)] * numberOfCoreGenes[i]
			#For regular genes, the weight is 
			number_of_regular_genes = path_length - numberOfCoreGenes [i] 

			current_path_weights.extend([self.regularGenesWeight] * (number_of_regular_genes))
	

			#random.seed(19)
			#random.shuffle(current_path_weights)
			self.weights["GenesWeight"][0].append(current_path_weights)

		self.weights["GenesWeight"][0] = np.asarray(self.weights["GenesWeight"][0])
	
	"""
	   The function writes the genomes into a csv file, ready for ML run.
	   @ genomeArr : A list of lists that represent genomes to be written in to the file.
	   @ fileName  : The name of the file into which the genomes are to be written.
	"""

	def createFile(self,genomeArr,fileName):
		
		#Total number of genes is the length of all nested lists of genome
		totalNumberOfGenes = sum(self.paths)

		#Creating file name:

		#Creating the title
		title = [str(x) for x in range(1, totalNumberOfGenes + 1, 1)]
	
		title = ",".join(title)
		title += ",Health Status\n"


		fileName = open(fileName + ".csv","w")
		fileName.write(title)


		for genome in genomeArr:
			
			healthStatus = genome.pop()

			line = ",".join(str(x) for x in functools.reduce(operator.iconcat, genome, []))

			fileName.write(line + "," + healthStatus + "\n")

		fileName.close()

	"""Returns "Sick" if the genome is sick according to model and "Healthy" otherwise."""
	def healthStatus(self,genome):
		
		flag = "Healthy"

		genome = np.asarray(genome)
		#print("genome",genome)

		for subtype_index in range(self.numberOfSubTypes):

			#print("SubType",subtype_index)
			#print("genes Weight",self.weights["GenesWeight"][subtype_index])

			genesEffect = (genome * self.weights["GenesWeight"][subtype_index]).sum(axis=1)
			
			#print("genesEffect",genesEffect)
			defectiveBoolArr = np.greater(genesEffect, self.maxDefectiveGenes)
			#print("defectiveBoolArr",defectiveBoolArr)
			
			#print("max maxDefectiveGene",self.maxDefectiveGenes)
			#print("pathsWieght",self.weights["pathsWieght"][subtype_index])
			
			pahtsEffect = defectiveBoolArr * self.weights["pathsWieght"][subtype_index]
					
			#print("pahtsEffect",pahtsEffect)
			#print("pahtsEffect.sum()",pahtsEffect.sum())
			#print("maxDefectivePaths",self.maxDefectivePaths)
			
			if pahtsEffect.sum() > self.maxDefectivePaths:
				#print("Sick\n\n")
				#return "Sick"
				flag = "Sick"
			
			#print("Healthy\n\n")
		#print("Healthy","\n\n")
		return flag

