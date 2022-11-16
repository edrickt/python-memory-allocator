from memoryallocator import MemoryAllocator, FIRST_FIT, BEST_FIT

if __name__ == "__main__":
    heap = MemoryAllocator(FIRST_FIT)
    p0 = heap.myalloc(1)
    p1 = heap.myalloc(1)
    p2 = heap.myrealloc(p0, 17)
    heap.heap.print_heap()
