from tcl_generator import generate_tcl
import sys, os

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        RuntimeError("There must be a Verilog file input!")

    else:
        module_name = sys.argv[1]
        abs_file_path = sys.argv[2]
        generate_tcl(module_name, abs_file_path)
        os.system("yosys -c " + module_name + "_synth.tcl")