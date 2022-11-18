from memoryallocator import MemoryAllocator, FIRST_FIT, BEST_FIT, IMPLICIT, EXPLICIT

if __name__ == "__main__":
    heap = MemoryAllocator(EXPLICIT, FIRST_FIT)
    p0 = heap.myalloc(1)
    heap.myfree(p0)
    p1 = heap.myalloc(1)
    p2 = heap.myalloc(1)
    heap.heap.print_heap()
    print()
