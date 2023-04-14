# Domain_Specific_FPGA_Toolchain

This repository conducts common pattern search via frequent subgraph mining algorith from GRAMI, maximum set independent analysis, and subgraph merging to produce Yosys-readable eblif file for domain-specific module of the FPGA that can be integrated using PRGA.

The toolchain utilizes Yosys and other tools. 
Refer to Yosys documentation for Yosys installation and GRAMI documentation under frequent_subgraphs/GraMi to install these in the system.

The toolchain takes in Verilog file as an input and currently produces a rudimentary eblif file of a specialized module.

Usage:
1. Use preprocess/preprocess.py with:

```bash
python3 preprocess.py module_name path/where/the/file/exists
```

An example command would be:
```bash
python3 preprocess.py bcd2bin /home/user/Domain_Specific_FPGA_Toolchain/benchmarks/bcd2bin.v
```
This produces an eblif file of the Verilog file. 

2. After the preprocessing, use frequent_subgraphs/main.py with:

```bash
python3 main.py -f relative_path/module_name.eblif indices of subgraphs the user wish to use
```

An example command would be:
```bash
python3 main.py -f ../benchmarks/bcd2bin.eblif 0 2
```
If the user wants to find 3 subgraphs and use the first one and then third one found. 

This will produce an eblif file that can be fetched back into Yosys. 

Requirements for this toolchain can be found in requirements.txt