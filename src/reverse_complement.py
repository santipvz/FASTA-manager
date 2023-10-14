# pylint: disable=duplicate-code
"""Reverse complement sequences in a FASTA file."""
from script_utils import sys, args, arguments, apply_transformation, error_mode
from transformers import ReverseComplement


mode = args['mode']
if mode == 'reverse' or mode == 'complement' or mode == 'both':
    transformed_sequences = ReverseComplement(style=mode).transform
else:
    args.pop('mode')
    error_mode(args, sys.argv[0])

script_args = arguments()
apply_transformation(script_args[0], script_args[1], transformed_sequences)
