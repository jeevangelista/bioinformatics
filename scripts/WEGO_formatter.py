#!/usr/bin/python

#######################################
# Formats a GO file to WEGO's native  #
# format.                              #
# Created by John Erol M. Evangelista #
#######################################

import sys, getopt, csv

def main(argv):
  go_annot = ''
  output = ''
  try:
    opts, args = getopt.getopt(argv,"hi:o:",["input=","output="])
  except getopt.GetoptError:
    print 'WEGO_formatter.py -i <GO file> -o <output>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print "Formats a GO file to WEGO's native format" 
      print 'WEGO_formatter.py -i <GO file> -o <output>'
      sys.exit()
    elif opt in ("-i", "--input"):
      go_annot = arg
    elif opt in ("-o", "--output"):
      output = arg
  

  with open(go_annot, 'r') as go:
    with open(output,'w') as out:
      curr_seq = ''
      next_seq = ''
      string = ''
      annot = ''
      for line in csv.reader(go, dialect="excel-tab"):
        next_seq = line[0]
        if curr_seq != next_seq:
          out.write(string+'\n')
          curr_seq = next_seq
          string = line[0] +'\t' + line[2]
        else:
          string = string  + "\t" + line[2]
        print line[0], line[2]
if __name__ == "__main__":
 main(sys.argv[1:])
