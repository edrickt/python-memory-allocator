import argparse
import sys
from dataclass import Arguments, MemoryInstruction
from memoryallocator import IMPLICIT, EXPLICIT, FIRST_FIT, BEST_FIT, MemoryAllocator

# Simulate dynamic memory based on the memory instructios from the file and arguments
# from command line
def simulate_dynamic_memory(memInstArr, args):
    # Create memory allocator based on command line args list type and fit type
    memalloc = MemoryAllocator(args.listType, args.fitType)
    # Create an array to store pointers
    pointerArr = [None] * 10000
    # Determine type of instruction
    for inst in memInstArr:
        # If allocation or reallocation, run myalloc or myrealloc and insert the pointer
        # into the index given by the name
        if inst.instruction == "a":
            pointerArr.insert(inst.name, memalloc.myalloc(inst.size))
        elif inst.instruction == "r":
            pointerArr.insert(inst.newName, memalloc.myrealloc(pointerArr[inst.name], inst.size))
        # If free, run myfree on the pointer in the index of pointer array given by name
        elif inst.instruction == "f":
            memalloc.myfree(pointerArr[inst.name])
    # Return the contents of the heap
    return memalloc.heap.get_simulation_results()

# TESTING PURPOSED ONLY! Runs the program on all of the files in the examples
# folder only. Examples folder must exist and result folder must exist.
def simulate_example_infiles():
    # All in files
    infiles = ["1.in", "2.in", "3.in", "4.in", "5.in", "6.in", "7.in", "8.in", "9.in", "10.in", "11.in"]
    # All cases to test
    args = [Arguments("", "implicit", "first", ""),
            Arguments("", "implicit", "best", ""),
            Arguments("", "explicit", "first", ""),
            Arguments("", "explicit", "best", "")]
    # For all infiles
    for i in range(0, len(infiles)):
        # If not 9.in since that causes program to exit
        if i != 8:
            # Open the file
            file = open_file("examples/" + infiles[i])
            # Create the memory instruction array
            memInstArr = create_meminst_array(file)
            # Run test for each test case and output to file
            for j in range(0, len(args)):
                result = simulate_dynamic_memory(memInstArr, args[j])
                outfile = open("./results/" + str(i+1) + "." + args[j].listType + "." + args[j].fitType + "." + "out", "w")
                outfile.write(result)

# Parse the command line arguments
def parse_args():
    # Initialize argument parser
    parser = argparse.ArgumentParser()
    # Outfile argument required
    parser.add_argument("-o", help="Output file", required=True)
    # List type argument required
    parser.add_argument("-l", help="List type: implicit or explicit", required=True)
    # Fit type argument required
    parser.add_argument("-f", help="Fit type: first or best", required=True)
    # Input file argument required
    parser.add_argument("-i", help="Input file", required=True)
    # Parse the command line argument into a data class
    args = parser.parse_args()
    # Verify that list type and fit type are valid
    verify_input(args)
    # Return as our data class of Arguments
    return Arguments(args.o, args.l, args.f, args.i)

# Verify that list type and fit type from command line argument is valid
def verify_input(args):
    if args.l == "implicit" or args.l == "explicit":
        if args.f == "first" or args.f == "best":
            return
        else:
            print("memsim.py: Invalid fit type")
    else:
        print("memsim.py: Invalid list type")
    sys.exit(1)

# Open file for reading
def open_file(fileString):
    try:
        file = open(fileString, "r")
        return file
    except:
        print("memsim.py: No such file or directory")
        sys.exit(1)

# Create an array of memory instructinons
def create_meminst_array(file):
    memInstArr = []
    # For each line in the in file
    for line in file:
        # Remove the commas
        curLine = line.strip().split(", ")
        instruction = curLine[0]
        # Create memory instruction based on first character
        memInst = MemoryInstruction(instruction=instruction)
        # Depending on memory instruction, then population necessary
        # attributes and append to the array
        if instruction == "f":
            memInst.name = int(curLine[1])
            memInstArr.append(memInst)
        elif instruction == "r":
            memInst.size = int(curLine[1])
            memInst.name = int(curLine[2])
            memInst.newName = int(curLine[3])
            memInstArr.append(memInst)
        elif instruction == "a":
            memInst.size = int(curLine[1])
            memInst.name = int(curLine[2])
            memInstArr.append(memInst)
    # Return array
    return memInstArr
