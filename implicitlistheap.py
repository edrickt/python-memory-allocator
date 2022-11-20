from heap import Heap
from heapitem import HeapItem
from copy import deepcopy

INT_MAX = 999999999
FIRST_FIT = "first fit"
BEST_FIT = "best fit"

class ImplicitListHeap(Heap):
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
        elif freeblock.totalSize == 0:
            freeblock.inuse = False
        else:
            self.heap[freeblock.headerIndex] = self.heap[freeblock.footerIndex] = freeblock

        self.insert_heap_item(heapItem)

    def insert_heap_item(self, heapItem):
        headerIndex = heapItem.headerIndex
        footerIndex = heapItem.footerIndex

        heapItem.inuse = True
        heapItem.name = self.itemCounter
        self.itemCounter += 1

        self.heap[headerIndex] = self.heap[footerIndex] = heapItem
        self.set_item_prev_next(heapItem)

        self.update_adjacent_heap_item_pointers(heapItem)

    def prev_adjacent_block(self, heapItem):
        root = True
        for i in range(heapItem.headerIndex-1, 1, -1):
            root = False
            if self.heap[i].inuse is True and self.heap[i].name != heapItem.name:
                return self.heap[i]
        if root is True:
            self.root = heapItem
        return None

    def coalesce(self, pointer):
        prevBlock = pointer.prev
        nextBlock = pointer.next

        if prevBlock is not None and nextBlock is not None:
            if prevBlock.allocated == 1 and nextBlock.allocated == 1:
                pointer.allocated = 0
                return
            elif prevBlock.allocated == 1 and nextBlock.allocated == 0:
                self.combine_adjacent_freeblocks(pointer, nextBlock)
                return
            elif prevBlock.allocated == 0 and nextBlock.allocated == 1:
                self.combine_adjacent_freeblocks(prevBlock, pointer)
                return
            elif prevBlock.allocated == 0 and nextBlock.allocated == 0:
                self.combine_adjacent_freeblocks(prevBlock, nextBlock)
                return
        else:
            if prevBlock is None and nextBlock is not None:
                if nextBlock.allocated == 1:
                    pointer.allocated = 0
                    return
                elif nextBlock.allocated == 0:
                    self.combine_adjacent_freeblocks(pointer, nextBlock)
                    return
            elif prevBlock is not None and nextBlock is None:
                if prevBlock.allocated == 1:
                    pointer.allocated = 0
                    return
                elif prevBlock.allocated == 0:
                    self.combine_adjacent_freeblocks(prevBlock, pointer)
                    return
            elif prevBlock is None and nextBlock is None:
                pointer.allocated = 0
                return

    def combine_adjacent_freeblocks(self, blockA, blockB):
        contents = self.copy_contents(blockA.headerIndex+1, blockB.footerIndex-1)
        blockB.headerIndex = blockA.headerIndex
        blockB.allocated = 0
        blockB.update_total_size_by_headers()
        self.paste_contents(blockB.headerIndex+1, blockB.footerIndex-1, contents)
        self.insert_heap_item(blockB)

    def extend_heap(self, sizeByte):
        totalSize = HeapItem.calculate_total_size(sizeByte)
        heapExtension = [HeapItem()] * int((totalSize/4)+1)
        headerIndex = len(self.heap)-1
        self.heap.pop()
        self.heap.extend(heapExtension)
        newFreeblock = HeapItem(payloadSize=sizeByte, 
                                allocated=0, 
                                inuse=True, 
                                headerIndex=headerIndex)
        newFreeblock.update_footer_index()
        self.insert_heap_item(newFreeblock)
        