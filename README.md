# Domain_Specific_FPGA_Toolchain

This repository conducts common pattern search via frequent subgraph mining algorith from GRAMI, maximum set independent analysis, and subgraph merging to produce Yosys-readable eblif file for domain-specific module of the FPGA that can be integrated using PRGA.

Refer to Mohammed Elseidy, Ehab Abdelhamid, Spiros Skiadopoulos, and Panos Kalnis. "GRAMI: Frequent Subgraph and Pattern Mining in a Single Large Graph. PVLDB, 7(7):517-528, 2014." to learn more about GraMi

Refer to J. Melchert, K. Feng, C. Donovick, R. Daly, R. Sharma, C. Barrett, M. A. Horowitz,
P. Hanrahan, and P. Raina, “Apex: A framework for automated processing element design space exploration using frequent subgraph analysis,” ASPLOS 2023, 2023. [Online]. Available: https://dl.acm.org/doi/10.1145/3582016.3582070 to learn more about the algorithms employed in this toolchain



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
python3 preprocess.py bcd2bin /home/user/common_patterns/benchmarks/bcd2bin.v
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

This code runs on Python 3.9.12


This code uses BSD-3 License.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.