#! /usr/bin/env python3

# @author: Télécom Paris

import sys
import re
import io

from vcd import VCDWriter
from vcd.gtkw import GTKWSave


# Class to encapsulate signal attributes
class Signal:
    def __init__(self, name, sigtype, size=0, options=None, labels=None, flags=None):
        self.name = name
        self.sigtype = sigtype
        self.size = size
        if options:
            self.options = options
        else:
            self.options = dict()
        self.labels = labels
        if flags:
            self.flags = flags
        else:
            self.flags = list()

    def getOption(self, opt):
        try:
            return self.options[opt]
        except KeyError:
            return None

    def setOption(self, opt, val):
        self.options[opt] = val

    def addFlag(self, flag):
        self.flags.append(flag)


def usage():
    sys.stderr.write('usage: logisim2vcd.py <output.vcd> [-spec file] [signame sigtype]+\n')
    sys.stderr.write('binary/integer sigtype: <size>\n')
    sys.stderr.write('enum/labeled sigtype  : <size>{label_0,label_1,...}\n')
    sys.stderr.write('sigtype with options  : <size>[option=value,flag,...]\n')
    sys.stderr.write('simulation data is expected on standard input')

# A list of all signals specified on the command line
signals = list()

# Parse command line. We are expecting the name of the output file, followed by
# pairs of signal name and signal specification (size or labels)
if len(sys.argv) < 2:
    sys.stderr.write('ERROR: please provide the project name or vcd output file as first argument\n')
    usage()
    exit(1)

# Output file name(s)    
vcdFileName = sys.argv[1]
if not vcdFileName.endswith('vcd'):
    gtkwFileName = vcdFileName + '.gtkw'
    vcdFileName += '.vcd'
else:
    gtkwFileName = vcdFileName[:-4] + '.gtkw'

# Check if specification simulation data is provided
args = sys.argv[2:]
specFile = None
if len(args) > 1 and args[0] == '-spec':
    specFile = args[1]
    args = args[2:]

# Parse signal specifications
name = None
sigspec = re.compile(r'(\d+)(\{.+\})?(\[.+\])?')
for arg in args:
    if name:

        # Parse signal specification
        if arg.isdigit():

            # Binary signal with only its size given
            sig = Signal(name, sigtype='integer', size=int(arg))
            signals.append(sig)
        else:

            # Signal spec with labels and/or options
            m = sigspec.match(arg)
            if not m:
                sys.stderr.write("ERROR: invalid signal specification: '{}'\n".format(arg))
                exit(1)

            # signal type: integer or string (with labels)
            size = int(m.group(1))
            if m.group(2):
                sigtype = 'string'
                labels = m.group(2)[1:-1].split(',')
            else:
                sigtype = 'integer'
                labels = None
            sig = Signal(name, sigtype=sigtype, size=size, labels=labels)

            # miscellaneous options (key value pairs or boolean options)
            if m.group(3):
                opts = m.group(3)[1:-1].split(',')
                for opt in opts:
                    pair = opt.split('=')
                    if len(pair) == 2:
                        sig.setOption(pair[0], pair[1])
                    elif len(pair) == 1:
                        sig.addFlag(pair[0])
                    else:
                        sys.stderr.write("ERROR: invalid option in signal specification: '{}'\n".format(arg))
                        exit(1)
            signals.append(sig)
        name = None
    else:
        name = arg

# Remove white space from simulation data
def compact(lines):
    values = []
    for line in lines:
        bits = ''.join(filter(lambda c:not c in [' ','\t'], line.strip()))
        values.append(bits)
    return values


# Read simulation data, remove white space
lines = sys.stdin.readlines()
values = compact(lines)
specValues = None
if specFile:
    with open(specFile) as f:
        lines = f.readlines()
    specValues = compact(lines)


# Function to create signal, value pairs from the raw logisim output
def extract(bits):
    values = []
    pos = 0
    for sig in signals:
        l = sig.size
        try:
            v = int(bits[pos:pos+l], base=2)
        except ValueError:
            v = bits[pos:pos+l]
        values.append( (sig, v) )
        pos += l
    return values


# Output VCD dump file
with open(vcdFileName, 'w') as f:
    with VCDWriter(f, timescale='1 ns', date='today') as writer:

        # Create VCD variables
        vcdVars = dict()
        specVars = dict()
        for sig in signals:
            vcdVars[sig.name] = writer.register_var('circ', sig.name, sig.sigtype, size=sig.size)
            if specValues:
                specVars[sig.name] = writer.register_var('spec', sig.name, sig.sigtype, size=sig.size)

        def dump(t, sig, x, varDict):
            if sig.sigtype == 'string':
                try:
                    label = sig.labels[x]
                except TypeError:
                    
                    # Tried to find label with unknown input ('X')
                    label = "X"
                except IndexError:
                    sys.stderr.write('IndexError in labels of signal {}: value {} is out of bounds\n'.format(sig.name, x))
                    exit(1)
                writer.change(varDict[sig.name], t, label)
            else:
                if type(x) is str:
                    
                    # vcd doesn't like 'E' (error), so replace it with 'X' (unknown)
                    x = x.replace('E', 'X')
                writer.change(varDict[sig.name], t, x)

        # Dump simulation data
        if not specValues:
            t = 0
            for bits in values:
                for sig, x in extract(bits):
                    dump(t, sig, x, vcdVars)
                t += 1
        else:
            t = 0
            for bits, specbits in zip(values, specValues):
                for sig, x in extract(bits):
                    dump(t, sig, x, vcdVars)
                for sig, x in extract(specbits):
                    dump(t, sig, x, specVars)
                t += 1


# Output GTK Wave save file (for nicely coloured and formatted signals)
with open(gtkwFileName, 'w') as f:
    gtkw = GTKWSave(f)
    gtkw.dumpfile(vcdFileName)
    gtkw.zoom_markers(-2.0)

    def trace(sig, prefix='circ.', defaultColor='normal'):
        color = sig.getOption('color')
        if not color:
            color = defaultColor
        datafmt = sig.getOption('datafmt')
        if not datafmt:
            if sig.size > 1:
                datafmt = 'dec'
            else:
                datafmt = 'bin'
        gtkw.trace(prefix + sig.name, color=color, datafmt=datafmt, extraflags=sig.flags)

    if specValues:
        gtkw.begin_group('Implementation')
    for sig in signals:
        trace(sig)
    if specValues:
        gtkw.end_group('Implementation')
        gtkw.begin_group('Specification')
        for sig in signals:
            trace(sig, prefix='spec.', defaultColor='yellow')
        gtkw.end_group('Specification')

sys.stderr.write('Wrote vcd trace to file {}\n'.format(vcdFileName))
sys.stderr.write('Wrote GTKwave config file {}\n'.format(gtkwFileName))

                 
