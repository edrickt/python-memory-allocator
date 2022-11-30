from heap import Heap
from heapitem import HeapItem

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
            # Update totalSize given new payload
            heapItem.update_total_size_by_payload()
            # Update footerIndex by new payloadSize
            heapItem.update_footer_index()
            # Remove old header of freeblock
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

    # Insert heapItem into heap
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

    # Coalesce freeblocks based on different cases
    def coalesce(self, heapItem):
        # Get previous and next blocks
        prevBlock = self.prev_adjacent_block(heapItem)
        nextBlock = self.next_adjacent_block(heapItem)

        # If the previous and next blocks are none, then create a dummy HeapItem 
        # that is allocated
        if prevBlock is None:
            prevBlock = HeapItem(allocated=1)
        if nextBlock is None:
            nextBlock = HeapItem(allocated=1)

        # Determine coalescing based on different cases
        # If prev and next blocks are allocated, push the current block as freeblock
        if prevBlock.allocated == 1 and nextBlock.allocated == 1:
            self.push_freeblock(heapItem)
        # If prev allocated and next not, coalesce current and next block
        elif prevBlock.allocated == 1 and nextBlock.allocated == 0:
            self.combine_adjacent_freeblocks(heapItem, nextBlock)
        # if prev is not allocated and next allocated, coalesce prev and current block
        elif prevBlock.allocated == 0 and nextBlock.allocated == 1:
            self.combine_adjacent_freeblocks(prevBlock, heapItem)
        # else both prev and next are not allocated, coalesce all 3
        elif prevBlock.allocated == 0 and nextBlock.allocated == 0:
            self.combine_adjacent_freeblocks(prevBlock, nextBlock)
            self.write_pointers()
            self.disconnect_block(heapItem, nextBlock)
            return
        self.write_pointers()

    # Pointers from old block in middle will need to be removed to simulate
    # removal of pointers
    def disconnect_block(self, heapItem, newBlock):
        footerIndex = heapItem.footerIndex
        headerIndex = newBlock.headerIndex
        self.heap[footerIndex+2] = self.heap[headerIndex+1]
        self.heap[footerIndex+3] = self.heap[headerIndex+2]

    # Will combine two adjacent freeblocks. Copying and pasting the content is done
    # so that the items in the freeblock are set to unused
    def combine_adjacent_freeblocks(self, blockA, blockB):
        # Copy the contents from blockA to blockB
        contents = self.copy_contents(blockA.headerIndex+1, blockB.footerIndex-1)
        # Assign attributes and update totalSize
        blockB.headerIndex = blockA.headerIndex
        blockB.allocated = 0
        blockB.update_total_size_by_headers()
        # Paste the content in the newly coalesced block
        self.paste_contents(blockB.headerIndex+1, blockB.footerIndex-1, contents)

        # Push freeblock into the freelist and insert it into the heap
        self.push_freeblock_to_freelist(blockA, blockB)
        self.insert_heap_item(blockB)

    # Push the freeblock into the freelist by deleting both coalesced freeblocks
    # and then pushing the new block to the top of the stack
    def push_freeblock_to_freelist(self, blockA, blockB):
        self.delete_freeblock(blockA)
        self.delete_freeblock(blockB)
        self.push_freeblock(blockB)

    # Delete freeblock from the stack
    def delete_freeblock(self, block):
        if self.root is None or block is None:
            return
        if self.root == block:
            self.root = block.next
        if block.next is not None:
            block.next.prev = block.prev
        if block.prev is not None:
            block.prev.next = block.next

    # Push freeblock to the front of the stack
    def push_freeblock(self, block):
        block.allocated = 0
        block.prev = None
        block.next = self.root
        if self.root is not None:
            self.root.prev = block
        self.root = block

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
                                headerIndex=headerIndex,
                                name=self.itemCounter)
        self.itemCounter += 1
        
        # Update the footer index by the totalSize, push into the freeblock, insert it into the
        # freeblock
        newFreeblock.update_footer_index()
        self.push_freeblock(newFreeblock)
        self.insert_heap_item(newFreeblock)
