#!/usr/bin/python

#######################################
# Gets the longest, shortest, mean    #
# length and N50 for Trinity assembly #
# Created by John Erol M. Evangelista #
#######################################

#TODO: Add support for Oases and SoapDenovo-Trans

from __future__ import division
import sys, getopt, re

def main(argv):
  fasta = ''
  len_regex =  re.compile('len=[0-9]*')
  output = ''
  try:
    opts, args = getopt.getopt(argv,"hf:o:",["fasta=", "output="])
  except getopt.GetoptError:
    print 'fasta_summarizer.py -f <input fasta> -o <output>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'Gets the longest, shortest, mean length and N50 for Trinity assembly'
      print 'fasta_summarizer.py -f <input fasta> -o <output>'
      sys.exit()
    elif opt in ("-f", "--fasta"):
      fasta = arg
    elif opt in ("-o", "--output"):
      output = arg

  input_file = open(fasta,'r')
  lengths = []
  shortest = 1000000
  longest = 0

  line = input_file.readline()
  while line:
    if line[0] == '>':
      # Find regex
      len_match = len_regex.search(line)
      len_curr = int(len_match.group()[4:])
      lengths.append(len_curr)
      if len_curr < shortest:
        shortest = len_curr
      if len_curr > longest:
        longest = len_curr
      line = input_file.readline()
    else:
      line = input_file.readline()
  input_file.close()

  #N50
  lengths.sort(reverse=True)
  total = sum(lengths)
  n50=0
  l50=0
  for l in lengths:
    n50+=l
    l50+=1
    if n50 >= total/2:
      break

  output_file = open(output,'w')
  output_file.write("Longest gene is %d \n" % longest)
  output_file.write("Shortest gene is %d\n" % shortest)
  output_file.write("Mean length is %f\n" % (sum(lengths)/len(lengths)))
  output_file.write("n50 is %d \n" % l)
  output_file.close()
if __name__ == "__main__":
 main(sys.argv[1:])
