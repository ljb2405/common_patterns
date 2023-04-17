supported_ops =  {"mul", "mult_middle", "const", "not", "and", "or", "xor", "shl", \
                    "lshr", "ashr", "neg", "add", "sub", \
                    "sle", "sge", "ule", "uge", "eq", "mux", \
                    "slt", "sgt", "ult", "ugt", "smax", "smin", \
                    "umax", "umin", "absd", "abs", \
                    "bitnot", "bitconst", "bitand", "bitor", "bitxor", "bitmux", \
                    "floatadd", "floatsub", "floatmul" \
                    "pos", "reduce_and", "reduce_or", "reduce_xor", "reduce_xnor", "reduce_bool", \
                    "logic_not", "xnor", "shr", "sshl", "sshr", "logic_and", "logic_or", "eqx", \
                    "nex", "pow", "lt", "le", "ne", "ge", "gt", "div", "mod", "divfloor", "modfloor", \
                    "mux", "pmux", "tribuf", "sr", "adff", "sdff", "dffsr", "sdffe", "dff", "reduce_bool", "logic_not", "re", "_SDFFE_PP0P_", '_SDFF_PP0_', "_SDFFE_PP0N_", \
                    "_DFFE_PP_", "_DFF_P_", "_SDFFCE_PN0P_", "_SDFFCE_PN1P_", "_SDFFCE_PP0P_", "_DFF_P", "_DLATCH_N_", \
                    "_SDFF_PN1_", "_SDFF_PP0_", "_SDFF_PP1_", "al", "_DFFE_PP_", "_DFFE_PN_", "_SDFF_PN0_", "_SDFFCE_PP0N_", "_DFFE_PN0N_", "_DFFE_PN0P_", "_DFF_PN0_", "mem_v2"}

bit_input_ops = {"bitand", "bitor", "bitxor", "bitnot", "bitmux"}

bit_output_ops = {"lut", "sle", "sge", "ule", "uge", "eq", "slt", "sgt", "ult", "ugt", "bitand", "bitor", "bitxor", "bitnot", "bitmux", "bitconst"}

lut_supported_ops = {"bitand", "bitor", "bitxor", "bitnot", "bitmux"}

comm_ops =  {"and", "or", "xor", "add", "eq", "mul", "mult_middle","alu", "umax", "umin", "smax", "smin", "ne"}

primitive_ops = {"not", "and", "or", "xor", "shl", "lshr", "ashr", "add", "sub",
                "sle", "sge", "ule", "uge", "eq", "slt", "sgt", "ult", "ugt", 
                "smax", "smin", "umax", "umin", "absd", "abs", "mul", "mux",
                "bitand", "bitor", "bitxor", "bitnot", "bitmux", "floatadd", "floatsub", "floatmul", "pos", "reduce_and", "reduce_or", "reduce_xor", "reduce_xnor", "reduce_bool" \
                "logic_not", "xnor", "shr", "sshl", "sshr", "logic_and", "logic_or", "eqx", 
                "nex", "pow", "lt", "le", "ne", "ge", "gt", "div", "mod", "divfloor", "modfloor",
                "mux", "pmux", "tribuf", "sr", "adff", "sdff", "dffsr", "sdffe", "dff", "reduce_bool", "logic_not", "re", "_SDFFE_PP0P_", '_SDFF_PP0_', "_SDFFE_PP0N_", 
                "_DFFE_PP_", "_DFF_P_", "_SDFFCE_PN0P_", "_SDFFCE_PN1P_", "_SDFFCE_PP0P_", "al", "_DFFE_PP_", "_DFFE_PN_", "_SDFF_PN0_", "_SDFFCE_PP0N_", "_DFFE_PN0N_", "_DFFE_PN0P_", "_DFF_PN0_", "mem_v2"}

alu_supported_ops = {"and", "mult_middle", "or", "xor", "shl", "lshr", "ashr", "add", "sub",
                    "sle", "sge", "ule", "uge", "eq", "slt", "sgt", "ult", "ugt", 
                    "smax", "smin", "umax", "umin", "absd", "abs", "floatadd", "floatsub", "floatmul"}

fp_alu_supported_ops = {"floatadd", "floatsub", "floatmul"}

input_names = {"input", "bit_input", "in_self"}
const_names = {"const_input", "bit_const_input"}
output_names = {"output", "bit_output", "out_self"}


non_yosys_ops = {"alu", "bit_alu", "lut", "input", "bit_input", "const_input", "bit_const_input", "output", "bit_output", "gte", "lte", "sub", "shr", "mult_middle", "in_self", "out_self"}

weights = {"const":1, "bitconst":1, "and":1, "or":1, "xor":1, "shl":1, "lshr":1, "ashr":1, "add":1, "sub":1,
    "sle":1, "sge":1, "ule":1, "uge":1, "eq":1, "slt":1, "sgt":1, "ult":1, "ugt":1, 
    "smax":2, "smin":2, "umax":2, "umin":2, "absd":4, "abs":3, "mul":1, "mult_middle":1000, "mux":1,
    "bitand":1, "bitor":1, "bitxor":1, "bitnot":1, "bitmux":1, "floatadd":1, "floatsub":1, "floatmul":1, "bit_alu":1,
    "gte":1, "lte":1, "sub":1, "shr":1, "pos":1, "reduce_and":1, "reduce_or":1, "reduce_xor":1, "reduce_xnor":1, "reduce_bool":1,
                    "logic_not":1, "xnor":1, "shr":1, "sshl":1, "sshr":1, "logic_and":1, "logic_or":1, "eqx":1,
                    "nex":1, "pow":1000, "lt":2, "le":2, "ne":2, "ge":2, "gt":2, "div":1, "mod":1, "divfloor":2, "modfloor":2,
                    "mux":1, "pmux":1, "tribuf":1, "sr":1, "adff":1, "sdff":1, "dffsr":1, "sdffe":1, "dff":1, "reduce_bool":1, "logic_not":1, "nand":1, "nor":1,
                    "or": 1, "xor": 1, "true" : 1, "not": 1, "mem_v2" : 0.0001, "dlatch" : 0.0001, "_SDFFE_PP0P_" : 0.0001, "_SDFF_PP0_" : 0.0001, "re" : 0.0001, "_SDFFE_PP0N_" : 0.0001, 
                    "_DFFE_PP_": 0.0001, "_DFF_P_" : 0.0001, "_SDFFCE_PN0P_" : 0.0001, "_SDFFCE_PN1P_" : 0.0001, "_SDFFCE_PP0P_" : 0.0001, "_DFF_P":0.0001, "_DLATCH_N_":0.0001, \
                    "_SDFF_PN1_":0.0001, "_SDFF_PP0_":0.0001, "_SDFF_PP1_":0.0001, "al":1, "_DFFE_PP_":.0001, "_DFFE_PN_":.0001, "_SDFF_PN0_":0.0001, "_SDFFCE_PP0N_":0.0001,  "_DFFE_PN0N_": 0.0001, "_DFFE_PN0P_":0.0001, "_DFF_PN0_":0.0001, "mem_v2":0.0001}


# op_area = {"const":12, "bitconst":1000, "and":1000, "or":1000, "xor":1000, "shl":1000, "lshr":1000, "ashr":1000, "add":1000, "sub":1000,
#     "sle":1000, "sge":1000, "ule":1000, "uge":1000, "eq":1000, "slt":1000, "sgt":1000, "ult":1000, "ugt":1000, 
#     "smax":1000, "smin":1000, "umax":1000, "umin":1000, "absd":1000, "abs":1000, "mul":2030, "mux":30,
#     "bitand":13, "bitor":13, "bitxor":13, "bitnot":13, "bitmux":13, "floatadd":1000, "floatsub":1000, "floatmul":1000, "bit_alu":1000,
#     "gte":1000, "lte":1000, "sub":1000, "shr":1000}

# op_timing = {"const":12, "bitconst":100, "and":100, "or":100, "xor":100, "shl":100, "lshr":100, "ashr":100, "add":100, "sub":100,
#     "sle":100, "sge":100, "ule":100, "uge":100, "eq":100, "slt":100, "sgt":100, "ult":100, "ugt":100, 
#     "smax":100, "smin":100, "umax":100, "umin":100, "absd":100, "abs":100, "mul":200, "mux":30,
#     "bitand":13, "bitor":13, "bitxor":13, "bitnot":13, "bitmux":13, "floatadd":100, "floatsub":100, "floatmul":100, "bit_alu":100,
#     "gte":100, "lte":100, "sub":100, "shr":100}

op_costs = {
"add":	{"crit_path": 0.33, "area": 117.04, "energy": 96.62},
"sub":	{"crit_path": 0.33, "area": 117.04, "energy": 96.62},
"bit_alu":	{"crit_path": 0.22, "area": 123.1, "energy": 64.11},
"gte":	{"crit_path": 0.34, "area": 146.57, "energy": 88.66},
"shl":	{"crit_path": 0.34, "area": 104.01, "energy": 44.82},
"shr":	{"crit_path": 0.39, "area": 242.86, "energy": 107.25},
"mul":	{"crit_path": 1.00, "area": 2446.14, "energy": 2540.00},
"mult_middle":	{"crit_path": 1.00, "area": 2446.14, "energy": 2540.00},
"lte":	{"crit_path": 0.45, "area": 155.61, "energy": 88.66},
"alu":	{"crit_path": 1.00, "area": 1581.64, "energy": 1016.04},
"abs":	{"crit_path": 0.04, "area": 12.77, "energy": 10.12},
"absd":	{"crit_path": 0.65, "area": 264.67, "energy": 243.81},
"float_alu":	{"crit_path": 1.00, "area": 2446.14, "energy": 2540.00},
"const":	{"crit_path": 0.03, "area": 5, "energy": 5},
"bitconst":	{"crit_path": 0.03, "area": 5, "energy": 5},
"lut":	{"crit_path": 0.34, "area": 104.01, "energy": 44.82},
"mux":	{"crit_path": 0.34, "area": 30, "energy": 20}
}

op_map = {"const": "const",
"bitconst": "bitconst",
"and": "bit_alu",
"or": "bit_alu",
"xor": "bit_alu",
"shl": "shl",
"lshr": "shr",
"ashr": "shr",
"add": "add",
"sub": "sub",
"sle": "lte",
"sge": "gte",
"ule": "lte",
"uge": "gte",
"eq": "sub",
"slt": "sub",
"sgt": "sub",
"ult": "sub",
"ugt": "sub",
"smax": "gte",
"smin": "lte",
"umax": "gte",
"umin": "lte",
"absd": "absd",
"abs": "abs",
"mul": "mul",
"mult_middle": "mul",
"alu": "alu",
"mux": "mux",
"bitand": "lut",
"bitor": "lut",
"bitxor": "lut",
"bitnot": "lut",
"bitmux": "lut",
"floatadd": "float_alu",
"floatsub": "float_alu",
"floatmul": "float_alu",
"bit_alu": "bit_alu",
"gte": "gte",
"lte": "lte",
"sub": "sub",
"shr": "shr",
"lut": "lut",
"pos": "bit_alu",
"reduce_and": "bit_alu",
"reduce_or": "bit_alu",
"reduce_xor": "bit_alu",
"reduce_xnor": "bit_alu",
"reduce_bool": "bit_alu",
"logic_not": "bit_alu",
"xnor" : "bit_alu",
"shr" : "shr",
"sshl" : "shl",
"sshr" : "shl",
"logic_and" : "bit_alu",
"logic_or" : "bit_alu",
"eqx" : "sub",
"nex" : "bit_alu",
"pow" : "lut",
"lt" : "lte", 
"le" : "lte",
"ne" : "sub",
"ge" : "gte",
"gt" : "gte",
"div" : "mul",
"mod" : "mul",
"divfloor" : "mul",
"modfloor" : "mul",
"pmux" : "mux",
"tribuf" : "reg",
"sr" : "reg",
"adff" : "reg",
"sdff" : "reg",
"dffsr" : "reg",
"sdffe" : "reg",
"dff" : "reg",
"logic_not" : "bit_alu"}


# op_inputs = {"const":0, "bitconst":0, "and":2, "or":2, "xor":2, "shl":2, "lshr":2, "ashr":2, "add":2, "sub":2,
#     "sle":2, "sge":2, "ule":2, "uge":2, "eq":2, "slt":2, "sgt":2, "ult":2, "ugt":2, 
#     "smax":2, "smin":2, "umax":2, "umin":2, "absd":2, "abs":1, "mul":2, "mux":3,
#     "bitand":3, "bitor":3, "bitxor":3, "bitnot":3, "bitmux":3, "floatadd":2, "floatsub":2, "floatmul":2, "bit_alu":2,
#     "gte":2, "lte":2, "sub":2, "shr":2}

op_bitwidth = {"const": [], "bitconst": [], "and": [1, 1], "or": [1, 1], "xor": [1, 1], "shl": [1, 1], "lshr": [1, 1], "ashr": [1, 1], "add": [1, 1], "sub": [1, 1],
    "sle": [1, 1], "sge": [1, 1], "ule": [1, 1], "uge": [1, 1], "eq": [1, 1], "slt": [1, 1], "sgt": [1, 1], "ult": [1, 1], "ugt": [1, 1], 
    "smax": [1, 1], "smin": [1, 1], "umax": [1, 1], "umin": [1, 1], "absd": [1, 1], "abs": [1, 1], "mul": [1, 1], "mult_middle": [1, 1], "mux": [1, 1, 1],
    "bitand": [1, 1, 1], "bitor": [1, 1, 1], "bitxor": [1, 1, 1], "bitnot": [1, 1, 1], "bitmux": [1, 1, 1], "floatadd": [1, 1], "floatsub": [1, 1], "floatmul": [1, 1], "bit_alu": [1, 1],
    "gte": [1, 1], "lte": [1, 1], "sub": [1, 1], "shr": [1, 1], "pos": [], "reduce_and": [4, 1], "reduce_or": [4, 1], "reduce_xor": [4, 1], "reduce_xnor": [4, 1], "reduce_bool": [4, 1], 
                    "logic_not": [4,4], "xnor":[1,1], "shr":[1,1], "sshl":[1,1], "sshr":[1,1], "logic_and": [4,4], "logic_or": [4,4], "eqx":[1,1], 
                    "nex": [4,4], "pow":[1,1], "lt":[1,1], "le":[1,1], "ne":[1,1], "ge":[1,1], "gt":[1,1], "div":[1,1], "mod":[1,1], "divfloor":[1,1], "modfloor":[1,1],
                    "mux":[8,4], "pmux":[8,4], "tribuf":[1,1], "sr":[1,1], "adff":[1,1], "sdff":[1,1], "dffsr":[1,1], "sdffe":[1,1], "dff":[1,1], "reduce_bool": [4,1], "logic_not": [4,4],
                    "nand":[1,1], "nor":[1,1], "xor":[1,1], "or" :[1,1], "true":[1,1], "not":[1,1], "_SDFF_PP0_":[1,1], "_SDFFE_PP0P_":[1,1], "re":[1,1], "_SDFFE_PP0N_" : [1,1], 
                    "_DFFE_PP_":[1,1], "_DFF_P_":[1,1], "_SDFFCE_PN0P_":[1,1], "_SDFFCE_PN1P_":[1,1], "_SDFFCE_PP0P_":[1,1], "_DFF_P":[1,1], "_DLATCH_N_":[1,1], \
                    "_SDFF_PN1_":[1,1], "_SDFF_PP0_":[1,1], "_SDFF_PP1_":[1,1], "al" : [1,1], "_DFFE_PP_":[1,1], "_DFFE_PN_":[1,1], "_SDFF_PN0_":[1,1], "_SDFFCE_PP0N_":[1,1], "_DFFE_PN0N_":[1,1], "_DFFE_PN0P_":[1,1], "_DFF_PN0_":[1,1], "mem_v2":[1,1]}

dffs = {"_DFFE_PP_", "_DFF_P_", "_SDFFCE_PN0P_", "_SDFFCE_PN1P_", "_SDFFCE_PP0P_", "_SDFF_PP0_", "_SDFFE_PP0P_", "re", "_SDFFE_PP0N_", "_DFF_P_", "_DLATCH_N_", "_SDFF_PN1_", "_SDFF_PP0_", "_SDPP_PP1_", "mem_v2", "sdffe", "sdff", "dff", "_DFF_P", "_DLATCH_N_", \
                    "_SDFF_PN1_", "_SDFF_PP0_", "_SDFF_PP1_", "_DFFE_PP_", "_DFFE_PN_", "_SDFF_PN0_", "_SDFFCE_PP0N_", "al", "_DFFE_PN0N_", "_DFFE_PN0P_", "_DFF_PN0_", "mem_v2"}
latches = {"re", "al"}
dff_without_latch = {"_DFFE_PP_", "_DFF_P_", "_SDFFCE_PN0P_", "_SDFFCE_PN1P_", "_SDFFCE_PP0P_", "_SDFF_PP0_", "_SDFFE_PP0P_", "_SDFFE_PP0N_", "_DFF_P_", "_DLATCH_N_", "_SDFF_PN1_", "_SDFF_PP0_", "_SDPP_PP1_", "mem_v2", "sdffe", "sdff", "dff", "_DFF_P", "_DLATCH_N_", \
                    "_SDFF_PN1_", "_SDFF_PP0_", "_SDFF_PP1_", "_DFFE_PP_", "_DFFE_PN_", "_SDFF_PN0_", "_SDFFCE_PP0N_" , "_DFFE_PN0N_", "_DFFE_PN0P_", "_DFF_PN0_", "mem_v2"}
dff_enable = {"_SDFFCE_PN0P_", "_SDFFCE_PN1P_", "_SDFFCE_PP0P_", "_SDFFE_PP0P_", "_SDFFE_PP0N_", "_SDFFCE_PP0N_", "_DFFE_PP_", "_DFFE_PN0N_", "_DFFE_PN0P_"}
muxes = {"mux_out_0", "mux_in_0", "mux_in_1", "mux_out_1"}
op_types = []
op_types_flipped = []

node_counter = 0