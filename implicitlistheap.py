from heapitem import HeapItem
from copy import deepcopy

INITIAL_SIZE = 8
MAX_SIZE = 100000
INT_MAX = 999999999
FIRST_FIT = "first fit"
BEST_FIT = "best fit"

class ImplicitListHeap:
    def __init__(self, fitType):
        self.fitType = fitType
        self.heap = [HeapItem()] * INITIAL_SIZE
        self.itemCounter = 1
        initialFreeblock = HeapItem(payloadSize=(INITIAL_SIZE-6)*4, allocated=0, inuse=True, headerIndex=1, footerIndex=len(self.heap)-2, name=0)
        self.insert_heap_item(initialFreeblock)
        self.root = self.heap[1]

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

        self.update_adjacent_heapItem_pointers(heapItem)

    def set_item_prev_next(self, heapItem):
        heapItem.next = self.next_adjacent_block(heapItem)
        heapItem.prev = self.prev_adjacent_block(heapItem)

    def next_adjacent_block(self, heapItem):
        for i in range(heapItem.footerIndex+1, len(self.heap)-2):
            if self.heap[i].inuse is True and self.heap[i].name != heapItem.name:
                return self.heap[i]
        return None

    def prev_adjacent_block(self, heapItem):
        root = True
        for i in range(heapItem.headerIndex-1, 1, -1):
            root = False
            if self.heap[i].inuse is True and self.heap[i].name != heapItem.name:
                return self.heap[i]
        if root is True:
            self.root = heapItem
        return None

    def update_adjacent_heapItem_pointers(self, heapItem):
        if heapItem.prev is not None:
            prevItem = heapItem.prev
            prevItem.next = heapItem
        if heapItem.next is not None:
            nextItem = heapItem.next
            nextItem.prev = heapItem

    def find_freeblock(self, sizeByte):
        if self.fitType == FIRST_FIT:
            return self.find_freeblock_first_fit(sizeByte)
        elif self.fitType == BEST_FIT:
            return self.find_freeblock_best_fit(sizeByte)
            
    def find_freeblock_first_fit(self, sizeByte):
        curItem = self.root
        totalSize = (sizeByte // 8 + 1) * 8 + 8
        if self.fitType == FIRST_FIT:
            while curItem is not None:
                if curItem.allocated == 0 and curItem.inuse == True and curItem.totalSize >= totalSize:
                    return curItem
                curItem = curItem.next
            return None

    def find_freeblock_best_fit(self, sizeByte):
        curItem = self.root
        totalSize = (sizeByte // 8 + 1) * 8 + 8
        min = INT_MAX
        found = None
        while curItem is not None:
            if curItem.allocated == 0 and curItem.inuse == True and curItem.totalSize >= totalSize:
                if min > curItem.totalSize:
                    min = curItem.totalSize
                    found = curItem
            curItem = curItem.next
        if found is not None:
            return found
        return None

    def find_block(self, pointer):
        name = pointer.name
        curItem = self.root
        while curItem is not None:
            if curItem.name == name and curItem.inuse is True and curItem.allocated == 1:
                return curItem
            curItem = curItem.next
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

    def copy_contents(self, indexA, indexB):
        contents = []
        for i in range(indexA, indexB+1):
            copy = deepcopy(self.heap[i])
            copy.inuse = False
            contents.append(copy)
        return contents

    def paste_contents(self, indexA, indexB, contents):
        j = 0
        for i in range(indexA, indexB+1):
            self.heap[i] = contents[j]
            j += 1

    def extend_heap(self, sizeByte):
        totalSize = (sizeByte // 8 + 1) * 8 + 8
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

    def print_heap(self):
        for i in range(0, len(self.heap)):
            heapItem = self.heap[i]
            if heapItem.headerfooter() == 0:
                print(f"{i},")
            else:
                print(f"{i},", hex(heapItem.headerfooter()))