import argparse
import sys
from dataclass import Arguments, MemoryInstruction

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help="Output file", required=True)
    parser.add_argument("-l", help="List type: implicit or explicit", required=True)
    parser.add_argument("-f", help="Fit type: first or best", required=True)
    parser.add_argument("-i", help="Input file", required=True)
    args = parser.parse_args()
    return Arguments(args.o, args.l, args.f, args.i)

def open_file(fileString):
    try:
        file = open(fileString, "r")
        return file
    except:
        print("memsim.py: No such file or directory")
        exit(sys.exit(1))

def create_meminst_array(file):
    memInstArr = []
    for line in file:
        curLine = line.strip().split(", ")
        instruction = curLine[0]
        memInst = MemoryInstruction(instruction=instruction)
        if instruction == "f":
            memInst.name = curLine[1]
            memInstArr.append(memInst)
        elif instruction == "r":
            memInst.size = curLine[1]
            memInst.name = curLine[2]
            memInst.newName = curLine[3]
            memInstArr.append(memInst)
        elif instruction == "a":
            memInst.size = curLine[1]
            memInst.name = curLine[2]
            memInstArr.append(memInst)
    return memInstArr
