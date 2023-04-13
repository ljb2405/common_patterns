import pickle
import networkx as nx
import typing as tp
from itertools import count, combinations
import pulp

from .utils import *
import subgraph_merging_freq.config as config
from .subgraph import Subgraph, DSESubgraph
from .plot_utils import *
import subgraph_merging_freq.utils as utils
from .merger import *

def gen_verilog(self):
    input_list = []
    output_list = []
    inout_node_list = []
    dff_node_list = []
    dffp_list = []
    dffn_list = []
    print(self.merged_graph.subgraph.adj)
    f = open("outputs/spec_module.v", 'w')

    # Write intro parts
    f.write("module spec_module (\n")
    f.write("\tinput wire clk,\n")
    f.write("\tinput wire rst,\n")

    for n in self.merged_graph.subgraph.nodes:
        if self.merged_graph.subgraph.nodes[n]['op'] == "input" or self.merged_graph.subgraph.nodes[n]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[n]['op'] == "const_input":
            input_list.append("\tinput wire in" + str(n) + ",\n")
            inout_node_list.append(n)
        elif self.merged_graph.subgraph.nodes[n]['op'] == "output" or self.merged_graph.subgraph.nodes[n]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[n]['op'] == "const_output":
            output_list.append("\toutput wire out" + str(n) + ",\n")
            inout_node_list.append(n)
        elif config.op_types[self.merged_graph.subgraph.nodes[n]['op']] in config.dffs:
            dff_node_list.append(n)
            
    
    for i in input_list:
        f.write(i)
    output_list[-1] = output_list[-1][:-2] + '\n'
    for o in output_list:
        f.write(o)

    f.write("\t);\n")
    f.write("\n")

    # Write the circuit
    for n in self.merged_graph.subgraph.nodes:
        op_num = self.merged_graph.subgraph.nodes[n]['op']
        op = config.op_types[op_num]
        if n not in inout_node_list and op != "dff" and op != "sdff" and op != "sdffe":
            f.write("\twire wire" + str(n) + ";\n")

    f.write("\n")
    for n in self.merged_graph.subgraph.nodes:
        op_num = self.merged_graph.subgraph.nodes[n]['op']
        op = config.op_types[op_num]
        # DFFs
        if op == "dff":
            f.write("\treg " + "[" + str(self.merged_graph.subgraph.in_degree(n)-1) + ":0]" + " dff" + str(n) + ";\n")
            for ind, d in enumerate(self.merged_graph.subgraph.predecessors(n)):
                dffp_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= wire" + str(d) + ";\n")
        elif op == "sdffe":
            f.write("\treg " + "[" + str(self.merged_graph.subgraph.in_degree(n)-1) + ":0]" + " dff" + str(n) + ";\n")
            for ind, d in enumerate(self.merged_graph.subgraph.predecessors(n)):
                dffp_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= wire" + str(d) + ";\n")
        elif op == "sdff":
            f.write("\treg " + "[" + str(self.merged_graph.subgraph.in_degree(n)-1) + ":0]" + " dff" + str(n) + ";\n")
            for ind, d in enumerate(self.merged_graph.subgraph.predecessors(n)):
                dffp_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= wire" + str(d) + ";\n")
        elif op == "_SDFF_PP0_":
            f.write("\treg " + "[" + str(self.merged_graph.subgraph.in_degree(n)-1) + ":0]" + " dff" + str(n) + ";\n")
            for ind, d in enumerate(self.merged_graph.subgraph.predecessors(n)):
                if d not in inout_node_list:
                    dffp_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= wire" + str(d) + ";\n")
                elif self.merged_graph.subgraph.nodes[d]['op'] == "input" or self.merged_graph.subgraph.nodes[d]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[d]['op'] == "const_input":
                    dffp_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= in" + str(d) + ";\n")
                elif self.merged_graph.subgraph.nodes[d]['op'] == "output" or self.merged_graph.subgraph.nodes[d]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[d]['op'] == "const_output":
                    dffp_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= out" + str(d) + ";\n")
        elif op == "_SDFFE_PP0P_" or op == "_DFFE_PP_" or op == "_DFF_P_" or op == "_SDFFCE_PP0P_" or op == "_SDFF_PP0_" or op == "_SDFF_PP1_" or op == "_DFFE_PP_":
            f.write("\treg " + "[" + str(self.merged_graph.subgraph.in_degree(n)-1) + ":0]" + " dff" + str(n) + ";\n")
            for ind, d in enumerate(self.merged_graph.subgraph.predecessors(n)):
                if d not in inout_node_list:
                    dffp_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= wire" + str(d) + ";\n")
                elif self.merged_graph.subgraph.nodes[d]['op'] == "input" or self.merged_graph.subgraph.nodes[d]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[d]['op'] == "const_input":
                    dffp_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= in" + str(d) + ";\n")
                elif self.merged_graph.subgraph.nodes[d]['op'] == "output" or self.merged_graph.subgraph.nodes[d]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[d]['op'] == "const_output":
                    dffp_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= out" + str(d) + ";\n")
        elif op == "re" or op == "al":
            f.write("\treg " + "[" + str(self.merged_graph.subgraph.in_degree(n)-1) + ":0]" + " dff" + str(n) + ";\n")
            for ind, d in enumerate(self.merged_graph.subgraph.predecessors(n)):
                if d not in inout_node_list:
                    dffp_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= wire" + str(d) + ";\n")
                elif self.merged_graph.subgraph.nodes[d]['op'] == "input" or self.merged_graph.subgraph.nodes[d]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[d]['op'] == "const_input":
                    dffp_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= in" + str(d) + ";\n")
                elif self.merged_graph.subgraph.nodes[d]['op'] == "output" or self.merged_graph.subgraph.nodes[d]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[d]['op'] == "const_output":
                    dffp_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= out" + str(d) + ";\n")
        elif op == "_SDFFE_PP0N_" or op == "_SDFFCE_PN0P_" or op == "_SDFFCE_PN1P_" or op == "_DLATCH_N_" or op == "_SDFF_PN1_" or op == "_DFFE_PN_" or op == "_DFFE_PN0_" or "_SDFFCE_PP0N_":
            f.write("\treg " + "[" + str(self.merged_graph.subgraph.in_degree(n)-1) + ":0]" + " dff" + str(n) + ";\n")
            for ind, d in enumerate(self.merged_graph.subgraph.predecessors(n)):
                if d not in inout_node_list:
                    dffn_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= wire" + str(d) + ";\n")
                elif self.merged_graph.subgraph.nodes[d]['op'] == "input" or self.merged_graph.subgraph.nodes[d]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[d]['op'] == "const_input":
                    dffn_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= in" + str(d) + ";\n")
                elif self.merged_graph.subgraph.nodes[d]['op'] == "output" or self.merged_graph.subgraph.nodes[d]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[d]['op'] == "const_output":
                    dffn_list.append("\t\tdff" + str(n) + "[" + str(ind) + "]" + " <= out" + str(d) + ";\n")
        
        # Primitives
        elif op == "not":
            s = self.merged_graph.subgraph.adj[n]
            for a, _ in s.items():
                f.write("\tnot not" + str(n) + " ")
                if a not in inout_node_list:
                    f.write("(wire" + str(a))
                elif a in dff_node_list:
                    f.write("(dff" + str(a))
                elif self.merged_graph.subgraph.nodes[a]['op'] == "input" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[a]['op'] == "const_input":
                    f.write("(in" + str(a))
                elif self.merged_graph.subgraph.nodes[a]['op'] == "output" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[a]['op'] == "const_output":
                    f.write("(out" + str(a))
                for p in self.merged_graph.subgraph.predecessors(n):
                    if p not in inout_node_list:
                        f.write(", wire" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "input" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[p]['op'] == "const_input":
                        f.write(", in" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "output" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[p]['op'] == "const_output":
                        f.write(", out" + p)
                f.write(");\n")
        elif op == "nand":
            s = self.merged_graph.subgraph.adj[n]
            for a, _ in s.items():
                f.write("\tnand nand" + str(n) + " ")
                if a not in inout_node_list:
                    f.write("(wire" + str(a))
                elif a in dff_node_list:
                    f.write("(dff" + str(a))
                elif self.merged_graph.subgraph.nodes[a]['op'] == "input" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[a]['op'] == "const_input":
                    f.write("(in" + str(a))
                elif self.merged_graph.subgraph.nodes[a]['op'] == "output" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[a]['op'] == "const_output":
                    f.write("(out" + str(a))
                for p in self.merged_graph.subgraph.predecessors(n):
                    if p not in inout_node_list:
                        f.write(", wire" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "input" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[p]['op'] == "const_input":
                        f.write(", in" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "output" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[p]['op'] == "const_output":
                        f.write(", out" + p)
                f.write(");\n")
        elif op == "nor":
            s = self.merged_graph.subgraph.adj[n]
            for a, _ in s.items():
                f.write("\tnor nor" + str(n) + " ")
                if a not in inout_node_list:
                    f.write("(wire" + str(a))
                elif a in dff_node_list:
                    f.write("(dff" + str(a))
                elif self.merged_graph.subgraph.nodes[a]['op'] == "input" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[a]['op'] == "const_input":
                    f.write("(in" + str(a))
                elif self.merged_graph.subgraph.nodes[a]['op'] == "output" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[a]['op'] == "const_output":
                    f.write("(out" + str(a))
                for p in self.merged_graph.subgraph.predecessors(n):
                    if p not in inout_node_list:
                        f.write(", wire" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "input" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[p]['op'] == "const_input":
                        f.write(", in" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "output" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[p]['op'] == "const_output":
                        f.write(", out" + p)
                f.write(");\n")
        elif op == "or":
            s = self.merged_graph.subgraph.adj[n]
            for a, _ in s.items():
                f.write("\tor or" + str(n) + " ")
                if a not in inout_node_list:
                    f.write("(wire" + str(a))
                elif a in dff_node_list:
                    f.write("(dff" + str(a))
                elif self.merged_graph.subgraph.nodes[a]['op'] == "input" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[a]['op'] == "const_input":
                    f.write("(in" + str(a))
                elif self.merged_graph.subgraph.nodes[a]['op'] == "output" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[a]['op'] == "const_output":
                    f.write("(out" + str(a))
                for p in self.merged_graph.subgraph.predecessors(n):
                    if p not in inout_node_list:
                        f.write(", wire" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "input" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[p]['op'] == "const_input":
                        f.write(", in" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "output" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[p]['op'] == "const_output":
                        f.write(", out" + p)
                f.write(");\n")
        elif op == "and":
            s = self.merged_graph.subgraph.adj[n]
            for a, _ in s.items():
                f.write("\tand and" + str(n) + " ")
                if a not in inout_node_list:
                    f.write("(wire" + str(a))
                elif a in dff_node_list:
                    f.write("(dff" + str(a))
                elif self.merged_graph.subgraph.nodes[a]['op'] == "input" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[a]['op'] == "const_input":
                    f.write("(in" + str(a))
                elif self.merged_graph.subgraph.nodes[a]['op'] == "output" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[a]['op'] == "const_output":
                    f.write("(out" + str(a))
                for p in self.merged_graph.subgraph.predecessors(n):
                    if p not in inout_node_list:
                        f.write(", wire" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "input" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[p]['op'] == "const_input":
                        f.write(", in" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "output" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[p]['op'] == "const_output":
                        f.write(", out" + p)
                f.write(");\n")
        elif op == "xor":
            s = self.merged_graph.subgraph.adj[n]
            for a, _ in s.items():
                f.write("\txor xor" + str(n) + " ")
                if a not in inout_node_list:
                    f.write("(wire" + str(a))
                elif a in dff_node_list:
                    f.write("(dff" + str(a))
                elif self.merged_graph.subgraph.nodes[a]['op'] == "input" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[a]['op'] == "const_input":
                    f.write("(in" + str(a))
                elif self.merged_graph.subgraph.nodes[a]['op'] == "output" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[a]['op'] == "const_output":
                    f.write("(out" + str(a))
                for p in self.merged_graph.subgraph.predecessors(n):
                    if p not in inout_node_list:
                        f.write(", wire" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "input" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[p]['op'] == "const_input":
                        f.write(", in" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "output" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[p]['op'] == "const_output":
                        f.write(", out" + p)
                f.write(");\n")
        # Mux - FIX
        elif op == "mux":
            s = self.merged_graph.subgraph.adj[n]
            for a, _ in s.items():
                f.write("\tmux assign")
                if a not in inout_node_list:
                    f.write("(wire" + str(a))
                elif a in dff_node_list:
                    f.write("(dff" + str(a))
                elif self.merged_graph.subgraph.nodes[a]['op'] == "input" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[a]['op'] == "const_input":
                    f.write("(in" + str(a))
                elif self.merged_graph.subgraph.nodes[a]['op'] == "output" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[a]['op'] == "const_output":
                    f.write("(out" + str(a))
                for p in self.merged_graph.subgraph.predecessors(n):
                    if p not in inout_node_list:
                        f.write(", wire" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "input" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[p]['op'] == "const_input":
                        f.write(", in" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "output" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[p]['op'] == "const_output":
                        f.write(", out" + p)
                f.write(");\n")
        # Comparators
        elif op == "gt":
            s = self.merged_graph.subgraph.adj[n]
            for a,_ in s.items():
                f.write("\tgt assign")
                if s not in inout_node_list:
                    f.write(" wire" + str(a) + " = ")
                elif a in dff_node_list:
                    f.write("(dff" + str(a) + " = ")
                elif self.merged_graph.subgraph.nodes[a]['op'] == "input" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[a]['op'] == "const_input":
                    f.write(" in" + str(a)  + " = ")
                elif self.merged_graph.subgraph.nodes[a]['op'] == "output" or self.merged_graph.subgraph.nodes[a]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[a]['op'] == "const_output":
                    f.write(" out" + str(a)  + " = ")
                for p in self.merged_graph.subgraph.predecessors(n):
                    if p not in inout_node_list:
                        f.write(", wire" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "input" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_input" or self.merged_graph.subgraph.nodes[p]['op'] == "const_input":
                        f.write(", in" + p)
                    elif self.merged_graph.subgraph.nodes[p]['op'] == "output" or self.merged_graph.subgraph.nodes[p]['op'] == "bit_output" or self.merged_graph.subgraph.nodes[p]['op'] == "const_output":
                        f.write(", out" + p)
                f.write(";\n")
        # True/False
        elif op == "true":
            f.write("\tassign wire" + str(n) + " = 1'b1;\n")
        elif op == "false":
            f.write("\tassign wire" + str(n) + " = 1'b0;\n")
        elif n not in inout_node_list and op != "const":
            raise ValueError(op + " is not yet supported on generating Verilog")

    # Write the dffs
    if len(dffp_list) > 0:
        f.write("\talways @(posedge clk) begin\n")
        for d in dffp_list:
            f.write(d)
        f.write("\tend\n")

    if len(dffn_list) > 0:
        f.write("\talways @(negedge clk) begin\n")
        for d in dffn_list:
            f.write(d)
        f.write("\tend\n")

    # Write the final parts
    f.write("endmodule")
    f.close()

