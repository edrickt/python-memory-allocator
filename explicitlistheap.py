from heap import Heap
from heapitem import HeapItem
from copy import deepcopy

INT_MAX = 999999999
FIRST_FIT = "first fit"
BEST_FIT = "best fit"

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
        elif freeblock.totalSize == 0:
            freeblock.inuse = False
        else:
            self.heap[freeblock.headerIndex] = self.heap[freeblock.footerIndex] = freeblock

        self.insert_heap_item(heapItem, freeblock)

    def insert_heap_item(self, heapItem, freeblock):
        headerIndex = heapItem.headerIndex
        footerIndex = heapItem.footerIndex

        heapItem.inuse = True
        heapItem.name = self.itemCounter
        self.itemCounter += 1

        self.heap[headerIndex] = self.heap[footerIndex] = heapItem
        self.insert_item_at_root(freeblock)

    def insert_item_at_root(self, heapItem):
        pass

    def find_freeblock(self, sizeByte):
        if self.fitType == FIRST_FIT:
            return self.find_freeblock_first_fit(sizeByte)
        elif self.fitType == BEST_FIT:
            return self.find_freeblock_best_fit(sizeByte)

# stop notes: find freeblocks shouldnt need to be changed since they
# iterate from root of only freeblock list only.

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
        for i in range(0, len(self.heap)):
            curItem = self.heap[i]
            if pointer.name == curItem.name and curItem.inuse is True:
                return curItem
        return None

# stop note: case 1 will need to insert the freeblock at root
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

# stop note: will need to insert the freeblock at root
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

# stop note: may need to step through inserting heap item of freeblock
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
            content = heapItem.headerfooter()
            if heapItem.headerfooter() == 0:
                print(f"{i},")
            else:
                print(f"{i}, 0x{content:0{8}X}")
