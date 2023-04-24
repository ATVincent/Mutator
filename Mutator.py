#!/usr/bin/env python
import sys, getopt, os, re
from collections import Counter
import fastaparser

def main(argv):


	# Acquisition of arguments 
	try:
		opts, args = getopt.getopt(argv,"hI:D:")
	except getopt.GetoptError:
		print ('Mutator.py -I InputFaa -D DiamondFile')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('Mutator.py -I InputFaa -D DiamondFile')
			sys.exit()
		elif opt in ("-I"):
			InputFile = str(arg)
		elif opt in ("-D"):
			DiamondFile = str(arg)

	Ref_dic = {}
	Align_dic = {}
	Def_dic = {}
	
	with open(InputFile) as fasta_file:
		parser = fastaparser.Reader(fasta_file)
		for seq in parser:
			i=int(1)
			Name = seq.id
			Definition = seq.description
			Sequence = seq.sequence_as_string()

			Def_dic.setdefault(Name, []).append(Definition)
			
			for AA in Sequence:
				Ref_dic.setdefault("%s--%d" %(Name, i), []).append(AA)
				i=i+1


	with open(DiamondFile) as f:
		for line in f:
			line = line.replace('\n', '').replace('\r', '')
			line = line.split("\t") 
			
			Read_dic = {}
			
			Subject_name = str(line[1])
			Subject_length = int(line[2])
			Alignment_start = int(line[3])
			Alignment_stop = int(line[4])
			identity = float(line[6])
			qcov = float(line[7])
			
			CIGAR = str(line[8])
			
			CIGAR_split = re.split('(\D+)',CIGAR)

			# If mutation occurs at the first position of the alignment
			if CIGAR_split[0] == '':
				CIGAR_split.pop(0)
				CIGAR_split.insert(0, 0)
			
			CIGAR_length = int(len(CIGAR_split)-2) # -2 because of the initial 0 and to avoid to count the last number
			
			CIGAR_element = int('0')
			
			if qcov >= float('95') and identity >= float('95'):
	
				while CIGAR_element <= CIGAR_length :
				
					if CIGAR_element == int('0'):
				
						Mutation_position = int(CIGAR_split[CIGAR_element]) + Alignment_start
						Mutation = str(CIGAR_split[CIGAR_element+1])
			
					else:
						Mutation_position = int(CIGAR_split[CIGAR_element]) + Alignment_start + int(CIGAR_split[CIGAR_element-2]) + 1
						Mutation = str(CIGAR_split[CIGAR_element+1])
				
					# to avoid all M->V at the first position
					if Mutation != str('VM') and Mutation_position != int('1') and str('X') not in Mutation:
						Read_dic.setdefault(Mutation_position, []).append(Mutation)
					CIGAR_element = CIGAR_element + 2

			#write in Align.dic ref AA if not in CIGAR, otherwise write the one in the CIGAR
			while Alignment_start <= Alignment_stop:
				
				Ref_AA = Ref_dic["%s--%d" %(Subject_name,Alignment_start)][0]
				
				if Alignment_start in Read_dic:
					Align_dic.setdefault("%s--%d--%s--%d" %(Subject_name,Alignment_start, Ref_AA, Subject_length), []).append(Read_dic[Alignment_start][0][0])
				else:
					Align_dic.setdefault("%s--%d--%s--%d" %(Subject_name,Alignment_start, Ref_AA, Subject_length), []).append(Ref_dic["%s--%d" %(Subject_name,Alignment_start)][0])				
				Alignment_start=Alignment_start+1

		for key in Align_dic:
			ProtName = key.split("--")[0]
			List_of_mut_to_keep = []
			AA_occurence = Counter(Align_dic[key])
			
			# To keep only mutations with more than 5 reads
			for x in AA_occurence:
				if (AA_occurence[x] >= int('20')):
					List_of_mut_to_keep.append("%s--%d" %(x, AA_occurence[x]))
			
			# Keep only if more than one interesting AA
			if len(List_of_mut_to_keep) > 1:
				print (key, end="	")
				for element in List_of_mut_to_keep:
					print (element, end="	")
				print(Def_dic[ProtName][0], end="	")
				print("")
if __name__ == "__main__":
    main(sys.argv[1:])
