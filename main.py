from memoryallocator import MemoryAllocator, FIRST_FIT, BEST_FIT, IMPLICIT, EXPLICIT
from helperfunctions import *

if __name__ == "__main__":
    heap = MemoryAllocator(EXPLICIT, FIRST_FIT)
    # p0 = heap.myalloc(5)
    # heap.myfree(p0)
    # p1 = heap.myalloc(10)
    # p2 = heap.myrealloc(p1, 20)
    # heap.heap.print_heap(20)
    # print()
    # heap.myfree(p2)
    # heap.heap.print_heap(20)
    p0 = heap.myalloc(5)
    p1 = heap.myalloc(5)
    p2 = heap.myalloc(5)
    p3 = heap.myalloc(5)
    p4 = heap.myalloc(5)
    heap.myfree(p1)
    heap.myfree(p3)
    heap.heap.print_heap(25)
    print()
    heap.myfree(p2)
    heap.heap.print_heap(25)
