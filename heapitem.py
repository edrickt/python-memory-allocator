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

        self.totalSize = self.update_total_size_by_payload()

    def update_total_size_by_payload(self):
        if self.payloadSize == 0:
            return 0
        totalSize = ((self.payloadSize + 8 - 1) // 8 * 8) + 8
        self.totalSize = totalSize
        return int(totalSize)

    def headerfooter(self):
        if self.payloadSize == 0:
            return 0
        headerFooter = self.totalSize | self.allocated
        return int(headerFooter)

    def update_footer_index(self):
        footerIndex = self.headerIndex + (self.totalSize / 4) - 1
        self.footerIndex = int(footerIndex)  

    def update_total_size_by_headers(self):
        words = self.footerIndex - self.headerIndex + 1
        self.totalSize = int(words * 4)
