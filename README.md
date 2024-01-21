# FASTA manager

The FASTA Manager is a versatile command-line tool designed to assist in the management and analysis of DNA or protein sequences stored in FASTA format. This tool provides functionalities for formatting, transforming, and generating statistics or plots from sequence data.


# Installation
You can install this program using pip with: **<pre><code>pip install fasta-manager</pre></code>**
# Command Line Arguments
--`dremove`: Remove duplicate sequences.

--`drename`: Rename duplicate sequences.

--`reverse`: Reverse sequences.

--`complement`: Complement sequences.

--`rc`: Reverse complement sequences.

--`stats`: Compute statistics.

--`casefile`: Case transformation (original, upper, lower).

--`plots`: Generate plots.

# Examples
Example 1: Remove duplicates and generate statistics
<pre><code>fasta --dremove --stats</pre></code>

Example 2: Reverse complement sequences and generate plots
<pre><code>fasta --rc --plots</pre></code>

Example 3: Perform case transformation
<pre><code>fasta --casefile upper</pre></code>

You can also combine parameters where order doesn't matter.
<pre><code>fasta --stats --plots --casefile lower --drename</pre></code>

# Results
The processed sequences will be stored in the `results` directory, and statistics (if computed) will be saved in the `stats` directory. Plots (if generated) will be saved in the `plots` directory

# Input File Format
The input files are expected to follow the format:

<pre><code>>ID
Sequence</pre></code>

## Example
`test_1.fasta`
<pre><code>>S1
actgACTG
>S2
ctgaCTGA
>S3
gggaGGGA
</pre></code>