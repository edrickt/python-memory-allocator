# reference: https://docs.python.org/3/library/copy.html
from implicitlistheap import ImplicitListHeap
from explicitlistheap import ExplicitListHeap
from heapitem import HeapItem
import sys

INITIAL_SIZE = 26
MAX_SIZE = 100000
IMPLICIT = "implicit"
EXPLICIT = "explicit"
FIRST_FIT = "first fit"
BEST_FIT = "best fit"

class MemoryAllocator:
    def __init__(self, listType, fitType):
        if listType == IMPLICIT:
            self.heap = ImplicitListHeap(fitType, INITIAL_SIZE)
        elif listType == EXPLICIT:
            self.heap = ExplicitListHeap(fitType, INITIAL_SIZE)

    def myalloc(self, sizeByte):
        itemToInsert = HeapItem(payloadSize=sizeByte, allocated=1, inuse=True)
        freeblock = self.heap.find_freeblock(sizeByte)
        if freeblock is not None:
            self.heap.insert_into_freeblock(itemToInsert, freeblock)
            return itemToInsert
        else:
            self.mysbrk(sizeByte)
            return self.myalloc(sizeByte)

    def myfree(self, pointer):
        block = self.heap.find_block(pointer)
        if block is not None:
            self.heap.coalesce(block)
        return None

    def myrealloc(self, pointer, sizeByte):
        foundBlock = self.heap.find_block(pointer)
        content = self.heap.copy_contents(foundBlock.headerIndex+1, foundBlock.headerIndex-1)
        newBlock = self.myalloc(sizeByte)
        if newBlock is not None:
            self.heap.paste_contents(newBlock.headerIndex+1, newBlock.headerIndex-1, content)
            self.myfree(foundBlock)
            return newBlock
        return None

    def mysbrk(self, sizeByte):
        totalSize = (sizeByte // 8 + 1) * 8 + 8
        if (totalSize / 4) + len(self.heap.heap) <= MAX_SIZE:
            self.heap.extend_heap(sizeByte)
        else:
            print("memheap.py: total heap capacity reached (maximum 100000 words)")
            sys.exit(1)
