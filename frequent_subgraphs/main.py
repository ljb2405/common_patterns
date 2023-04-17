import sys
import argparse
import os
import pickle
import blifparser.blifparser as blifparser
from subgraph_mine.convert_eblif3 import convert_eblif3
from utils import *
from subgraph_mine.find_maximal_ind_set import find_maximal_independent_set
from subgraph_mine.graph_output import graph_output
from subgraph_merging_freq.merge_subgraphs import merge_subgraphs
import subgraph_mine.config
from graphviz import Digraph
import matplotlib
# import blif2graph
import time

def main():
    tic = time.perf_counter()
    parser = argparse.ArgumentParser(description='Graph analysis of Yosys eblif files')
    parser.add_argument('-c', '--cached', help='Use cached subgraphs', action="store_true", default=False)
    parser.add_argument('-f', '--files', nargs='+', metavar=("file", "subgraph_index"),help='Application files for analysis', action='append')
    parser.add_argument('-p', '--pipeline', help="Number of pipelining stages", type=int, default = 0)

    args = parser.parse_args()
    use_cached_subgraphs = args.cached
    file_ind_pairs = {}

    for file_ind in args.files:
        if '.eblif' not in file_ind[0]:
            parser.error('-f file is not a eblif file')

        try:
            inds = [int(i) for i in file_ind[1:]]
        except:
            parser.error('subgraph indicies are not ints')

        file_ind_pairs[file_ind[0]] = inds

    file_names = list(file_ind_pairs.keys())
    subgraph_file_ind_pairs = {}

    
    if not use_cached_subgraphs:
        num_nodes = convert_eblif3(file_names)

        dot_files = [".temp/" + os.path.basename(f).replace(".eblif", ".dot") for f in file_names]

        for file_ind, file in enumerate(file_names):
            file_stripped = os.path.basename(file).split(".")[0]

            print("Starting on ", file_stripped)

            # Takes in grami_in.txt produces orig_graph.pdf
            print("Graphing original graph")
            #graph_output(dot_files[file_ind], file_stripped)
            support = int(num_nodes[file_ind] * 0.13)
            min_support = int(num_nodes[file_ind] * 0.01)
            #TODO: Edit the function to direct to the correct GraMi directory
            # Takes in grami_in.txt and subgraph support, produces Output.txt
            print(file_ind_pairs[file])
            grami_subgraph_mining(dot_files[file_ind], file_ind_pairs[file], support, min_support)

            max_ind_set_stats = find_maximal_independent_set(dot_files[file_ind], "GraMi/Output.txt")

            new_subgraphs_file = dot_files[file_ind].replace(".dot", "_subgraphs.dot")
            max_ind_set_stats = sort_subgraph_list("GraMi/Output.txt", new_subgraphs_file, max_ind_set_stats)

            # Takes in Output.txt produces subgraphs.pdf
            print("Graphing subgraphs")
            graph_output(new_subgraphs_file, file_stripped + "_subgraphs", max_ind_set_stats)

            subgraph_file_ind_pairs[dot_files[file_ind].replace(".dot", "_subgraphs.dot")] = file_ind_pairs[file]
        else:
            dot_files = [".temp/" + os.path.basename(f).replace(".eblif", ".dot") for f in file_names]
            for file_ind, file in enumerate(file_names):
                subgraph_file_ind_pairs[dot_files[file_ind].replace(".dot", "_subgraphs.dot")] = file_ind_pairs[file]
    
    print("Starting subgraph merging")
    print(subgraph_file_ind_pairs)
    merge_subgraphs(subgraph_file_ind_pairs, args.pipeline)
    toc = time.perf_counter()
    t = (toc - tic) / 60
    print(f"{t:0.4f} minutes elapsed")

if __name__ == "__main__":
    main()