import sys
import math
import random
from random import randrange
from itertools import islice
import functools
import operator
import statistics
import numpy as np
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


def readOriginalDataIntoMartix(input_file_name):

	# Reading the base data
	base_data_file = open(input_file_name, "r")

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
		if line[-1] == "Healthy" or line[-1] == "Sick":
			del line[-1]

		# Add the list created as list of ints
		base_data_matrix.append([int(x) for x in line])
		
	return base_data_matrix,first_line


def shuffleData(input_file_name):

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
	
	return base_data_matrix,first_line


def writeNewMatrixToAfile(file_name, matrix):
	
  output_file = open(file_name, "w+")
 
  for genome in matrix:
    
    line = ",".join(str(x) for x in genome) + "\n"
    
    output_file.write(line)

  output_file.close()



if __name__ == '__main__':
	
	
	input_file = sys.argv[1]
	#input_file = '/content/RealDataCombined_comma.csv'
	base_data_matrix,first_line = shuffled_matrix,first_line = shuffleData(input_file)
	writeNewMatrixToAfile(file_name, matrix)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
