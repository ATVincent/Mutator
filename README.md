# Mutator
## What is Mutator ?
Mutator is a tool composed of several scripts allowing to detect, using genomic data, amino acid changes within a subpopulation.

The DIAMOND tool is required and must be installed on the system (https://github.com/bbuchfink/diamond).
## How to use Mutator?
### 1. Mapping reads to primary protein sequences

The first step is to map the sequencing reads on the primary protein sequences with the diamond tool (blastx algorithm). It is recommended to concatenate the files containing the R1 and R2 reads (CONCAT.fastq file in our case).


```sh
diamond blastx --query CONCAT.fastq --db Database/DB.dmnd -f 6 qseqid sseqid slen sstart send evalue pident qcovhsp btop bitscore -k 0 -e 1e-10 -c 1 -p 14 --out Result.diamond
```
Obviously you have to adapt the command line (eg the number of threads) for your needs. DIAMOND documentation is available here:
https://github.com/bbuchfink/diamond

### 2. Filtering DIAMOND results
The second step is to filter the results of DIAMOND to keep only the reads mapping on only one sequence (and thus remove the paralogs). This step also allows to keep the alignment that corresponds to the best-hit (according to the bitscore).

```sh
python Sort_diamond.py -I Result.diamond > Result_sorted.diamond
```
### 3. Detection of amino acid changes

The third step is the one that identifies the amino acid changes present in the subpopulation.

```sh
python Mutator.py -I Proteins.faa -D Result_sorted.diamond > Result_mutator.tsv
```
Please note that it is important to give, in addition to the file sorted by Sort_diamond.py, the file with the protein sequences that have been used to map the reads with DIAMOND.

### 4. Rearrange Mutator result (optional)
The last step is optional and makes it easier to read Mutator's results.
```sh
python Compile_Mutations.py -I Result_mutator.tsv > Result_mutator_compiled.tsv
```
## License
Mutator Copyright (C) 2023 Antony T. Vincent. This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.