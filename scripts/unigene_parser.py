#!/usr/bin/python

#######################################
# Outputs a fasta file from that      #
# contains the longest representative # 
# sequences from a assembly file      #
# Created by John Erol M. Evangelista #
#######################################


import sys, getopt, re

def main(argv):
  fasta = ''
  cluster = ''
  output = ''
  software = ''
  try:
    opts, args = getopt.getopt(argv,"hf:s:o:",["fasta=","output="])
  except getopt.GetoptError:
    print 'unigene_parser.py -f <input fasta> -s <software> -o <output>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'Outputs a fasta file from that contains the longest representative sequences from a relabeled corset fasta file.'
      print 'unigene_parser.py -f <input fasta> -s <software> -o <output>'
      print '-s: t: trinity s: soap o: oases'
      sys.exit()
    elif opt in ("-f", "--fasta"):
      fasta = arg
    elif opt in ("-s", "--software"):
      software = arg #TODO: Add checking
    elif opt in ("-o", "--output"):
      output = arg
  
  #Trinity and oases regex
  trinity_len = re.compile('len=[0-9]*')
  trinity_name = re.compile('TR[0-9]*\|[a-zA-Z0-9]*_[a-zA-Z0-9]*_[a-zA-Z0-9]*')

  oases_len = re.compile('Length_[0-9]*')
  oases_name = re.compile('Locus_[0-9]*_Transcript_[0-9]*/[0-9]*')

  soap_name = re.compile('[A-Za-z0-9]*')

  trinity_cluster = re.compile('TR[0-9]*\|[a-zA-Z0-9]*_[a-zA-Z0-9]*')
  oases_cluster = re.compile('Locus_[0-9]*')
  soap_cluster = re.compile('Locus_[0-9]*|C[0-9]+')
  
  #Initialize to none
  #Cluster_name -> (transcript_name, len)
  cluster_prev = ''

  input_file = open(fasta,'r')
  line = input_file.readline()
  cluster_dict = {}
  while line:
    if line[0] == '>':
      if software == 't':
        t_cluster = trinity_cluster.search(line)
        if t_cluster:
          t_cluster = t_cluster.group()
          t_len = trinity_len.search(line)
          if t_len:
            length = int(t_len.group()[4:])
            if t_cluster in cluster_dict:
              if cluster_dict[t_cluster][1] < length:
                cluster_dict[t_cluster] = (trinity_name.search(line).group(), length)
            else:
              cluster_dict[t_cluster] = (trinity_name.search(line).group(), length)
      elif software == 'o':
        o_cluster = oases_cluster.search(line)
        if o_cluster:
          o_cluster = o_cluster.group()
          o_len = oases_len.search(line)
          if o_len:
            length = int(o_len.group()[4:])
            if o_cluster in cluster_dict:
              if cluster_dict[o_cluster][1] < length:
                cluster_dict[o_cluster] = (oases_name.search(line).group(), length)
            else:
              cluster_dict[o_cluster] = (oases_name.search(line).group(), length)
      elif software == 's':
        #TODO: Don't count lenght of C[0-9]* headers.
        s_cluster = soap_cluster.search(line)
        if s_cluster:
          s_cluster = s_cluster.group()
          #Move next line
          line = input_file.readline()
          length = 0
          #count until next sequence
          while line[0] != '>':
            length += len(line.strip())
            line = input_file.readline()
          if s_cluster in cluster_dict:
            if cluster_dict[s_cluster][1] < length:
              cluster_dict[s_cluster] = (soap_name.search(line).group(), length)
          else:
            cluster_dict[s_cluster] = (soap_name.search(line).group(), length)
          continue
    line = input_file.readline()
  
  input_file.close()
  output_file = open(output,'w')
  input_file = open(fasta,'r')
  line = input_file.readline()
  while line:
    if line[0] == '>':
      if software == 't':
        t_cluster = trinity_cluster.search(line)
        trinity = trinity_name.search(line)
        if t_cluster:
          t_cluster = t_cluster.group()
          trinity = trinity.group() if trinity else None
          if cluster_dict[t_cluster][0] == trinity:
            output_file.write(line)
            line = input_file.readline()
            while line and line[0] != '>':
              output_file.write(line)
              line = input_file.readline()
            else:
              continue
      elif software == 'o':
        o_cluster = oases_cluster.search(line)
        oases = oases_name.search(line)
        if o_cluster:
          o_cluster = o_cluster.group()
          oases = oases.group() if oases else None
          if cluster_dict[o_cluster][0] == oases:
            output_file.write(line)
            line = input_file.readline()
            while line and line[0] != '>':
              output_file.write(line)
              line = input_file.readline()
            else:
              continue
        elif software == 's':
          s_cluster = soap_cluster.search(line)
          soap = soap_name.search(line)
          if s_cluster:
            s_cluster = s_cluster.group()
            soap = soap.group() if soap else None
            if cluster_dict[s_cluster][0] == soap:
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
