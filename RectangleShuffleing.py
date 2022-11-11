import sys
import math
import random
from random import randrange
from SimpleDiseaseGeneratorByGene import DisaeseModel
from ComplexDiseaseGeneragor import ComplexDisaeseModel
from itertools import islice
import functools
import operator
import statistics
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import logging
import os

def randomizeIndex(ncol, nrow):

	# randomize two columns (genes)
	gene1 = randrange(ncol)
	gene2 = randrange(ncol)

	# randomize four rows (genomes), two for each column(gene)
	genome1 = []
	# Get the first index
	genome1.append(randrange(nrow))

	# As long as the new index is the same as the one already picked,
	# randomize a different one.
	temp = randrange(nrow)
	while temp == genome1[0]:
		temp = randrange(nrow)

	genome1.append(temp)
	genome1.sort()

	return gene1,gene2,genome1

def createPathsInGenome(genome,paths):
	genome = iter(genome) 
	Output = [list(islice(genome, elem)) for elem in paths] 

	return Output

def writeNewMatrixToAfile(file_name, matrix, first_line,disease):
	
	output_file = open(file_name, "w+")

	#If the desctiption line did not include the "health status", add it
	if not first_line.strip().endswith("status"):
		first_line=first_line.strip()+",health status\n"

	output_file.write(first_line)

	healthStatus_counter={"Healthy":0,"Sick":0}

	for genome in matrix:
			
			genome=createPathsInGenome(genome,disease.paths)
			
			#print("Now")
			healthStatus = disease.healthStatus(genome)
			
			healthStatus_counter[healthStatus]+=1

			line = ",".join(str(x) for x in functools.reduce(
				operator.iconcat, genome, []))

			output_file.write(line + "," + healthStatus + "\n")

	output_file.close()

	return healthStatus_counter


def readOriginalDataIntoMartix(input_file_name):


	try:
		# Reading the base data
		base_data_file = open(input_file_name, "r")
		
	except IOError:
		print(f"ahmm, Eden? don't kill me but... {input_file_name} is not a real file....")
		exit()
		


	# The matrix that holds the data as list of lists
	base_data_matrix = []

	# Is this the first line? if it is-> skip it.
	first_line_flag = True


	# Create a matrix that holds all the data from the base data set.

	for line in base_data_file:

		# Is this the first line? if it is-> keep it and skip it.
		if first_line_flag:
			first_line = line
			first_line_flag = False
			continue

		
		# make a list of each line (corresponding to a genome)
		line = line.strip().split(",")

		#In case the data contatins already a health status- delete it.
		if line[-1]=="Healthy" or line[-1]=="Sick":
			del line[-1]


		# Add the list created as list of ints
		base_data_matrix.append([int(x) for x in line])


	return base_data_matrix,first_line

def shuffleData(input_file_name):
	#subprocess.call('echo "Shuffeling has started." | mail -s "CreateDiseaseByShuffeling" edenmaimon6@gmail.com', shell=True)
	base_data_matrix,first_line = readOriginalDataIntoMartix(input_file_name)
	# Size of the matrix= number of inner lists X the len of an inner list (as
	# they all in the same length).

	ncol = len(base_data_matrix[0])
	nrow = len(base_data_matrix)

	"""--------------Test----------------------------"""

	#Random 10 unique genomes.

	print("nrow", nrow)
	if nrow <= 1 : 
		print(f"Not enough rows left! only :{nrow} rows")
		exit()
	random_genomes_for_test = random.sample(range(0,nrow), 2)

	
	#Create a dictionary of a ganome-
	#genomes_matches_through_shuffeling=[]
	#genomes_matches_through_shuffeling.append(np.sum(np.asarray(base_data_matrix[random_genomes_for_test[0]])==np.asarray(base_data_matrix[random_genomes_for_test[1]])))
	"""--------------Test-----------------------------"""
	
	total_size_of_matrix = nrow * ncol

	# Number of shuffles required =size*log2(size):
	num_of_shuffle = total_size_of_matrix * math.log2(total_size_of_matrix)
	#num_of_shuffle = 200

	shuffles_done = 0

	while shuffles_done < num_of_shuffle:

		#print((shuffles_done/num_of_shuffle)*100,"%")
		#print(genomes_matches_through_shuffeling)
		gene1, gene2, genome1 = randomizeIndex(ncol, nrow)


		"""--------------Test-----------------------------"""

		#if genome1[0] in  random_genomes_for_test and genome1[1] in random_genomes_for_test:
		#	genomes_matches_through_shuffeling.append(np.sum(np.asarray(base_data_matrix[genome1[0]])==np.asarray(base_data_matrix[genome1[1]])))
			
		"""--------------Test-----------------------------"""
		
		#print(gene1,genome1)
		
		# check if the four could be swapped:
		if (base_data_matrix[genome1[0]][gene1] == base_data_matrix[genome1[1]][gene2] and
				base_data_matrix[genome1[1]][gene1] == base_data_matrix[genome1[0]][gene2] and
				base_data_matrix[genome1[0]][gene1] != base_data_matrix[genome1[1]][gene1]):

			#print("Before",base_data_matrix[genome1[0]][gene1],base_data_matrix[genome1[1]][gene1],base_data_matrix[genome1[0]][gene2],base_data_matrix[genome1[1]][gene2])

			# Swap each row values with themselves.
			base_data_matrix[genome1[0]][gene1], base_data_matrix[genome1[1]][gene1] = base_data_matrix[genome1[1]][gene1],base_data_matrix[genome1[0]][gene1]
			base_data_matrix[genome1[0]][gene2], base_data_matrix[genome1[1]][gene2] = base_data_matrix[genome1[1]][gene2],base_data_matrix[genome1[0]][gene2]

			
			#print("After",base_data_matrix[genome1[0]][gene1],base_data_matrix[genome1[1]][gene1],base_data_matrix[genome1[0]][gene2],base_data_matrix[genome1[1]][gene2])

			shuffles_done += 1

	#print("The two genomes selected for the test are:",random_genomes_for_test)
	#print("AVG shuffled genes for the two genomes:",statistics.mean(genomes_matches_through_shuffeling))
	#plt.plot(genomes_matches_through_shuffeling,'ro')
	#plt.savefig("twoGenomesMatch.png")
	
	#subprocess.call('echo "Shuffeling is done." | mail -s "CreateDiseaseByShuffeling" edenmaimon6@gmail.com', shell=True)
	
	return base_data_matrix,first_line




"""
Fileds of the model
paths, numberOfSubTypes,, maxDefectiveGenes=3, maxDefectivePaths=2,zeroDes, oneDes, TwoDes, 
		alloweDeviation=100
"""
def createSimpleDiseaseModel(paths):
	"""Create a disase model fit for a simple models.
	"""
	maxDefectiveGenes=float(sys.argv[3])
	maxDefectivePaths=float(sys.argv[4])
	numberOfSubTypes=int(sys.argv[5])

	disease = DisaeseModel(paths, numberOfSubTypes,maxDefectiveGenes,maxDefectivePaths)

	return disease

def createComplexDisaseModel(paths):
	
	"""Create a disase model fit for a complex models:

		self, paths, numberOfCoreGenes, numOfCorePaths, weightOfRegularGenes , weightOfRegularPaths 
		, weightOfCorePaths , weightOfCoreGenes, maxPaths , maxGenes , numberOfSubTypes = 1 ,
		zeroOdd = 0,oneOdds = 0, twoOdds = 0 ,zeroDes = zeroDes, oneDes = oneDes, TwoDes = TwoDes, alloweDeviation = 0
	
	"""
	
	
	"""
	maxGenes = 23
	maxPaths = 11
	

	numOfCorePaths = 3
	weightOfCorePaths = 5

	numberOfCoreGenes = [3] * 8
	weightOfCoreGenes = 5

	#Genes
	weightOfRegularGenes = 2 
	

	#Paths
	weightOfRegularPaths = 2.2
	
	

	number_Of_SubTypes = 1
	
	"""

	numberOfGenes = int(sys.argv[3])
	numberOfPaths = int(sys.argv[4])
	
	maxGenes = float(sys.argv[5])
	maxPaths = float(sys.argv[6])

	paths= [numberOfGenes] * numberOfPaths


	numOfCorePath = int(sys.argv[7])
	corePathWeight = float(sys.argv[8])

	numOfCoreGenes = [int(sys.argv[9])] * numberOfPaths
	coreGeneWeight = float(sys.argv[10])

	regGeneWeight = float(sys.argv[11])

	number_Of_SubTypes = 1
	#regPathWeight = maxPaths / number of regular genes
	regPathWeight = (maxPaths / (numberOfPaths - numOfCorePath))
	#regPathWeight = 1
	#print(f"numberOfGenes :{numberOfGenes}\n numberOfPaths: {numberOfPaths}\n  maxGenes: {maxGenes}")
	#print(f"maxPaths :{maxPaths}\n numOfCorePath: {numOfCorePath}\n  corePathWeight: {corePathWeight}")
	#print(f"numOfCoreGenes :{numOfCoreGenes}\n coreGeneWeight: {coreGeneWeight}\n  regGeneWeight: {regGeneWeight}\n")

	disease = ComplexDisaeseModel(paths, numOfCoreGenes, numOfCorePath, regGeneWeight,
		 regPathWeight, corePathWeight , coreGeneWeight, maxPaths, maxGenes, number_Of_SubTypes)
	random.seed()
	return disease

if __name__ == '__main__':
	
	#Is the disease complex or simple?
	type_of_disease_model = sys.argv[1]
	#The name of the file to be shuffled
	input_file_name = sys.argv[2]
	#[number of genes in each path] * number of paths
	paths = [6]*8

	#Create the model and extract the parameters accorrding to weather the disease is simple or complex.
	if (type_of_disease_model == "Simple" ) :
		output_file = sys.argv[6]
		disease = createSimpleDiseaseModel(paths)

	elif (type_of_disease_model == "Complex" ):
		output_file = sys.argv[12]
		disease = createComplexDisaseModel(paths)
	
	shuffled_matrix,first_line = shuffleData(input_file_name)
	
	#file_name, matrix, first_line,disease
	health_Status_counter = writeNewMatrixToAfile(output_file,shuffled_matrix,first_line,disease)

	print("Health status", health_Status_counter)

	print("Sick precentage", (health_Status_counter["Sick"] / (health_Status_counter["Sick"] + health_Status_counter["Healthy"]))*100)
	print("Healthy precentage", (health_Status_counter["Healthy"] / (health_Status_counter["Sick"] + health_Status_counter["Healthy"]))*100)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

"""
COMMAND LINE PARAMETERS SIMPLE: 
sys.argv[1]= type_of_disease_model (Simple)
sys.argv[2]= file name of the base Data to be shuffled.
sys.argv[3]= maxDefectiveGenes
sys.argv[4]= maxDefectivePaths
sys.argv[5]= numberOfSubTypes
sys.argv[6]= output file name
"""

"""
COMMAND LINE PARAMETERS Complex: 
sys.argv[1]= type_of_disease_model (Complex)
sys.argv[2]= file name of the base Data to be shuffled.
sys.argv[3]= numberOfGenes
sys.argv[4]= numberOfPaths
sys.argv[5]= maxGenes
sys.argv[6]= maxPaths 
sys.argv[7]= numOfCorePath
sys.argv[8]= corePathWeight
sys.argv[9]= numOfCoreGenes
sys.argv[10]= coreGeneWeight
sys.argv[11]= regGeneWeight
sys.argv[12]= output file name
"""






