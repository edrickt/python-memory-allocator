from heap import Heap

INT_MAX = 999999999
FIRST_FIT = "first fit"
BEST_FIT = "best fit"

class ExplicitListHip(Heap):
    def __init__(self, fitType, initialSize):
        super().__init__(fitType, initialSize)
