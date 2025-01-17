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

import re
import csv
import json
import sys

class CustomVisitor(nl.Visitor): 
    
	
    def __init__(self, netlist, direction, algorithm):
        super().__init__(netlist, direction, algorithm)
        self.visited = set()
        self.has_combinational_loops = False
         
    def visit(self, net):
        
        if net in self.visited: 
            return False
        
        self.visited.add(net)
        # print("visit: {}".format(net))
        return True
    
            
    def visit_gate(self, gate): 
        
        if gate in self.visited: 
            self.has_combinational_loops = True
            return list()
        
        self.visited.add(gate)
        # print("visit_gate: {}".format(gate))
        return self.get_next_nodes(gate)
 

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
    
        with open(csv_spec_file, "r") as csv_file: 
            csv_reader = csv.reader(csv_file)
            
            for row in csv_reader: 
                if row[0].startswith('#'):  # Skip comment lines
                    continue
                
                source_signal = row[3] + '[0]'
                destination_signal = row[5] + '[0]'
                source_signal = re.sub(r"[~!]", "", source_signal)
                destination_signal = re.sub(r"[~!]", "", destination_signal)
                
                for netlist in rtl.netlists: 
                    
                    # Checking structural connectivity
                    visitor = CustomVisitor(netlist, nl.Direction.BIDIRECTIONAL, nl.Algorithm.BFS)
                    start = netlist.find_net(source_signal)
                    end = netlist.find_net(destination_signal)
                    result = ""
                    if start: 
                        visitor.traverse(start)
                    
                    if end in visitor.visited: 
                        result = "connected"
                    else:
                        result = "unconnected"
                    
                    # Detecting combinational loops
                    visitor = CustomVisitor(netlist, nl.Direction.FORWARD, nl.Algorithm.DFS)
                    if start: 
                        visitor.traverse(start)
                    
                    if visitor.has_combinational_loops: 
                        result = "combinational_loop"
                
                print(row[1] + " " + row[3] + " " + row[5] + " " + result)    
        
   
if __name__ == "__main__":
    main()
