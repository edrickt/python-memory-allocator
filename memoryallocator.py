from implicitlistheap import ImplicitListHeap
from explicitlistheap import ExplicitListHeap
from heapitem import HeapItem
import sys

# Constants
INITIAL_SIZE = 1000
MAX_SIZE = 100000
IMPLICIT = "implicit"
EXPLICIT = "explicit"
FIRST_FIT = "first"
BEST_FIT = "best"

# Memory allocater class that performs allocation and freeing
class MemoryAllocator:
    def __init__(self, listType, fitType):
        # Create heap based on list type and fit type
        if listType == IMPLICIT:
            self.heap = ImplicitListHeap(fitType, INITIAL_SIZE)
        elif listType == EXPLICIT:
            self.heap = ExplicitListHeap(fitType, INITIAL_SIZE)

    # Allocate memory in heap
    def myalloc(self, sizeByte):
        # Create a HeapItem for the item to insert
        itemToInsert = HeapItem(payloadSize=sizeByte, allocated=1, inuse=True)
        # Find the freeblock
        freeblock = self.heap.find_freeblock(sizeByte)
        # If freeblock found, insert into the freeblock
        if freeblock is not None:
            self.heap.insert_into_freeblock(itemToInsert, freeblock)
            return itemToInsert
        # Else, extend the heap and run myalloc again
        else:
            self.mysbrk(sizeByte)
            return self.myalloc(sizeByte)

    # Free the pointer in heap
    def myfree(self, pointer):
        # Find the block based on the pointer
        block = self.heap.find_block(pointer)
        # If found, then free and coalesce
        if block is not None:
            self.heap.coalesce(block)
        return None

    # Realloc a pointer in the heap
    def myrealloc(self, pointer, sizeByte):
        # Find the old pointer
        foundBlock = self.heap.find_block(pointer)
        # Get the content of the old pointer
        content = self.heap.copy_contents(foundBlock.headerIndex+1, foundBlock.footerIndex-1)
        # Allocate the new block with updated size
        newBlock = self.myalloc(sizeByte)
        # If a new block is found, then paste the old block's content into new block and free old
        # block
        if newBlock is not None:
            self.heap.paste_contents(newBlock.headerIndex+1, len(content)+newBlock.headerIndex, content)
            self.myfree(foundBlock)
            return newBlock
        return None

    # If heap is too small to accomodate an alloc, extend the heap and allocate into the newly
    # extended heap space
    def mysbrk(self, sizeByte):
        # Get the totalSize
        totalSize = HeapItem.calculate_total_size(sizeByte)
        # Extend the heap by the totalSize if it is less than our MAX_SIZE
        if (totalSize / 4) + len(self.heap.heap) <= MAX_SIZE:
            self.heap.extend_heap(sizeByte)
        else:
            print("memheap.py: total heap capacity reached (maximum 100000 words)")
            sys.exit(1)
