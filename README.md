# FASTA manager

The objective of this project is the creation of an application for managing files in FASTA format, a text format used in bioinformatics to represent DNA or protein sequences. A FASTA file stores information for one or more sequences. Each sequence is composed of a header line beginning with the ">" character and one or more lines containing text with the corresponding DNA or protein sequence. The header provides the sequence identifier. Let's look at an example of content in FASTA format:

## Examples
 \> S1
 
 ACTG

In this case, the file contains a single sequence whose identifier is 'S1' and the DNA sequence is 'ACTG'. As mentioned above, a file can have several sequences and, at the same time, each sequence can have its content distributed over several lines. Let's look at another example:

\> S1

ACTGAT

\> S2

AACCGC

In this case, the file contains two sequences with identifiers 'S1' and 'S2', and the DNA sequences are 'ACTGAT' and 'AACCGC' respectively (as you can see, the lines following the header are joined together into a single string which represents the complete sequence). 

# Some usage commands
Change file name or format
<pre><code>python fasta_format.py --input=test_1.fasta --output=test1.fasta --case=lower --maxLength=2</pre></code>

Rename chains with the same ID
<pre><code>python disambiguate.py --input=test_3.fasta --output=test2.fasta --mode=rename</pre></code>

Delete chains with the same ID
<pre><code>python disambiguate.py --input=test_3.fasta --output=test2_1.fasta --mode=remove</pre></code>

Get a reversed and complemented chain
<pre><code>python reverse_complement.py --input=test_3.fasta --output=test3.fasta --mode=both</pre></code>

Get the complementary chain of a given one
<pre><code>python reverse_complement.py --input=test_4.fasta --output=test4.fasta --mode=complement</pre></code> 

Get the reversed chain of a given one
<pre><code>python reverse_complement.py --input=test_4.fasta --output=test4.fasta --mode=reverse</pre></code>

Get data from a file in csv format (Amount of A,C,T,G...) with the option to show plots of this data (--extra-plots-dir is an optional argument)
<pre><code>python fasta_summary.py --input=INPUT --output=CSV_OUTPUT --extra-plots-dir=GRAPHS_OUTPUT</pre></code>
