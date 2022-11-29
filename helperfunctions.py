import argparse
import sys
from dataclass import Arguments, MemoryInstruction
from memoryallocator import IMPLICIT, EXPLICIT, FIRST_FIT, BEST_FIT, MemoryAllocator

def simulate_dynamic_memory(memInstArr, args): 
    memalloc = MemoryAllocator(args.listType, args.fitType)
    pointerArr = [None] * 1000
    for inst in memInstArr:
        if inst.instruction == "a":
            pointerArr.insert(inst.name, memalloc.myalloc(inst.size))
        elif inst.instruction == "r":
            pointerArr.insert(inst.newName, memalloc.myrealloc(pointerArr[inst.name], inst.size))
        elif inst.instruction == "f":
            memalloc.myfree(pointerArr[inst.name])
    return memalloc.heap.get_simulation_results()

def simulate_example_infiles():
    infiles = ["1.in", "2.in", "3.in", "4.in", "5.in", "6.in", "7.in", "8.in", "9.in", "10.in", "11.in"]
    args = [Arguments("", "implicit", "first", ""),
            Arguments("", "implicit", "best", ""),
            Arguments("", "explicit", "first", ""),
            Arguments("", "explicit", "best", "")]
    for i in range(0, len(infiles)):
        if i != 8:
            file = open_file("examples\\" + infiles[i])
            memInstArr = create_meminst_array(file)
            for j in range(0, len(args)):
                result = simulate_dynamic_memory(memInstArr, args[j])
                outfile = open("./results/" + str(i+1) + "." + args[j].listType + "." + args[j].fitType + "." + "out", "w")
                outfile.write(result)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help="Output file", required=True)
    parser.add_argument("-l", help="List type: implicit or explicit", required=True)
    parser.add_argument("-f", help="Fit type: first or best", required=True)
    parser.add_argument("-i", help="Input file", required=True)
    args = parser.parse_args()
    verify_input(args)
    return Arguments(args.o, args.l, args.f, args.i)

def verify_input(args):
    if args.l == "implicit" or args.l == "explicit":
        if args.f == "first" or args.f == "best":
            return
        else:
            print("memsim.py: Invalid fit type")
    else:
        print("memsim.py: Invalid list type")
    sys.exit(1)

def open_file(fileString):
    try:
        file = open(fileString, "r")
        return file
    except:
        print("memsim.py: No such file or directory")
        sys.exit(1)

def create_meminst_array(file):
    memInstArr = []
    for line in file:
        curLine = line.strip().split(", ")
        instruction = curLine[0]
        memInst = MemoryInstruction(instruction=instruction)
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
    return memInstArr
