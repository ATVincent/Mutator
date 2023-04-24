#!/usr/bin/env python
import sys, getopt, os, re
from collections import Counter
from operator import itemgetter

def main(argv):


	# Acquisition of arguments 
	try:
		opts, args = getopt.getopt(argv,"hI:")
	except getopt.GetoptError:
		print ('Sort_diamond.py -I DiamondFile')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('Sort_diamond.py -I DiamondFile')
			sys.exit()
		elif opt in ("-I"):
			InputFile = str(arg)


	Diamond_dic = {}
	
	with open(InputFile) as f:
		for line in f:
			line = line.replace('\n', '').replace('\r', '')
			line = line.split("\t") 
			
			Element_list = []
			qseqid = line[0]
			sseqid = line[1]
			slen = line[2]
			sstart = line[3]
			send = line[4]
			evalue = line[5]
			pident = line[6]
			qcovhsp = line[7]
			btop = line[8]
			bitscore = line[9]
			
			Element_list.append(qseqid)
			Element_list.append(sseqid)
			Element_list.append(slen)
			Element_list.append(sstart)
			Element_list.append(send)
			Element_list.append(evalue)
			Element_list.append(pident)
			Element_list.append(qcovhsp)
			Element_list.append(btop)
			Element_list.append(bitscore)
			
			Diamond_dic.setdefault(qseqid, []).append(Element_list)
	
	for key in Diamond_dic:

		if len(Diamond_dic[key]) == int('1'):
			hit_to_retain = Diamond_dic[key][0]
			for element in hit_to_retain:
				print (element, end="	")
			print('')
#		else:
#			sorted_hits = sorted(Diamond_dic[key], key=itemgetter(9), reverse=True)
#			hit_to_retain = sorted_hits[0]
#			for element in hit_to_retain:
#				print (element, end="	")
#			print('')

if __name__ == "__main__":
    main(sys.argv[1:])