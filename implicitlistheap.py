from heap import Heap
from heapitem import HeapItem

# Implicit list heap class that inherits from Heap Class
class ImplicitListHeap(Heap):
    def __init__(self, fitType, initialSize):
        # Initialize parent class self variables
        super().__init__(fitType, initialSize)

    # Insert the heapItem into a freeblock
    def insert_into_freeblock(self, heapItem, freeblock):
        # heapItem will have the headerIndex of the freeblock
        heapItem.headerIndex = freeblock.headerIndex
        # Update footerIndex based on headerIndex and size
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
            # Update totalSize given new payload
            heapItem.update_total_size_by_payload()
            # Update footerIndex by new payloadSize
            heapItem.update_footer_index()
            # Remove old header of freeblock
            self.heap[heapItem.footerIndex-1] = HeapItem()
        # If the freeblock is taken entirely up by the heapitem, set to unused
        elif freeblock.totalSize == 0:
            freeblock.inuse = False
        # Else, add the new freeblock with new headers and footers
        else:
            self.heap[freeblock.headerIndex] = self.heap[freeblock.footerIndex] = freeblock

        # Insert heapItem at its headerIndex and footerIndex
        self.insert_heap_item(heapItem)

    # Insert heapItem into heap
    def insert_heap_item(self, heapItem):
        headerIndex = heapItem.headerIndex
        footerIndex = heapItem.footerIndex

        # Set heapItem to be inuse, name it, and increment the itemCounter for naming
        heapItem.inuse = True
        heapItem.name = self.itemCounter
        self.itemCounter += 1

        # Insert into heap and set the heapItem's adjacent blocks, then make those 
        # items point to heapItem
        self.heap[headerIndex] = self.heap[footerIndex] = heapItem
        self.set_item_prev_next(heapItem)
        self.update_adjacent_heap_item_pointers(heapItem)

    # Get previous adjacent blocks, set root to heapItem if it is at the beginning of the
    # heap
    def prev_adjacent_block(self, heapItem):
        root = True
        for i in range(heapItem.headerIndex-1, 1, -1):
            root = False
            if self.heap[i].inuse is True and self.heap[i].name != heapItem.name:
                return self.heap[i]
        if root is True:
            self.root = heapItem
        return None

    # Coalesce freeblocks based on different cases
    def coalesce(self, heapItem):
        # Get previous and next blocks
        prevBlock = heapItem.prev
        nextBlock = heapItem.next

        # If the previous and next blocks are none, then create a dummy HeapItem 
        # that is allocated       
        if prevBlock is None:
            prevBlock = HeapItem(allocated=1)
        if nextBlock is None:
            nextBlock = HeapItem(allocated=1)

        # Determine coalescing based on different cases
        # If prev and next blocks are allocated, deallocate current block
        if prevBlock.allocated == 1 and nextBlock.allocated == 1:
            heapItem.allocated = 0
            return
        # If prev block allocated and next block not, coalesce current and next block
        elif prevBlock.allocated == 1 and nextBlock.allocated == 0:
            self.combine_adjacent_freeblocks(heapItem, nextBlock)
            return
        # If prev block not allocated and next block is, coalesce prev and current block
        elif prevBlock.allocated == 0 and nextBlock.allocated == 1:
            self.combine_adjacent_freeblocks(prevBlock, heapItem)
            return
        # If both adjacent blocks unallocated, then coalesce all three
        elif prevBlock.allocated == 0 and nextBlock.allocated == 0:
            self.combine_adjacent_freeblocks(prevBlock, nextBlock)
            return

    # Will combine two adjacent freeblocks. Copying and pasting the content is done
    # so that the items in the freeblock are set to unused
    def combine_adjacent_freeblocks(self, blockA, blockB):
        # Copy the contents from blockA to blockB
        contents = self.copy_contents(blockA.headerIndex+1, blockB.footerIndex-1)
        # Assign attributes and update totalSize
        blockB.headerIndex = blockA.headerIndex
        blockB.allocated = 0
        blockB.update_total_size_by_headers()
        # Paste the content in the newly coalesced block and insert back into the heap as free
        self.paste_contents(blockB.headerIndex+1, blockB.footerIndex-1, contents)
        self.insert_heap_item(blockB)

    # Used for mysbrk to extend the heap given sizeByte
    def extend_heap(self, sizeByte):
        # Calculate the totalSize
        totalSize = HeapItem.calculate_total_size(sizeByte)
        # Initialize the heap extension with empty HeapItems
        heapExtension = [HeapItem()] * int((totalSize/4)+1)
        # Set the headerIndex to be at the end of the old heap
        headerIndex = len(self.heap)-1

        # Remove the placeholder on the old heap then extend it by the new heap extension
        self.heap.pop()
        self.heap.extend(heapExtension)
        # Create a new freeblock to be put where the heap was extended
        newFreeblock = HeapItem(payloadSize=sizeByte, 
                                allocated=0, 
                                inuse=True, 
                                headerIndex=headerIndex)

        # Update the footer index by the totalSize, push into the freeblock, insert it into the
        # freeblock
        newFreeblock.update_footer_index()
        self.insert_heap_item(newFreeblock)
        