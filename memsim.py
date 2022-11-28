from memoryallocator import MemoryAllocator, FIRST_FIT, BEST_FIT, IMPLICIT, EXPLICIT
from helperfunctions import *

if __name__ == "__main__":
    args = parse_args()
    # args = Arguments("out", "implicit", "first", "examples/1.in")
    infile = open_file(args.infileString)
    memInstArr = create_meminst_array(infile)
    result = simulate_dynamic_memory(memInstArr, args)
    outfile = open(args.outfileString, "w")
    outfile.write(result)
