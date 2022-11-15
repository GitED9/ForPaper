import sys
import random 
import os

"""
This script gets as input a file with correct labels according to some model and number of SNPs to be deleted 
and then it deletes them and leaves the genome with the original label.
It's done to try and see how the algorithms deals with lack of data.

input: 
sys[1] = file after check (with corret labels).
sys[2] = number of SNPs to be deleted.

"""

def createEmptyListOfColumnss(number_of_rows):
	
	columns_list = []
	for i in range(number_of_rows):
		columns_list.append([])

	return columns_list

def readFileIntoRowList(original_file):
	
	first_line = original_file.readline().strip().split(",")
	columns_list = createEmptyListOfColumnss(len(first_line))

	for i,gene in enumerate(first_line):
		columns_list[i].append(gene)


	for line in original_file:
		line = line.strip().split(",")
		for i,gene in enumerate(line):
			columns_list[i].append(gene)
	
	return columns_list

def deleteSNPs(number_of_SNPs_to_add, columns_list):

	columnt_to_delet = random.sample(range(0, (len(columns_list) - 1)), number_of_SNPs_to_add)
	for i in sorted(columnt_to_delet, reverse=True):
		del columns_list[i]
	
	"""
	first_index = (-1) * (number_of_SNPs_to_add + 1)
	del columns_list [first_index:-1]
	"""
	return columns_list

def writeOutputToAFile(columns_list, output_file_name):
	
	output = open (output_file_name, "w")
	number_of_columns = len(columns_list)

	number_of_rows = len(columns_list[0])

	for i in range(number_of_rows):
		for j in range(number_of_columns):
			if j == 0 :
				output.write(columns_list[j][i])
			else:
				output.write(f",{columns_list[j][i]}")
		output.write("\n")

	output.close()

	print(f"The file after added columns is in {output_file_name}")

def outputNameCreator(original_file_name, number_of_SNPs_to_add, output_path):
	
	original_file_name = original_file_name.strip().split("/")[-1]

	original_file_name = original_file_name.strip().split("_")
	size = original_file_name[-2:]
	del original_file_name[-2:]
	output_prefix = f'{"_".join(original_file_name)}_Lack_{number_of_SNPs_to_add}_{size[0]}'
	output_file_name = f'{output_path}{output_prefix}_{size[1]}'

	return output_file_name, output_prefix


if __name__ == '__main__':

	original_file_name = sys.argv[1]
	per_of_SNPs_to_delete = int (sys.argv[2])
	output_path = sys.argv[3]

	original_file = open(original_file_name, "r")

	output_file_name, output_prefix = outputNameCreator(original_file_name, per_of_SNPs_to_delete, output_path)
	

	columns_list = readFileIntoRowList(original_file)
	number_of_SNPs_to_delete = int( (per_of_SNPs_to_delete / 100) * (len(columns_list) - 1) )
	columns_list = deleteSNPs (number_of_SNPs_to_delete, columns_list)
	writeOutputToAFile(columns_list, output_file_name)







