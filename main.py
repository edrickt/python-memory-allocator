from memoryallocator import MemoryAllocator, FIRST_FIT, BEST_FIT, IMPLICIT, EXPLICIT
from helperfunctions import *

if __name__ == "__main__":
    heap = MemoryAllocator(EXPLICIT, FIRST_FIT)
    p0 = heap.myalloc(5)
    heap.myfree(p0)
    p1 = heap.myalloc(10)
    p2 = heap.myrealloc(p1, 20)
    heap.myfree(p2)
    heap.heap.print_heap()
