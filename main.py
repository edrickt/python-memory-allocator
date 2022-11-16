from memoryallocator import MemoryAllocator, FIRST_FIT, BEST_FIT, IMPLICIT, EXPLICIT

if __name__ == "__main__":
    heap = MemoryAllocator(IMPLICIT, FIRST_FIT)
    p0 = heap.myalloc(1)
    p2 = heap.myalloc(1)
    p3 = heap.myalloc(1)
    heap.myfree(p3)
    p4 = heap.myalloc(1)
    heap.myfree(p2)
    p5 = heap.myalloc(1)
    heap.heap.print_heap()
