# Holds all command line arguments
class Arguments:
    def __init__(self, outfileString, listType, fitType, infileString):
        self.outfileString = outfileString
        self.listType = listType
        self.fitType = fitType
        self.infileString = infileString

# A data class for a memory instruction
class MemoryInstruction:
    def __init__(self, instruction=None, size=None, name=None, newName=None):
        self.instruction = instruction
        self.size = size
        self.name = name
        self.newName = newName
        