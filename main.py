#!/usr/bin/python3

from Circuit import  Circuit
import simplejson as json
import argparse

def main():
    args = parse_option()
    circuit = load_json(args.infile)

    if args.verbose:
        print(circuit)

    if args.disp:
        circuit.disp(size=50, scale=0.6)

    circuit.save(50, .6, args.outfile)

def parse_option():
    usage = "qcdraw infile outfile [--disp] [--verbose] [--help]"
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('infile', type=str, help='file name of input')
    parser.add_argument('outfile', type=str, help='file name of output')
    parser.add_argument('-d', '--disp', action='store_true', help='display the circuit')
    parser.add_argument('-v', '--verbose', action='store_true', help='show verbose message')
    args = parser.parse_args()
    return args

def load_json(file_name):
    circuit = Circuit()
    with open(file_name) as file:
        data = json.load(file)
        for gate in data['gates']:
            type = gate['type']
            x = gate.get('x')
            fill_color = gate.get('fill_color', 'w')
            edge_color = gate.get('edge_color', 'k')
            if not type == "PC":
                control = gate.get('control')
                target = gate['target']
                circuit.add_gate(type, control, target, x, fill_color, edge_color)
            else:
                measurement = gate['measurement']
                correction = gate['correction']
                circuit.add_correction(measurement, correction, x, fill_color, edge_color)

    return circuit

if __name__ == '__main__':
    main()