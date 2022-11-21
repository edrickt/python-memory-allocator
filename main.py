from memoryallocator import MemoryAllocator, FIRST_FIT, BEST_FIT, IMPLICIT, EXPLICIT
from helperfunctions import *

if __name__ == "__main__":
    heap = MemoryAllocator(EXPLICIT, FIRST_FIT)
    p0 = heap.myalloc(10)
    p1 = heap.myalloc(1)
    p2 = heap.myalloc(5)
    heap.myfree(p0)
    heap.myfree(p2)
    p3 = heap.myalloc(5)
    heap.heap.print_heap()
