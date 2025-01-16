"""
Structural Connectivity Verification

Author(s):
    -
    -

Parse the JSON netlist file and the CSV connectivity specification and traverse
the netlist to verify that each connection in the CSV is reachable in the RTL
implementation.

Some connections might not be verified because their circuits have
combinational loops. These must be detected and reported as well.
"""

import netlist as nl

import csv
import json
import sys

class CustomVisitor(nl.Visitor): 
	
	def __init__(self, netlist, direction, algorithm): 
		super().__init__(netlist, direction, algorithm)

	def traverse(self, start): 
		print(self.netlist)
	
	def visit(self):
		pass
	
	def visit_gate(self): 
		pass 
 

def main():
    try:
        json_netlist_file = sys.argv[1]
    except IndexError:
        print("Error: missing input JSON netlist file")
        exit(1)

    try:
        csv_spec_file = sys.argv[2]
    except IndexError:
        print("Error: missing input CSV spec file")
        exit(1)

    with open(json_netlist_file) as netlist_file:
        rtl = nl.RTL(json.load(netlist_file))
	
    for netlist in rtl.netlists: 
	    start = netlist.find_net("A[0]")
	    if start: 
		    visitor = CustomVisitor(netlist, nl.Direction.FORWARD, nl.Algorithm.BFS)
		    visitor.traverse(start)
	

if __name__ == "__main__":
    main()
