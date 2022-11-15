"""This script filtered out all the sick or the healthy from a file. Originaly created to filter out the healthy created by
shuffeling the sick real data and vise versa"""
import sys

"""
COMMAND LINE PARAMETERS SIMPLE: 
sys.argv[1]= Original data set
sys.argv[2]= Data set after filtering (output)
sys.argv[3]= "Healthy" | "Sick" label
"""


#Original data set
file=open(sys.argv[1],"r")
#Data set after filtering
output=open(sys.argv[2],"w")
#"Healthy" | "Sick"
label_to_filter_in=sys.argv[3]+"\n"

#Write the description line into the new file
output.write(file.readline())

total_genomes=0
genomes_filtered_in=0
filtered_out_genomes_indexes=[]

#write into the new file only the genomes that we want to keep (healthy or sick)
for i,line in enumerate(file):
	total_genomes+=1
	if line.endswith(label_to_filter_in):
		output.write(line)
		genomes_filtered_in+=1
	else:
		filtered_out_genomes_indexes.append(i)

print("\n")
print(f"Number of genomes left after filtering:{genomes_filtered_in} out of {total_genomes} genomes")
print(f"Left persentage:{(genomes_filtered_in/total_genomes)*100} %")
print("Filtered out genomes:",(len(filtered_out_genomes_indexes)/total_genomes)*100)


file.close()
output.close()
