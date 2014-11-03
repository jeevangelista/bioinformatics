#!/usr/bin/python

#######################################
# Outputs a fasta file from that      #
# contains the sequences specified in #
# the tag file.                        #
# Created by John Erol M. Evangelista #
#######################################


import sys, getopt

def main(argv):
  fasta = ''
  tags = ''
  separator = ' '
  output = ''
  try:
    opts, args = getopt.getopt(argv,"hi:t:s:o:",["input=","tags=","separator=","output="])
  except getopt.GetoptError:
    print 'fasta_parser.py -i <input fasta> -t <tags> -s <separator> -o <output>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'Outputs a fasta file from that contains the sequences specified in the tag file.'
      print 'fasta_parser.py -i <input fasta> -t <tags> -s <separator> -o <output>'
      sys.exit()
    elif opt in ("-i", "--input"):
      fasta = arg
    elif opt in ("-t", "--tags"):
      tags = arg
    elif opt in ("-s", "--separator"):
      separator = arg
    elif opt in ("-o", "--output"):
      output = arg
  

  tag_list = []
  f = open(tags,'r')
  for line in f:
    tag_list.append(line.strip()+separator)
  f.close()

  input_file = open(fasta,'r')
  output_file = open(output,'w')

  line = input_file.readline()
  while line:
    if line[0] == '>':
      # Match
      if any (tag in line for tag in tag_list):
        output_file.write(line)
        line = input_file.readline()
        while line[0] != '>':
          output_file.write(line)
          line = input_file.readline()
      else:
        line = input_file.readline()
    else:
      line = input_file.readline()
  output_file.close()
  input_file.close()
if __name__ == "__main__":
 main(sys.argv[1:])
