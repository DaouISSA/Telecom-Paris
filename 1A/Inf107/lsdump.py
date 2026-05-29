#! /usr/bin/env python3

from argparse import ArgumentParser

import sys

parser = ArgumentParser(
        prog = 'lsdump',
        description = 'transform objdump output to logisim memory contents'
    )

parser.add_argument('-v', '--version', default='2', 
                    help='Set version of logisim output file (2 or 3)')
parser.add_argument('-o', '--output', default=None,
                    help='output file name (defaults to stdout)')
parser.add_argument('infile', 
                    help='input file name')

args = parser.parse_args()
   
out = None
if args.output:
    out = open(args.output, 'w')
else:
    out = sys.stdout
    
with open(sys.argv[1], 'r') as infile:
    lines = infile.readlines()[1:]
    if args.version == '3':
        out.write('v3.0 hex bytes addressed big-endian\n')
    else:
        out.write('v2.0 raw\n')
    for line in lines:
        bytes = line.strip().split(' ')
        addr = 0
        i = 0
        instr = ''
        for byte in bytes:
            instr = byte + instr
            if i == 3:
                if args.version == '3':
                    out.write('{:04X}: {}\n'.format(addr, instr))
                else:
                    out.write('{}\n'.format(instr))
                i = 0
                instr = ''
                addr += 4
            else:
                i += 1
    
if args.output:
    sys.stderr.write("Wrote memory file '{}'\n".format(args.output))
