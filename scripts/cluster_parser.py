#!/usr/bin/python

#######################################
# Outputs a fasta file from that      #
# contains the longest representative # 
# sequences from a cluster file       #
# Created by John Erol M. Evangelista #
#######################################


import sys, getopt, re

def main(argv):
  fasta = ''
  cluster = ''
  output = ''
  try:
    opts, args = getopt.getopt(argv,"hf:o:",["fasta=","output="])
  except getopt.GetoptError:
    print 'cluster_parser.py -f <input fasta> -o <output>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'Outputs a fasta file from that contains the longest representative sequences from a relabeled corset fasta file.'
      print 'cluster_parser.py -f <quoted comma separated input fasta> -o <output>'
      sys.exit()
    elif opt in ("-f", "--fasta"):
      fasta = arg
    elif opt in ("-o", "--output"):
      output = arg
  
  #Trinity and oases regex
  trinity_len = re.compile('len=[0-9]*')
  trinity_name = re.compile('TR[0-9]*\|[a-zA-Z0-9]*_[a-zA-Z0-9]*_[a-zA-Z0-9]*')

  oases_len = re.compile('Length_[0-9]*')
  oases_name = re.compile('Locus_[0-9]*_Transcript_[0-9]*/[0-9]*')

  soap_name = re.compile('[A-Za-z0-9]*')

  cluster = re.compile('Cluster-[0-9]*\.[0-9]*')
  
  #Initialize to none
  #Cluster_name -> (transcript_name, len)
  cluster_prev = ''

  for f in fasta.split(","):
    input_file = open(f,'r')
    line = input_file.readline()
    cluster_dict = {}
    while line:
      if line[0] == '>':
        cluster_name = cluster.search(line)
        if cluster_name:
          cluster_name = cluster_name.group()
          t_len = trinity_len.search(line)
          o_len = oases_len.search(line)
          if t_len:
            length = int(t_len.group()[4:])
            if cluster_name in cluster_dict:
              if cluster_dict[cluster_name][1] < length:
                cluster_dict[cluster_name] = (trinity_name.search(line).group(), length)
            else:
              cluster_dict[cluster_name] = (trinity_name.search(line).group(), length)
          elif o_len:
            length = int(o_len.group()[7:])
            if cluster_name in cluster_dict:
              if cluster_dict[cluster_name][1] < length:
                cluster_dict[cluster_name] = (oases_name.search(line).group(), length)
            else:
              cluster_dict[cluster_name] = (oases_name.search(line).group(), length)
          else:
            soap_name = soap_name.search(line).group()
            #Move next line
            line = input_file.readline()
            length = 0
            #count until next sequence
            while line[0] != '>':
              length += len(line.strip())
              line = input_file.readline()
            if cluster_name in cluster_dict:
              if cluster_dict[cluster_name][1] < length:
                cluster_dict[cluster_name] = (soap_name.search(line).group(), length)
            else:
              cluster_dict[cluster_name] = (soap_name.search(line).group(), length)

            continue
      line = input_file.readline()
  
  input_file.close()
  output_file = open(output,'w')
  for f in fasta.split(","):
    input_file = open(f,'r')
    line = input_file.readline()
    while line:
      if line[0] == '>':
        cluster_name = cluster.search(line)
        if cluster_name:
          cluster_name = cluster_name.group()
          trinity = trinity_name.search(line)
          oases = oases_name.search(line)
          soap = soap_name.search(line)
          trinity = trinity.group() if trinity else None
          oases = oases.group() if oases else None
          soap = soap.group() if soap else None
          if cluster_dict[cluster_name][0] == trinity:
            output_file.write(line)
            line = input_file.readline()
            while line and line[0] != '>':
              output_file.write(line)
              line = input_file.readline()
            else:
              continue
          elif cluster_dict[cluster_name][0] == oases:
            output_file.write(line)
            line = input_file.readline()
            while line and line[0] != '>':
              output_file.write(line)
              line = input_file.readline()
            else:
              continue
          elif cluster_dict[cluster_name][0] == soap:
            output_file.write(line)
            line = input_file.readline()
            while line and line[0] != '>':
              output_file.write(line)
              line = input_file.readline()
            else:
              continue
      line = input_file.readline()
  print "Number of clusters: %d" % len(cluster_dict)
  output_file.close()
  input_file.close()
if __name__ == "__main__":
 main(sys.argv[1:])
