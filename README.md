# Bioinformatics scripts

Mostly for transcriptomics.

## How to use
Add the following to your ~/.bashrc file (~/.zshrc file for Bio-Linux)
```
export PATH=~/path/to/scripts:$PATH
```

## Documentation
**blast_parser.py**

Returns a fasta file that contains the sequences that (0) have Blast hits (1) have no Blast hits.
```
blast_parser.py -i <input fasta> -x <blast xml> -c <0 (query hits), 1 (query nonhits)> -o <output>
```

**fasta_parser.py**

Outputs a fasta file from that contains the sequences specified in the tag file.
```
fasta_parser.py -i <input fasta> -t <tags> -s <separator> -o <output>
```

**fasta_summarizer.py**

Gets the longest, shortest, mean length and N50 for Trinity assembly.
```
fasta_summarizer.py -f <input fasta> -o <output>
```

**oases_unigene_parser.py**

Gets unigenes by getting the locus with (1) Greatest confidence score and in case of a tie (2) longest of the tie.
```
oases_unigene_parser.py -f <input fasta> -o <output>
```

**trinity_longest_parser.py**

Gets unigenes by getting the longest gene in the cluster.
```
trinity_longest_parser.py -f <input fasta> -o <output>
```

**WEGO_formatter.py**

Formats a GO file to WEGO's native format.

```
WEGO_formatter.py -i <GO file> -o <output>
```
