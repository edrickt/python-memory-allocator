# Heap item class that is inserted into the heap
class HeapItem:
    def __init__(self, payloadSize=0, allocated=0, inuse=False, headerIndex=0, footerIndex=0, name=-1, prev=None, next=None):
        self.payloadSize = payloadSize
        self.allocated = allocated
        self.inuse = inuse
        self.headerIndex = headerIndex
        self.footerIndex = footerIndex
        self.name = name
        self.prev = prev
        self.next = next
        
        # Initialize totalSize based on payload amount
        self.totalSize = self.update_total_size_by_payload()

    # Updates totalSize by payload
    def update_total_size_by_payload(self):
        if self.payloadSize == 0:
            return 0
        # Calculate totalSize based on payloadSize
        totalSize = HeapItem.calculate_total_size(self.payloadSize)
        self.totalSize = totalSize
        return int(totalSize)

    # Get the heapItems header and footer
    def headerfooter(self):
        if self.payloadSize == 0:
            return 0
        headerFooter = self.totalSize | self.allocated
        return int(headerFooter)

    # Creates or updates the heapItem's footerIndex based on headerIndex and
    # totalSize of the block
    def update_footer_index(self):
        footerIndex = self.headerIndex + (self.totalSize / 4) - 1
        self.footerIndex = int(footerIndex)  

    # Update the heapItem's total size to be used when headers are changed
    def update_total_size_by_headers(self):
        words = self.footerIndex - self.headerIndex + 1
        self.totalSize = int(words * 4)

    # Static method to calculate total size
    @staticmethod
    def calculate_total_size(sizeByte):
        totalSize = ((sizeByte + 8 - 1) // 8 * 8) + 8
        return int(totalSize)
