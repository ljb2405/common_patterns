import sys
import os
import pickle
import blifparser.blifparser as blifparser
import subgraph_mine.config as config
from graphviz import Digraph
import time

# Finds connection within the eblif file
def find_conn(filepath):
    
    f = open(filepath, 'r')
    result = []
    lines = f.readlines()
    for line in lines:
        if ".conn" in line:
            result.append(line[:-1])
            
    f.close()
    return result
# Second version to the convert_eblif in order to get rid of wires as constants and see if it that improves the speed
# blif dudes are in list type
def convert_eblif3(eblif_files):

    if not os.path.exists('.temp'):
        os.makedirs('.temp')
    

    dot_files = [os.path.basename(f).replace(".eblif", ".dot") for f in eblif_files]

    op_types = {}
    op_types["in_self"] = "0"
    op_types["out_self"] = "1"
    op_types["const"] = "2"
    instance_names = {}
    used_ops = set()
    unsupported_ops = set()
    num_nodes = []
    op_index = 3
    
    for ind, f in enumerate(eblif_files):

        out_file = open('.temp/' + dot_files[ind], 'w')

        ## TAKEN FROM THE APEX PROJECT NEEDS TO BE CHANGED TO BE ABLE TO TAKE MULTIPLE OUTPUTS
        ## Self indicates output of the circuit
        ## TODO: Need to generalize to take in multiple outputs
        ## TODO: Try to redeuce the clutter on the graph by getting rid of wires
        ## TODO: Fix to check parameters to see if the parameters are inputs/outputs
        # instance_names["self"] = 0
        ##

        out_file.write('t # 1\n')
        # Inputs and outputs to the operators
        inputs = {}
        outputs = {}
        conns = {} 
        unsupported_wires = []
        filepath = os.path.abspath(f)
        parser = blifparser.BlifParser(filepath)
        # Connections within the blif file in list format
        conn = find_conn(filepath)

        blif = parser.blif
        # dot = Digraph(format="pdf")
        dot = Digraph(format="pdf", engine="neato")
            #         graph_attr=dict(splines='true',
            #                   sep='5',
            #                   overlap='scale'),
            #   node_attr=dict(shape='circle',   
            #                  margin='0',
            #                  fontsize='10',
            #                  width='0.2',
            #                  height='0.2',
            #                  fixedsize='true'),
            #   edge_attr=dict(arrowsize='0.4'))
        edges = []

        # get the name of the model
        print(blif.model.name)
        # Writes the inputs
        inst_ind = len(blif.inputs.inputs)
        for i in range(0, inst_ind):
            out_file.write('v ' + str(i) + ' ' + op_types['in_self'] + '\n')
            dot.node(str(i), "in_self")
            instance_names[blif.inputs.inputs[i].replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')] = i
            inputs[blif.inputs.inputs[i].replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')] = i
         # Writes the outputs
        inst_ind += len(blif.outputs.outputs)
        for i in range(len(blif.inputs.inputs), inst_ind):
            out_file.write('v ' + str(i) + ' ' + op_types['out_self'] + '\n')
            dot.node(str(i), "out_self")
            instance_names[blif.outputs.outputs[i-len(blif.inputs.inputs)].replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')] = i
            outputs[blif.outputs.outputs[i-len(blif.inputs.inputs)].replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')] = i

        instance_id = inst_ind

        # For nodes
        # For .names
        for n in blif.booleanfunctions:
            
            if len(n.truthtable) != 0:
                t = ''.join(n.truthtable[0])
            elif n.output == "$false":
                
                dot.node(str(instance_id), "false")
                out_file.write('v ' + str(instance_id) + ' ' + str(op_types["const"]) + '\n')
                instance_names["_false"] = instance_id
                instance_id += 1
                t = "0"
            elif n.output == "$undef":
                dot.node(str(instance_id), "undef")
                out_file.write('v ' + str(instance_id) + ' ' + str(op_types["const"]) + '\n')
                instance_names["_undef"] = instance_id
                instance_id += 1
                t = "0"
            else:
                print(n)
                unsupported_ops.add(n)
                t = "0"
            
            
            if t in config.supported_truth_tables:
                op = config.supported_truth_tables.get(t)
                used_ops.add(op)
                if op not in op_types:
                    op_types[op] = op_index
                    op_index += 1
                dot.node(str(instance_id), op)
                out_file.write('v ' + str(instance_id) + ' ' + str(op_types[op]) + '\n')
                instance_names[n.output.replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')] = instance_id
                instance_id += 1

        # For subckts
        for s in blif.subcircuits:
            op = s.modelname[1:]

            if op in config.supported_ops:
                used_ops.add(op)
                if op not in op_types:
                    op_types[op] = op_index
                    op_index += 1
                dot.node(str(instance_id), op)
                out_file.write('v ' + str(instance_id) + ' ' + str(op_types[op]) + '\n')
                node_str = s.params[-1][s.params[-1].find("=")+1:]
                for p in s.params:
                    if (p[0] == "Y") | (p[0] == "Q"):
                        node_str = p[p.find("=")+1:]
                instance_names[node_str.replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')] = instance_id
                instance_id += 1
            else:
                unsupported_ops.add(op)
                print(op)

        for l in blif.latches:
            op = l.type

            if op in config.supported_ops:
                used_ops.add(op)
                if op not in op_types:
                    op_types[op] = op_index
                    op_index += 1
                dot.node(str(instance_id), op)
                out_file.write('v ' + str(instance_id) + ' ' + str(op_types[op]) + '\n')
                node_str = l.output.replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')
                instance_names[node_str] = instance_id
                instance_id += 1
            else:
                unsupported_ops.add(op)
                print(op)
        
        for c in conn:
            splitted = c.split(' ')
            source = splitted[1].replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')
            sink = splitted[2].replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')

            if instance_names.get(source) == None:
                dot.node(str(instance_id), "wire")
                out_file.write('v ' + str(instance_id) + ' ' + str(op_types["const"]) + '\n')
                instance_names[source] = instance_id
                conns[source] = instance_id
                instance_id += 1
                
            
            if instance_names.get(sink) == None:
                dot.node(str(instance_id), "wire")
                out_file.write('v ' + str(instance_id) + ' ' + str(op_types["const"]) + '\n')
                instance_names[sink] = instance_id
                conns[sink] = instance_id
                instance_id += 1
            
            dot.edge(str(instance_names[source]), str(instance_names[sink]))
            edges.append("e " + str(instance_names[source]) + " " + str(instance_names[sink]) + ' 0\n')


        # For edges
        i = 0
        tic = time.perf_counter()    
        for n in blif.booleanfunctions:
            node_str = n.output.replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')

            if (node_str != "_true") & (node_str != "_false") & (node_str != "_undef"):
                if instance_names.get(node_str) != None:
                    innode_id = instance_names[node_str]

                    for inp in n.inputs:
                        inp_str = inp.replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')
                        
                        if instance_names.get(inp_str) != None:
                            outnode_id = instance_names[inp_str]
                            dot.edge(str(outnode_id), str(innode_id))
                            if outputs.get(inp_str) != None:
                                edges.append("e " + str(outnode_id) + " " + str(innode_id) + ' 0\n')
                            else:
                                edges.append("e " + str(outnode_id) + " " + str(innode_id) + ' 1\n')
                        else:
                            print(".names wire error for the inputs")
                            unsupported_wires.append(inp)
            elif (node_str != "_true") & (node_str != "_false") & (node_str != "_undef"):
                print(".names wire error for the outputs")
                unsupported_wires.append(node_str)
                
            toc = time.perf_counter()
            #print(str(i) + " out of " + str(len(blif.subcircuits) + len(blif.booleanfunctions)) + " components completed")
            #print(f"{toc - tic:0.4f} seconds elapsed")
            # i += 1
        for l in blif.latches:
            node_str = l.output.replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')

        
            if instance_names.get(node_str) != None:
                innode_id = instance_names[node_str]

                inp_str = l.input.replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')
                
                if instance_names.get(inp_str) != None:
                    outnode_id = instance_names[inp_str]
                    dot.edge(str(outnode_id), str(innode_id))
                    if outputs.get(inp_str) != None:
                        edges.append("e " + str(outnode_id) + " " + str(innode_id) + ' 0\n')
                    else:
                        edges.append("e " + str(outnode_id) + " " + str(innode_id) + ' 1\n')
                else:
                    print(".names wire error for the inputs")
                    unsupported_wires.append(l.input)

        for s1 in blif.subcircuits:
            node_str = s1.params[-1][s1.params[-1].find("=")+1:]
            for p in s1.params:
                if (p[0] == "Y") | (p[0] == "Q"):
                    node_str = p[p.find("=")+1:]
            if instance_names.get(node_str.replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')) != None:
                innode_id = instance_names[node_str.replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')]
                for p1 in s1.params:
                    #print(p1[0:2])
                    if (p1[0] == "A") | (p1[0] == "B") | (p1[0] == "D"):
                        str_ind = p1.find("=")
                        processed_p1 = p1[str_ind+1:].replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')
                        
                        if instance_names.get(processed_p1) != None:
                            outnode_id = instance_names[processed_p1]
                            dot.edge(str(outnode_id), str(innode_id))
                            if (p1[0] == "A") or (p1[0] == "D"):
                                edges.append("e " + str(outnode_id) + " " + str(innode_id) + ' 0\n')
                            else:    
                                edges.append("e " + str(outnode_id) + " " + str(innode_id) + ' 1\n')
                            
                        else:
                            print(".subckt wire error for the inputs")
                            unsupported_wires.append(p1)
                    elif p1[0:2] == "S=":
                        str_ind = p1.find("=")
                        processed_p1 = p1[str_ind+1:].replace('.','_').replace('\\', '_').replace('$', '_').replace(':', '_').replace('[', '_').replace(']','')

                        if instance_names.get(processed_p1) != None:
                            outnode_id = instance_names[processed_p1]
                            dot.edge(str(outnode_id), str(innode_id))
                            edges.append("e " + str(outnode_id) + " " + str(innode_id) + ' 2\n')
                        else:
                            print(".subckt wire error for the sel signal")
                            unsupported_wires.append(p1)



            else:
                print(".subckt wire error for the output")
                unsupported_wires.append(node_str)
                
            
            toc = time.perf_counter()
            #print(str(i) + " out of " + str(len(blif.subcircuits) + len(blif.booleanfunctions)) + " components completed")
            #print(f"{toc - tic:0.4f} seconds elapsed")
            # i += 1

        print("Node and edge construction finished")
        # For edges
        proc_edges = []    
        for e in edges:
            if e not in proc_edges:
                proc_edges.append(e)
        for e in proc_edges:
            out_file.write(e)
        print("Edge appending finished.... wrapping up the graph conversion")
        with open('.temp/op_types.txt', 'wb') as op_types_out_file:
            pickle.dump(op_types, op_types_out_file)

        with open('.temp/used_ops.txt', 'wb') as used_ops_out_file:
            pickle.dump(used_ops, used_ops_out_file)
        if len(instance_names) < 10000:
            dot.render(f'pdf/{dot_files[ind]}', view=False)  
        print("Used ops:", op_types) 
        print("Unsupported ops:", unsupported_ops)
        print("Unsupported wires: ", unsupported_wires)
        num_nodes.append(instance_id)
        # print(inputs)
        # print(outputs)
    return num_nodes

if __name__ == "__main__":
    convert_eblif3(["../bgm5.eblif"])