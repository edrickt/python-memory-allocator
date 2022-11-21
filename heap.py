from heapitem import HeapItem
from copy import deepcopy

INT_MAX = 999999999
FIRST_FIT = "first fit"
BEST_FIT = "best fit"

class Heap:
    def __init__(self, fitType, initialSize):
        self.fitType = fitType
        self.heap = [HeapItem()] * initialSize
        self.itemCounter = 1
        initialFreeblock = HeapItem(payloadSize=(initialSize-6)*4, allocated=0, inuse=True, headerIndex=1, footerIndex=len(self.heap)-2, name=0)
        self.insert_heap_item(initialFreeblock)
        self.root = self.heap[1]

    def insert_into_freeblock(self, heapItem, freeblock):
        return NotImplementedError

    def insert_heap_item(self, heapItem):
        return NotImplementedError

    def set_item_prev_next(self, heapItem):
        heapItem.next = self.next_adjacent_block(heapItem)
        heapItem.prev = self.prev_adjacent_block(heapItem)

    def next_adjacent_block(self, heapItem):
        for i in range(heapItem.footerIndex+1, len(self.heap)-2):
            if self.heap[i].inuse is True and self.heap[i].name != heapItem.name:
                return self.heap[i]
        return None

    def prev_adjacent_block(self, heapItem):
        return NotImplementedError

    def update_adjacent_heap_item_pointers(self, heapItem):
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
        totalSize = HeapItem.calculate_total_size(sizeByte)
        if self.fitType == FIRST_FIT:
            while curItem is not None:
                if curItem.allocated == 0 and curItem.inuse == True and curItem.totalSize >= totalSize:
                    return curItem
                curItem = curItem.next
            return None

    def find_freeblock_best_fit(self, sizeByte):
        curItem = self.root
        totalSize = HeapItem.calculate_total_size(sizeByte)
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
        for i in range(1, len(self.heap)-2):
            curItem = self.heap[i]
            if isinstance(curItem, HeapItem) is True:
                if pointer.name == curItem.name and curItem.inuse is True:
                    return curItem
        return None

    def coalesce(self, pointer):
        return NotImplementedError

    def combine_adjacent_freeblocks(self, blockA, blockB):
        return NotImplementedError

    def copy_contents(self, indexA, indexB):
        contents = []
        for i in range(indexA, indexB+1):
            copy = deepcopy(self.heap[i])
            if isinstance(copy, HeapItem):
                copy.inuse = False
            contents.append(copy)
        return contents

    def paste_contents(self, indexA, indexB, contents):
        j = 0
        for i in range(indexA, indexB+1):
            self.heap[i] = contents[j]
            j += 1

    def extend_heap(self, sizeByte):
        return NotImplementedError

    def print_heap(self):
        print(f"{0},", "0x00000000")
        # for i in range(1, len(self.heap)-1):
        for i in range(1, 25):
            heapItem = self.heap[i]
            if isinstance(heapItem, HeapItem):
                content = heapItem.headerfooter()
                if content == 0:
                    print(f"{i},")
                else:
                    print(f"{i}, 0x{content:0{8}X}")
            else:
                print(f"{i}, 0x{heapItem:0{8}X}")
        print(f"{len(self.heap)-1},", "0x00000000")
