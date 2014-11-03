# Bioinformatics scripts

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
