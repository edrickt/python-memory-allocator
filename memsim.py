from memoryallocator import MemoryAllocator, FIRST_FIT, BEST_FIT, IMPLICIT, EXPLICIT
from helperfunctions import *

if __name__ == "__main__":
    # Get command line arguments
    args = parse_args()
    # Open the infile
    infile = open_file(args.infileString)
    # Create memory instructions array from infile
    memInstArr = create_meminst_array(infile)
    # Simulate dynamic memory and get results
    result = simulate_dynamic_memory(memInstArr, args)
    # Write to outfile
    outfile = open(args.outfileString, "w")
    outfile.write(result)
