import pickle
import networkx as nx
import typing as tp
from itertools import count, combinations
import pulp
from networkx import MultiDiGraph
# from .utils import *
import subgraph_merging_freq.config as config
# from subgraph import Subgraph, DSESubgraph
# from plot_utils import *
#import subgraph_merging_freq.utils as utils
# from .merger import *
from peak_gen.arch import read_arch, graph_arch

def gen_networkx_graph():
    arch = read_arch("outputs/PE.json")
    graph = MultiDiGraph()
    # inputs_subgraph.attr(rank='min')
    for input in arch.inputs:
        graph.add_node(str(input), type="in")

    for bit_input in arch.bit_inputs:
        graph.add_node(str(bit_input), type="in")

  
    

    mux_in0_idx = 0
    mux_in1_idx = 0
    mux_in2_idx = 0

    for module in arch.modules:
        if module.id in arch.inputs or module.id in arch.outputs or module.id in arch.bit_inputs or module.id in arch.bit_outputs:
            pass
        elif module.type_ != None:
            # print(module.id)
            graph.add_node(module.id, type=module.type_)
            # print(module.id)
        # print(graph.nodes[module.id]["type"])
        if module.type_ == "lut":
        
            if len(module.in0) > 1:
                graph.add_node("mux_in0_" + str(mux_in0_idx), type="mux")

                for in0 in module.in0:
                    graph.add_edge(str(in0), "mux_in0_" + str(mux_in0_idx))

                graph.add_edge("mux_in0_" + str(mux_in0_idx),str(module.id))  
                mux_in0_idx += 1
            else:
                graph.add_edge(str(module.in0[0]), str(module.id))
        
            if len(module.in1) > 1:
                graph.add_node("mux_in1_" + str(mux_in1_idx), type="mux")

                for in1 in module.in1:
                    graph.add_edge(str(in1), "mux_in1_" + str(mux_in1_idx))

                graph.add_edge("mux_in1_" + str(mux_in1_idx),str(module.id))  
                mux_in1_idx += 1
            else:
                graph.add_edge(str(module.in1[0]), str(module.id))

            if len(module.in2) > 1:
                graph.add_node("mux_in2_" + str(mux_in2_idx), type="mux")

                for in2 in module.in2:
                    graph.add_edge(str(in2), "mux_in2_" + str(mux_in2_idx))

                graph.add_edge("mux_in2_" + str(mux_in2_idx),str(module.id))  
                mux_in2_idx += 1
            else:
                graph.add_edge(str(module.in2[0]), str(module.id))
        else:
            if module.type_ == "mux":
                if len(module.in2) > 1:
                    graph.add_node("mux_in2_" + str(mux_in2_idx), type="mux")

                    for in2 in module.in2:
                        graph.add_edge(str(in2), "mux_in2_" + str(mux_in2_idx))

                    graph.add_edge("mux_in2_" + str(mux_in2_idx),str(module.id))  
                    mux_in2_idx += 1
                else:
                    graph.add_edge(str(module.in2[0]), str(module.id))
                    
            if len(module.in0) > 1:
                graph.add_node("mux_in0_" + str(mux_in0_idx), type="mux")

                for in0 in module.in0:
                    graph.add_edge(str(in0), "mux_in0_" + str(mux_in0_idx))

                graph.add_edge("mux_in0_" + str(mux_in0_idx),str(module.id))  
                mux_in0_idx += 1
            else:
                graph.add_edge(str(module.in0[0]), str(module.id))
        
            if len(module.in1) > 1:
                graph.add_node("mux_in1_" + str(mux_in1_idx),type="mux")

                for in1 in module.in1:
                    graph.add_edge(str(in1), "mux_in1_" + str(mux_in1_idx))

                graph.add_edge("mux_in1_" + str(mux_in1_idx),str(module.id))  
                mux_in1_idx += 1
            else:
                graph.add_edge(str(module.in1[0]), str(module.id))



    mux_reg_idx = 0
    for reg in arch.regs:
        if reg != None:
            graph.add_node(str(reg.id), type="reg")

        if len(reg.in_) > 1:
            graph.add_node("mux_reg_" + str(mux_reg_idx),type="mux")

            for in_ in reg.in_:
                graph.add_edge(str(in_), "mux_reg_" + str(mux_reg_idx))

            graph.add_edge("mux_reg_" + str(mux_reg_idx), str(reg.id))  
            mux_reg_idx += 1
        else:
            graph.add_edge(str(reg.in_[0]), str(reg.id))

    mux_bit_reg_idx = 0
    for bit_reg in arch.bit_regs:
        if reg != None:
            graph.add_node(str(bit_reg.id), type="bit_reg")

        if len(bit_reg.in_) > 1:
            graph.add_node("mux_bit_reg_" + str(mux_bit_reg_idx),type="mux")

            for in_ in bit_reg.in_:
                graph.add_edge(str(in_), "mux_bit_reg_" + str(mux_bit_reg_idx))

            graph.add_edge("mux_bit_reg_" + str(mux_bit_reg_idx), str(bit_reg.id))  
            mux_bit_reg_idx += 1
        else:
            graph.add_edge(str(bit_reg.in_[0]), str(bit_reg.id))


    for const_idx, reg in enumerate(arch.const_inputs):
        graph.add_node(str(reg.id), type="const")

    mux_out_idx = 0
    
    for i, output in enumerate(arch.outputs):
        
        graph.add_node("out_" + str(i), type="out")
        if len(output) > 1:
            graph.add_node("mux_out_" + str(mux_out_idx), type="mux")

            for out in output:
                graph.add_edge(str(out), "mux_out_" + str(mux_out_idx))

            graph.add_edge("mux_out_" + str(mux_out_idx), "out_" + str(i))
            mux_out_idx += 1
        elif len(output) == 1:
            graph.add_edge(str(output[0]), "out_" + str(i))


    for i, output in enumerate(arch.bit_outputs):
        
        graph.add_node("bit_out_" + str(i), type="out")
        if len(output) > 1:
            graph.add_node("mux_out_" + str(mux_out_idx), type="mux")

            for out in output:
                graph.add_edge(str(out), "mux_out_" + str(mux_out_idx))

            graph.add_edge("mux_out_" + str(mux_out_idx), "bit_out_" + str(i))
            mux_out_idx += 1
        elif len(output) == 1:
            graph.add_edge(str(output[0]), "bit_out_" + str(i))


    # print(graph.nodes['in225']["type"])
    print(graph.nodes)
    if graph.has_node('None'):
        graph.remove_node('None')
    return graph.copy()

def gen_eblif():
    graph = gen_networkx_graph()
    arch = read_arch("outputs/PE.json")
    in_list = []
    out_list = []

   
    f = open("outputs/spec_module.eblif", 'w')

    # Write intro parts
    f.write("# Generated by Automated Toolchain for Domain-Specific FPGA\n")
    f.write(".model spec_module\n")
    f.write(".inputs clk reset enable")
    for input in arch.inputs:
        f.write("wire" + str(input) + " ")
        in_list.append("wire" + str(input))
    for bit_input in arch.bit_inputs:
        f.write("wire" + str(bit_input) + " ")
        in_list.append("wire" + str(bit_input))
    f.write("\n.outputs wireout_0")
    # for output in arch.outputs:
    #     print(output)
    #     f.write(" wire" + str(output))
    #     out_list.append("wire" + str(output))
    f.write("\n.names $false\n.names $true\n1\n.names $undef\n")
    print(graph.nodes.data())
    for node in graph.__iter__():
        type = graph.nodes[node]['type']
        if type == "in" or type == "out":
            pass
        elif type in config.dff_without_latch:
            f.write("\n.subckt $" + type + " C=clk")
            ins = graph.predecessors(node)
            outs = graph.successors(node)
            # EDIT IN THE ARCH.PY TO CONSIDER LATCH and DFFS as one-input, one-output gates
            for i in ins:
                f.write(" D=wire" + str(i))
            if type in config.dff_enable:
                f.write(" E=enable")
            for o in outs:
                f.write(" Q=wire" + str(o))
            f.write(" R=reset")
        elif type in config.latches:
            f.write("\n.latch")
            ins = graph.predecessors(node)
            outs = graph.successors(node)

            for i in ins:
                f.write(" wire" + str(i))
            for o in outs:
                f.write(" wire" + str(o))
            
            f.write(" " + type + " clk 2")

        elif type == "mux":
            f.write("\n.subckt $mux")

            ins = graph.predecessors(node)
            outs = graph.successors(node)
            in_list = []
            for i in ins:
                in_list.append("wire" + str(i))
            if len(in_list) == 2:
                f.write(" A=wire" + str(in_list[0]) + " B=wire" + str(in_list[1]))
            elif len(in_list) > 2:
                for i in in_list:
                    f.write(" A=wire" + str(i))
            f.write(" S=select" + node)
            for ind, o in enumerate(outs):
                f.write(" Y=wire" + str(o))

        elif type == "true":
            f.write("\n$true")
        #elif type == "const":
        else:
            f.write("\n.names")
            ins = graph.predecessors(node)
            outs = graph.successors(node)

            for i in ins:
                f.write(" wire" + str(i))
            
            for o in outs:
                f.write(" wire" + str(o))
            
            if type == "and":
                f.write("\n11 1")
            elif type == "nor":
                f.write("\n00 1")    
            elif type == "xor":
                f.write("\n10 1\n01 1")
            elif type == "nand":
                f.write("\n0- 1\n-0 1")
            elif type == "or":
                f.write("\n1- 1\n-1 1")
            elif type == "not":
                f.write("\n0 1")
            else:
                print(type)

    f.write("\n.end")

if __name__ == "__main__":
    gen_eblif()