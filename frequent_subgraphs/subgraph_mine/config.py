supported_ops =  {"mul", "mult_middle", "const", "not", "and", "or", "xor", "shl", \
                    "lshr", "ashr", "neg", "add", "sub", \
                    "sle", "sge", "ule", "uge", "eq", "mux", \
                    "slt", "sgt", "ult", "ugt", "smax", "smin", \
                    "umax", "umin", "absd", "abs", \
                    "bitnot", "bitconst", "bitand", "bitor", "bitxor", "bitmux", \
                    "floatadd", "floatsub", "floatmul" \
                    "pos", "reduce_and", "reduce_or", "reduce_xor", "reduce_xnor", "reduce_bool" \
                    "logic_not", "xnor", "shr", "sshl", "sshr", "logic_and", "logic_or", "eqx" \
                    "nex", "pow", "lt", "le", "ne", "ge", "gt", "div", "mod", "divfloor", "modfloor", \
                    "mux", "pmux", "tribuf", "sr", "adff", "sdff", "dffsr", "sdffe", "dff", "reduce_bool", "logic_not", "dlatch", "mem_v2", "nand", "nor", "or", \
                    "_SDFFE_PP0P_", "_SDFF_PP0_", "re", "_SDFFE_PP0N_", "_DFFE_PP_", "_DFF_P_", "_SDFFCE_PN0P_", "_SDFFCE_PN1P_", "_SDFFCE_PP0P_", "_DFF_P", "_DLATCH_N_", \
                    "_SDFF_PN1_", "_SDFF_PP0_", "_SDFF_PP1_", "al", "_DFFE_PP_", "_DFFE_PN_", "_SDFF_PN0_", "_SDFFCE_PP0N_", "_DFFE_PN0N_", "_DFFE_PN0P_", "_DFF_PN0_"}

supported_truth_tables = {"111" : "and", "01" : "not", "11" : "wire", "0-1" : "nand", "1" : "true", "001" : "nor", "1-1" : "or", "101" : "xor"}