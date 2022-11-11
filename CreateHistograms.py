import matplotlib.pyplot as plt
import sys
from matplotlib.ticker import PercentFormatter
import numpy as np




def create_Histogram(input_file, hist_name, title):

	healthy_0_list = []
	healthy_1_list = []
	healthy_2_list = []

	sick_0_list = []
	sick_1_list = []
	sick_2_list = []

	sick_counter = 0 
	healthy_counter = 0

	for line in input_file:

		line = line.strip().split(",")
		#In case the data contatins already a health status- delete it.
		zero_count = line.count("0")
		one_count = line.count("1")
		two_count = line.count("2")

		
		if line[-1] == "Healthy":
			healthy_0_list.append(zero_count)
			healthy_1_list.append(one_count)
			healthy_2_list.append(two_count)
			healthy_counter += 1


		if line[-1] == "Sick":
			sick_0_list.append(zero_count)
			sick_1_list.append(one_count)
			sick_2_list.append(two_count)
			sick_counter += 1



	print("Healthy 0 average", np.mean(healthy_0_list))
	print("Healthy 0 stdvp", np.std(healthy_0_list))
	print("Healthy 0 median", np.median(healthy_0_list))

	print("\n")
	print("Healthy 1 average", np.mean(healthy_1_list))
	print("Healthy 1 stdvp", np.std(healthy_1_list))
	print("Healthy 1 median", np.median(healthy_1_list))

	print("\n")
	print("Healthy 2 average", np.mean(healthy_2_list))
	print("Healthy 2 stdvp", np.std(healthy_2_list))
	print("Healthy 2 median", np.median(healthy_2_list))
	print("\n")

	print("Sick 0 average", np.mean(sick_0_list))
	print("Sick 0 stdvp", np.std(sick_0_list))
	print("Sick 0 median", np.median(sick_0_list))
	print("\n")

	print("Sick 1 average", np.mean(sick_1_list))
	print("Sick 1 stdvp", np.std(sick_1_list))
	print("Sick 1 median", np.median(sick_1_list))
	print("\n")

	print("Sick 2 average", np.mean(sick_2_list))
	print("Sick 2 stdvp", np.std(sick_2_list))
	print("Sick 2 median", np.median(sick_2_list))





	#plt.figure(figsize=(6,6))
	#plt.hist([healthy_0_list, sick_0_list], weights= [np.ones(healthy_counter) / healthy_counter , np.ones(sick_counter) / sick_counter ],hatch='/', ec='k', color = ['steelblue', 'indianred'])
	plt.hist([healthy_0_list, sick_0_list], weights= [np.ones(healthy_counter) / healthy_counter , np.ones(sick_counter) / sick_counter ], ec='k', color = ['steelblue', 'indianred'])

	plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
	plt.xlim([5,35])
	plt.tick_params(labelsize=10.5)
	plt.title(f"Histogram of Zero's (0) For The {title} ", fontsize = 14, pad = 12)
	plt.legend(['Healthy','Sick'],  prop={'size': 13})
	plt.xlabel('Number of zero\'s in a genotype', fontsize = 13)
	plt.ylabel('Percentage of genotypes', fontsize = 13)
	plt.tight_layout()
	plt.savefig(f"{hist_name}_0.png")
	plt.close() 


	#For hiched
	#plt.hist([healthy_1_list, sick_1_list], weights= [np.ones(healthy_counter) / healthy_counter , np.ones(sick_counter) / sick_counter ],hatch='/',ec='k', color = ['steelblue', 'indianred'])

	#For not hiched
	plt.hist([healthy_1_list, sick_1_list], weights= [np.ones(healthy_counter) / healthy_counter , np.ones(sick_counter) / sick_counter ],ec='k', color = ['steelblue', 'indianred'])

	plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
	plt.xlim([5,35])
	plt.tick_params(labelsize=10.5)
	plt.title(f"Histogram of One's (1) For The {title}", fontsize=14, pad = 12)
	plt.legend(['Healthy','Sick'], prop={'size': 13})
	plt.xlabel('Number of one\'s in a genotype', fontsize = 13)
	plt.ylabel('Percentage of genotypes', fontsize = 13)
	plt.tight_layout()
	plt.savefig(f"{hist_name}_1.png")
	plt.close()

	#plt.hist([healthy_2_list,sick_2_list], weights= [np.ones(healthy_counter) / healthy_counter , np.ones(sick_counter) / sick_counter ],hatch='/', ec='k', color = ['steelblue', 'indianred'])
	plt.hist([healthy_2_list,sick_2_list], weights= [np.ones(healthy_counter) / healthy_counter , np.ones(sick_counter) / sick_counter ], ec='k', color = ['steelblue', 'indianred'])

	plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
	plt.xlim([5,35])
	plt.tick_params(labelsize=10.5)
	plt.title(f"Histogram of Two's (2) For The {title} ", fontsize=14, pad = 12)
	plt.legend(['Healthy','Sick'], prop={'size': 13})
	plt.xlabel('Number of two\'s in a genotype', fontsize = 13)
	plt.ylabel('Percentage of genotypes', fontsize = 13)
	plt.tight_layout()
	plt.savefig(f"{hist_name}_2.png")
	plt.close()


"""
This script creates three histograms of healthy and sick indiciduals, one histogram for the
zero values, one for the ones and the third for the twos. Histograms are saved as png files.

sys.argv[1] - a path to a csv file where each row is a 'sample' and each columns a gene. The
last columns is the health status ('Healthy' or 'Sick')

hist_name[2] - the title of the histogram

"""
if __name__ == '__main__':


	input_file = sys.argv[1]
	hist_name = sys.argv[2]
	input_file = open(input_file,"r")
	input_file = input_file.readlines()

	if len(sys.argv) == 4:
		title = sys.argv[3]
	else:
		title = hist_name

	del input_file[0]

	create_Histogram(input_file, hist_name, title)