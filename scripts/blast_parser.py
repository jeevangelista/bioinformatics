#!/usr/bin/python

#######################################
# Returns a fasta file that contains  #
# the sequences that (0) have Blast   #
# hits (1) have no Blast hits         #
# Created by John Erol M. Evangelista #
#######################################

#TODO: Improve running time

from Bio.Blast import NCBIXML
import sys, getopt
from collections import deque

def main(argv):
  fasta = ''
  xml = ''
  output = ''
  comp = 1
  try:
    opts, args = getopt.getopt(argv,"hi:x:c:o:",["input=","xml=","complement=","output="])
  except getopt.GetoptError:
    print 'blast_parser.py -i <input fasta> -x <blast xml> -o <output>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'Returns a fasta file that contains the sequences that (0) have Blast hits (1) have no Blast hits.'
      print 'blast_parser.py -i <input fasta> -x <blast xml> -c <0 (query hits), 1 (query nonhits)> -o <output>'
      sys.exit()
    elif opt in ("-i", "--input"):
      fasta = arg
    elif opt in ("-x", "--xml"):
      xml = arg
    elif opt in ("-c", "--complement"):
      comp = int(arg)
    elif opt in ("-o", "--output"):
      output = arg
  
  xmls = xml.split()
  query_list = []
  for x in xmls:
    result_handle = open(x)
    blast_records = NCBIXML.parse(result_handle)

    for blast_record in blast_records:
      for alignment in blast_record.alignments:
        # Alignment exists!
        if len(alignment.hsps):
          query_list.append(blast_record.query)
    result_handle.close()
  input_file = open(fasta,'r')
  output_file = open(output,'w')

  #query_list.sort()

  query_list = deque(query_list)

  line = input_file.readline()
  query = query_list.popleft() if query_list else None

  while line and query:
    if line[0] == '>':
      if comp == 0:
        if query in line:
          output_file.write(line)
          line = input_file.readline()
          while line and line[0] != '>':
            output_file.write(line)
            line = input_file.readline()
          query = query_list.popleft() if query_list else None
        else:
          line = input_file.readline()
      elif comp != 0:
        if query in line:
          line = input_file.readline()
          # Equate '######################' instead of None to query so that it'll iterate up to the last line
          query = query_list.popleft() if query_list else '######################' #TODO: Fix this
        else:
          output_file.write(line)
          line = input_file.readline()
          while line and line[0] != '>':
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
