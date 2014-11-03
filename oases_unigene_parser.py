#!/usr/bin/python

#######################################
# Gets unigenes by getting the locus  #
# with (1) Greatest confidence score  #
# and in case of a tie (2) longest of #
# the tie                             #
# Created by John Erol M. Evangelista #
#######################################

import sys, getopt, re

def main(argv):
  fasta = ''
  regex = re.compile('[a-zA-Z0-9]*_[a-zA-Z0-9]*')
  conf_regex = re.compile('Confidence_[0-9.]*')
  len_regex =  re.compile('Length_[0-9]*')
  output = ''
  try:
    opts, args = getopt.getopt(argv,"hf:o:",["fasta=", "output="])
  except getopt.GetoptError:
    print 'oases_unigene_parser.py -f <input fasta> -o <output>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('Gets unigenes by getting the locus with (1) Greatest' + 
            ' confidence score and in case of a tie (2) longest of the tie')
      print 'oases_unigene_parser.py -f <input fasta> -o <output>'
      sys.exit()
    elif opt in ("-f", "--fasta"):
      fasta = arg
    elif opt in ("-o", "--output"):
      output = arg

  input_file = open(fasta,'r')
  output_file = open(output,'w')
  unigenes = []
  unigene = ''
  unigene_seq = ''

  line = input_file.readline()
  while line:
    if line[0] == '>':
      # Find regex
      match = regex.search(line)
      len_match = len_regex.search(line)
      conf_match = conf_regex.search(line)
      # header!
      if match and conf_match:
        label = match.group()
        conf_curr = float(conf_match.group()[11:])
        len_curr = int(len_match.group()[7:])
        # new unigene!
        if label != unigene:
          # Unigene not empty. Hindi sa start. Write previous result sa output file
          if len(unigene):
            output_file.write(header)
            output_file.write(unigene_seq)
          # Set value of unigene
          unigene = label
          conf_max = 0
          len_max = 0
          # For testing
          if unigene not in unigenes:
            unigenes.append(unigene)
        if conf_curr > conf_max:
          conf_max = conf_curr
          len_max = len_curr
          header = line
          # copy sequence
          unigene_seq = ''
          line = input_file.readline()
          while line and line[0] != '>':
            unigene_seq += line
            line = input_file.readline()
          if not line:
            output_file.write(header)
            output_file.write(unigene_seq)
        elif conf_curr == conf_max and len_curr > len_max: 
          len_max = len_curr
          header = line
          # copy sequence
          unigene_seq = ''
          line = input_file.readline()
          while line and line[0] != '>':
            unigene_seq += line
            line = input_file.readline()
          if not line:
            output_file.write(header)
            output_file.write(unigene_seq)
        else:
          line = input_file.readline()
    else:
      line = input_file.readline()
  print len(unigenes)
  output_file.close()
  input_file.close()

if __name__ == "__main__":
 main(sys.argv[1:])
