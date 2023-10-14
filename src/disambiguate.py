# pylint: disable=duplicate-code
"""Disambiguate duplicated identifiers in a FASTA file."""
from script_utils import sys, args, arguments, apply_transformation, error_mode
from transformers import DuplicatedIdentifiersRemover, DuplicatedIdentifiersRenamer


mode = args['mode']
if mode == 'rename':
    transformed_sequences = DuplicatedIdentifiersRenamer().transform
elif mode == 'remove':
    transformed_sequences = DuplicatedIdentifiersRemover().transform
else:
    args.pop('mode')
    error_mode(args, sys.argv[0])

script_args = arguments()
apply_transformation(script_args[0], script_args[1], transformed_sequences)
