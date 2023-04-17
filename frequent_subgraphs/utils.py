import os, pickle

def sort_subgraph_list(input_filename, output_filename, max_ind_set_size):

    with open(input_filename) as file:
        lines = file.readlines()

    graph_num = -1

    out_text = []

    for line in lines.copy():
        if ':' in line:
            graph_num += 1
            out_text.append(line)
        elif graph_num >= 0:
            if line[0] == 'v':
                if line.split(" ")[2][0] != '0':
                    out_text[graph_num] += line
            elif line[0] == 'e':
                if line.split(" ")[3][0] != '5':
                    out_text[graph_num] += line

    inds = sorted(max_ind_set_size.items(), key=lambda x: x[1][2], reverse=True)
    # breakpoint()
    # inds = sorted(max_ind_set_size.items(), key=lambda x: x[0], reverse=True)
    # out_text = out_text.reverse()

    ret_text = []

    for ind in inds:
        ret_text.append(out_text[ind[0]])
    

    if not os.path.exists('.temp'):
        os.makedirs('.temp')

    with open(output_filename, "w") as outfile:
        for subgraph in ret_text:
            outfile.write(subgraph)

    return inds

def grami_subgraph_mining(input_file, subgraph_inds, support, min_support):

    if len(subgraph_inds) == 0:
        max_subgraph = 1
    else:
        max_subgraph = max(subgraph_inds)
        
    # support =  300 # Starting support number

    print("Starting GraMi subgraph mining...")
    
    num_subgraphs = 0

    while num_subgraphs <= max_subgraph and support > min_support:#150:
        
        os.system('''cd GraMi
        ./grami -f ../../''' + input_file + ''' -s ''' + str(support) + ''' -t 1 -p 0 > grami_log.txt
        cd ../''')

        with open("GraMi/Output.txt") as file:
            lines = file.readlines()

        num_subgraphs = 0
        
        for line in lines.copy():
            if ':' in line:
                num_subgraphs += 1

        print("Support =", support, " num_subgraphs =", num_subgraphs)

        support -= 2

    print("Finished GraMi subgraph mining")
