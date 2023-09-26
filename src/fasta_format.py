from fasta import SeqFileManager, errorGeneric
from script_utils import *


script_args = arguments()
errorGeneric(args, sys.argv[0])
caseFile = args.get('case', 'original')
maxLengthFile = int(args.get('maxLength', 0))
# Error if maxLength < 0
errorLength(maxLengthFile) 

load = SeqFileManager.loadFasta(script_args[0])
SeqFileManager(SeqFileManager.parseCase(caseFile), maxLengthFile).writeFasta(load, script_args[1])

