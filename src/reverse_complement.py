from script_utils import *
from transformers import ReverseComplement


mode = args['mode']
if mode == 'reverse' or mode == 'complement' or mode == 'both':
    transformed_sequences = ReverseComplement(style=mode).transform
else:
    args.pop('mode')
    errorMode(args, sys.argv[0])
    
script_args = arguments()
apply_transformation(script_args[0], script_args[1], transformed_sequences)


