from heap import Heap
from heapitem import HeapItem
from copy import deepcopy

INT_MAX = 999999999
FIRST_FIT = "first"
BEST_FIT = "best"

class ExplicitListHeap(Heap):
    def __init__(self, fitType, initialSize):
        super().__init__(fitType, initialSize)

    def insert_into_freeblock(self, heapItem, freeblock):
        heapItem.headerIndex = freeblock.headerIndex
        heapItem.update_footer_index()

        freeblock.headerIndex = heapItem.footerIndex+1
        freeblock.update_total_size_by_headers()

        if freeblock.totalSize == 8:
            heapItem.payloadSize = int(((heapItem.totalSize-3)/4)*4)
            heapItem.update_total_size_by_payload()
            heapItem.update_footer_index()
            self.heap[heapItem.footerIndex-1] = HeapItem()
            freeblock.inuse = False
            self.delete_freeblock(freeblock)
            # why is this not committing
        elif freeblock.totalSize == 0:
            freeblock.inuse = False
            self.delete_freeblock(freeblock)
        else:
            self.heap[freeblock.headerIndex] = self.heap[freeblock.footerIndex] = freeblock

        self.insert_heap_item(heapItem)
        self.write_pointers()

    def insert_heap_item(self, heapItem):
        headerIndex = heapItem.headerIndex
        footerIndex = heapItem.footerIndex

        heapItem.inuse = True
        heapItem.name = self.itemCounter
        self.itemCounter += 1

        self.heap[headerIndex] = self.heap[footerIndex] = heapItem

    def write_pointers(self):
        curBlock = self.heap[1]
        while curBlock is not None:
            prevBlock = curBlock.prev
            nextBlock = curBlock.next
            if curBlock.allocated == 0:
                if prevBlock is not None:
                    self.heap[curBlock.headerIndex+1] = prevBlock.headerIndex
                else:
                    self.heap[curBlock.headerIndex+1] = 0
                if nextBlock is not None:
                    self.heap[curBlock.headerIndex+2] = nextBlock.headerIndex
                else:
                    self.heap[curBlock.headerIndex+2] = 0
            elif curBlock.allocated == 1:
                if isinstance(self.heap[curBlock.headerIndex+1], HeapItem) is True:
                    self.heap[curBlock.headerIndex+1] = 0
                if isinstance(self.heap[curBlock.headerIndex+2], HeapItem) is True:
                    self.heap[curBlock.headerIndex+2] = 0
            curBlock  = self.next_adjacent_block(curBlock)

    def prev_adjacent_block(self, heapItem):
        for i in range(heapItem.headerIndex-1, 1, -1):
            root = False
            if self.heap[i].inuse is True and self.heap[i].name != heapItem.name:
                return self.heap[i]
        return None

    def coalesce(self, pointer):
        prevBlock = self.prev_adjacent_block(pointer)
        nextBlock = self.next_adjacent_block(pointer)

        if prevBlock is not None and nextBlock is not None:
            if prevBlock.allocated == 1 and nextBlock.allocated == 1:
                self.push_freeblock(pointer)
            elif prevBlock.allocated == 1 and nextBlock.allocated == 0:
                self.combine_adjacent_freeblocks(pointer, nextBlock)
            elif prevBlock.allocated == 0 and nextBlock.allocated == 1:
                self.combine_adjacent_freeblocks(prevBlock, pointer)
            elif prevBlock.allocated == 0 and nextBlock.allocated == 0:
                self.combine_adjacent_freeblocks(prevBlock, nextBlock, True)
                self.write_pointers()
                self.disconnect_block(pointer, nextBlock)
                return
        else:
            if prevBlock is None and nextBlock is not None:
                if nextBlock.allocated == 1:
                    self.push_freeblock(pointer)
                elif nextBlock.allocated == 0:
                    self.combine_adjacent_freeblocks(pointer, nextBlock)
            elif prevBlock is not None and nextBlock is None:
                if prevBlock.allocated == 1:
                    self.push_freeblock(pointer)
                elif prevBlock.allocated == 0:
                    self.combine_adjacent_freeblocks(prevBlock, pointer)
            elif prevBlock is None and nextBlock is None:
                self.push_freeblock(pointer)
        self.write_pointers()

    def disconnect_block(self, pointer, newBlock):
        footerIndex = pointer.footerIndex
        headerIndex = newBlock.headerIndex
        self.heap[footerIndex+2] = self.heap[headerIndex+1]
        self.heap[footerIndex+3] = self.heap[headerIndex+2]

    def combine_adjacent_freeblocks(self, blockA, blockB, case2=False):
        contents = self.copy_contents(blockA.headerIndex+1, blockB.footerIndex-1)
        blockB.headerIndex = blockA.headerIndex
        blockB.allocated = 0
        blockB.update_total_size_by_headers()
        self.paste_contents(blockB.headerIndex+1, blockB.footerIndex-1, contents)
        self.push_freeblock_to_freelist(blockA, blockB)
        self.insert_heap_item(blockB)

    def push_freeblock_to_freelist(self, blockA, blockB):
        self.delete_freeblock(blockA)
        self.delete_freeblock(blockB)
        self.push_freeblock(blockB)

    def delete_freeblock(self, block):
        if self.root is None or block is None:
            return
        if self.root == block:
            self.root = block.next
        if block.next is not None:
            block.next.prev = block.prev
        if block.prev is not None:
            block.prev.next = block.next

    def push_freeblock(self, block):
        block.allocated = 0
        block.prev = None
        block.next = self.root
        if self.root is not None:
            self.root.prev = block
        self.root = block

    def extend_heap(self, sizeByte):
        totalSize = HeapItem.calculate_total_size(sizeByte)
        heapExtension = [HeapItem()] * int((totalSize/4)+1)
        headerIndex = len(self.heap)-1
        self.heap.pop()
        self.heap.extend(heapExtension)
        newFreeblock = HeapItem(payloadSize=sizeByte, 
                                allocated=0, 
                                inuse=True, 
                                headerIndex=headerIndex,
                                name=self.itemCounter)
        self.itemCounter += 1
        newFreeblock.update_footer_index()
        self.push_freeblock(newFreeblock)
        self.insert_heap_item(newFreeblock)
