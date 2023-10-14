"""This module contains the functions that are used by the scripts"""

from fasta import SeqFileManager, error_generic, error_length
from script_utils import sys, args, arguments


script_args = arguments()
error_generic(args, sys.argv[0])
caseFile = args.get('case', 'original')
maxLengthFile = int(args.get('maxLength', 0))
# Error if maxLength < 0
error_length(maxLengthFile)

load = SeqFileManager().load_fasta(script_args[0])
SeqFileManager(SeqFileManager.parse_case(caseFile), maxLengthFile).write_fasta(load, script_args[1])
