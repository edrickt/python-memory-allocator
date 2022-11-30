from heap import Heap
from heapitem import HeapItem

# Constants
INT_MAX = 999999999
FIRST_FIT = "first"
BEST_FIT = "best"

# Explicit list heap class that inherits from Heap class
class ExplicitListHeap(Heap):
    def __init__(self, fitType, initialSize):
        # Initialize variables from parent class and write pointer for new
        # first freeblock
        super().__init__(fitType, initialSize)
        self.write_pointers()

    # Function to insert heapItem into freeblock
    def insert_into_freeblock(self, heapItem, freeblock):
        # heapItem will have the headerIndex of the freeblock
        heapItem.headerIndex = freeblock.headerIndex
        # Update the footerIndex calculated from headerIndex and size
        heapItem.update_footer_index()

        # Header of freeblock will be index after footer of heapItem
        freeblock.headerIndex = heapItem.footerIndex+1
        # Update new size of frebelock after new heapItem
        freeblock.update_total_size_by_headers()

        # If the freeblock now only consists of the two pointers, make the
        # heapItem occupy the remaining two words
        if freeblock.totalSize == 8:
            # Update payloadSize to occupy next two blocks
            heapItem.payloadSize = int(((heapItem.totalSize-3)/4)*4)
            # Update totalSize given new payLoad
            heapItem.update_total_size_by_payload()
            # Update footerIndex by new payloadSize
            heapItem.update_footer_index()
            # Remove old freeblock header
            self.heap[heapItem.footerIndex-1] = HeapItem()
            # Set freeblock to not be inuse and delete the freeblock
            freeblock.inuse = False
            self.delete_freeblock(freeblock)
        # If the freeblock is taken entirely up by the heapitem, delete it
        elif freeblock.totalSize == 0:
            freeblock.inuse = False
            self.delete_freeblock(freeblock)
        # Else, add the new freeblock with new headers and footers
        else:
            self.heap[freeblock.headerIndex] = self.heap[freeblock.footerIndex] = freeblock

        # Insert the heapItem at the headerIndex and footerIndex
        self.insert_heap_item(heapItem)
        # Write the pointers for freeblocks
        self.write_pointers()

    # Insert heapItem given the headerIndex and footerIndex
    def insert_heap_item(self, heapItem):
        headerIndex = heapItem.headerIndex
        footerIndex = heapItem.footerIndex

        # Set the heapItem to inuse, name it given the itemCounter and
        # increment the itemCounter
        heapItem.inuse = True
        heapItem.name = self.itemCounter
        self.itemCounter += 1

        # insert into heap
        self.heap[headerIndex] = self.heap[footerIndex] = heapItem

    # Write the pointers for the freeblocks
    def write_pointers(self):
        # Set the current block to the beginning of the heap
        curBlock = self.root
        # While not at the end of the heap items, keep iterating through them
        # and writing pointers
        while curBlock is not None:
            prevBlock = curBlock.prev
            nextBlock = curBlock.next
            
            # If there is a previous freeblock, then write pointer, else write 0
            # since there is no pointer. Do same for nextBlock
            if prevBlock is not None:
                self.heap[curBlock.headerIndex+1] = prevBlock.headerIndex
            else:
                self.heap[curBlock.headerIndex+1] = 0
            if nextBlock is not None:
                self.heap[curBlock.headerIndex+2] = nextBlock.headerIndex
            else:
                self.heap[curBlock.headerIndex+2] = 0

            curBlock  = curBlock.next

    # Get previous adjacent block to heapItem
    def prev_adjacent_block(self, heapItem):
        # Iterate backwards from heapItem headerIndex
        for i in range(heapItem.headerIndex-1, 1, -1):
            # If the heapItem is inuse and is not the same block, then return it
            if self.heap[i].inuse is True and self.heap[i].name != heapItem.name:
                return self.heap[i]
        return None

    def coalesce(self, pointer):
        prevBlock = self.prev_adjacent_block(pointer)
        nextBlock = self.next_adjacent_block(pointer)

        if prevBlock is None:
            prevBlock = HeapItem(allocated=1)
        if nextBlock is None:
            nextBlock = HeapItem(allocated=1)

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
