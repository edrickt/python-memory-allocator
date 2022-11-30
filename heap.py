# reference: https://docs.python.org/3/library/copy.html
# reference: https://www.tutorialspoint.com/python_data_structure/python_linked_lists.htm
from heapitem import HeapItem
from copy import deepcopy

# Contents
INT_MAX = 999999999
FIRST_FIT = "first"
BEST_FIT = "best"

# Parent heap class that implicit and explicit list heap inherits from
class Heap:
    def __init__(self, fitType, initialSize):
        self.fitType = fitType
        # Initialize heap with empty HeapItems
        self.heap = [HeapItem()] * initialSize
        # Used to give unique names to each new pointer
        self.itemCounter = 1
        # Create first initial freeblock and insert into the heap
        initialFreeblock = HeapItem(payloadSize=(initialSize-5)*4, allocated=0, inuse=True, headerIndex=1, footerIndex=len(self.heap)-2, name=0)
        self.insert_heap_item(initialFreeblock)
        # Set the first freeblock as the root
        self.root = self.heap[1]

    # Implemented by ExplicitListHeap and ImplicitListHeap
    def insert_into_freeblock(self, heapItem, freeblock):
        return NotImplementedError

    # Implemented by ExplicitListHeap and ImplicitListHeap
    def insert_heap_item(self, heapItem):
        return NotImplementedError

    # Set the heapItem's previous and next block based off adjacent blocks
    def set_item_prev_next(self, heapItem):
        heapItem.next = self.next_adjacent_block(heapItem)
        heapItem.prev = self.prev_adjacent_block(heapItem)

    # Get next adjacent block from heapItem
    def next_adjacent_block(self, heapItem):
        for i in range(heapItem.footerIndex+1, len(self.heap)-2):
            if self.heap[i].inuse is True and self.heap[i].name != heapItem.name:
                return self.heap[i]
        return None

    # Implemented by ExplicitListHeap and ImplicitListHeap
    def prev_adjacent_block(self, heapItem):
        return NotImplementedError

    # Set the adjacent blocks to point to heapItem
    def update_adjacent_heap_item_pointers(self, heapItem):
        if heapItem.prev is not None:
            prevItem = heapItem.prev
            prevItem.next = heapItem
        if heapItem.next is not None:
            nextItem = heapItem.next
            nextItem.prev = heapItem

    # Find freeblock based on fitType
    def find_freeblock(self, sizeByte):
        if self.fitType == FIRST_FIT:
            return self.find_freeblock_first_fit(sizeByte)
        elif self.fitType == BEST_FIT:
            return self.find_freeblock_best_fit(sizeByte)
            
    # Find freeblock by iterating through heapItem's next blocks
    def find_freeblock_first_fit(self, sizeByte):
        curItem = self.root
        totalSize = HeapItem.calculate_total_size(sizeByte)
        # While not the end of the heap, keep finding the freeblock that is big enough to
        # accomodate allocation
        while curItem is not None:
            if curItem.allocated == 0 and curItem.inuse == True and curItem.totalSize >= totalSize:
                return curItem
            curItem = curItem.next
        return None

    # Find the freeblock that best fits allocation
    def find_freeblock_best_fit(self, sizeByte):
        curItem = self.root
        totalSize = HeapItem.calculate_total_size(sizeByte)
        min = INT_MAX
        found = None
        while curItem is not None:
            if curItem.allocated == 0 and curItem.inuse == True and curItem.totalSize >= totalSize:
                # If min is bigger than current item's total size, update the minimum
                if min > curItem.totalSize:
                    min = curItem.totalSize
                    found = curItem
            curItem = curItem.next
        # If we found a block, return it
        if found is not None:
            return found
        return None

    # Find block by name through linear search of the heap
    def find_block(self, pointer):
        for i in range(1, len(self.heap)-2):
            curItem = self.heap[i]
            if isinstance(curItem, HeapItem) is True:
                # If pointer matches, return it
                if pointer.name == curItem.name and curItem.inuse is True:
                    return curItem
        return None

    # Implemented by ExplicitListHeap and ImplicitListHeap
    def coalesce(self, pointer):
        return NotImplementedError

    # Implemented by ExplicitListHeap and ImplicitListHeap
    def combine_adjacent_freeblocks(self, blockA, blockB):
        return NotImplementedError

    # Copy contents of heap from indexA and indexB
    def copy_contents(self, indexA, indexB):
        contents = []
        for i in range(indexA, indexB+1):
            # Use deepcopy to create new items in memory, not references
            copy = deepcopy(self.heap[i])
            # If it is a HeapItem, set it as not in use
            if isinstance(copy, HeapItem):
                copy.inuse = False
            # Add to array
            contents.append(copy)
        return contents

    # Paste the contents in the specified index ranges
    def paste_contents(self, indexA, indexB, contents):
        j = 0
        for i in range(indexA, indexB+1):
            self.heap[i] = contents[j]
            j += 1

    # Implemented by ExplicitListHeap and ImplicitListHeap
    def extend_heap(self, sizeByte):
        return NotImplementedError

    # Return the heap as a string
    def get_simulation_results(self):
        string = ""
        num = len(self.heap)-1
        # Placeholder
        string += f"{0}, " + "0x00000001\n"
        # Iterate through heap
        for i in range(1, num):
            # Set heapItem
            heapItem = self.heap[i]
            # If it is not a pointer
            if isinstance(heapItem, HeapItem):
                # Get the header and footer and add it to the string
                content = heapItem.headerfooter()
                if content == 0:
                    string += f"{i},\n"
                else:
                    string += f"{i}, 0x{content:0{8}X}\n"
            else:
                string += f"{i}, 0x{heapItem:0{8}X}\n"
        # Placeholder
        string += f"{len(self.heap)-1}, " + "0x00000001\n"
        return string

    # USED FOR TESTING PURPOSED ONLY. Prints the heap
    def print_heap(self, num=None):
        if num is None:
            num = len(self.heap)-1
        # Placeholder
        print(f"{0},", "0x00000001")
        for i in range(1, num):
            # Set heapItem
            heapItem = self.heap[i]
            # If it is not a pointer
            if isinstance(heapItem, HeapItem):
                # Get the header and footer and add it to the string
                content = heapItem.headerfooter()
                if content == 0:
                    print(f"{i},")
                else:
                    print(f"{i}, 0x{content:0{8}X}")
            else:
                print(f"{i}, 0x{heapItem:0{8}X}")
        # Placeholder
        print(f"{len(self.heap)-1},", "0x00000001")
