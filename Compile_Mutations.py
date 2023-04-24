#!/usr/bin/env python
import sys, getopt, os, re
from collections import Counter

def main(argv):


	# Acquisition of arguments 
	try:
		opts, args = getopt.getopt(argv,"hI:")
	except getopt.GetoptError:
		print ('Compile_Mutations.py -I MutatorFile')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('Compile_Mutations.py -I MutatorFile')
			sys.exit()
		elif opt in ("-I"):
			InputFile = str(arg)

	Prot_dic = {}
	Def_dic = {}
	with open(InputFile) as f:
		for line in f:
			line = line.replace('\n', '').replace('\r', '')
			line = line.split("\t") 
			
			gene_name = str(line[0].split("--")[0])
			Position = int(line[0].split("--")[1])
			Ref_AA = str(line[0].split("--")[2])
			length = int(line[0].split("--")[3])
			Definition = str(line[-2])

			if ("%s--%d" %(gene_name, length) not in Def_dic):
				Def_dic.setdefault("%s--%d" %(gene_name, length), []).append(Definition)
				

			for element in line:
				# keep only mutations by removing the gene name and the description
				if not element.startswith(gene_name) and '--' in element:
					Mutated_AA = str(element.split("--")[0])
					# Remove the reference AA to keep only those are mutator
					if Mutated_AA != Ref_AA:
						Prot_dic.setdefault("%s--%d" %(gene_name, length), []).append("%s--%d" %(element, Position))
						
		for key in Prot_dic:
			length = float(key.split("--")[1])
			Number_of_Mutation = float(len(Prot_dic[key]))
			
			Percentage = (Number_of_Mutation*100)/length
			
			Definition = Def_dic[key][0]
			
			print (key, end="	")
			print (Percentage, end="	")
			print (Definition, end="	")
			
			for Mutation in Prot_dic[key]:
				print (Mutation, end="	")
			
			print ('')
			
if __name__ == "__main__":
    main(sys.argv[1:])