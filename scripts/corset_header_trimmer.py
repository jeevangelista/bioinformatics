#!/usr/bin/python

#######################################
# Trims fasta header to include       #
# clusters only                       #
# Created by John Erol M. Evangelista #
#######################################


import sys, getopt, re

def main(argv):
  fasta = ''
  output = ''
  try:
    opts, args = getopt.getopt(argv,"hi:o:",["input=","output="])
  except getopt.GetoptError:
    print 'corset_header_trimmer.py -i <input fasta> -o <output>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'Trims fasta header to include clusters only.'
      print 'corset_header_trimmer.py -i <input fasta> -o <output>'
      sys.exit()
    elif opt in ("-i", "--input"):
      fasta = arg
    elif opt in ("-o", "--output"):
      output = arg

  corset_header = re.compile('Cluster-[0-9]*.[0-9]*')

  input_file = open(fasta,'r')
  output_file = open(output,'w')

  line = input_file.readline()
  while line:
    if line[0] == '>':
      # Match
      header = corset_header.search(line)
      header = header.group()
      output_file.write(">"+header+"\n")
    else:
      output_file.write(line)
    line = input_file.readline()
  output_file.close()
  input_file.close()
if __name__ == "__main__":
 main(sys.argv[1:])
