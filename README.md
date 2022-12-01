# Python Memory Allocator
Malloc, free, realloc, and sbrk in Python

## PROGRAM GENERAL INFORMATION

Language: Python
Version: 3.9.7

## USAGE

### COMMAND LINE

Execution: ```$python3 memsim.py [-h] -o <outfile> -l <implicit or explicit> -f <first or best> -i <infile>```

### AS A PACKAGE

Simulating malloc, realloc, free, and sbrk is also possible by importing memoryallocator.py where the user is then able to perform normal memory allocation functions similar to C.

Example:

```
from memoryallocator import *

memalloc = MemoryAllocator(IMPLICIT, FIRST)
p0 = memalloc.myalloc(5)
...
```

## REFERENCES

* Copy an object in new memory
  * https://docs.python.org/3/library/copy.html
* Linked list operations
  * https://www.tutorialspoint.com/python_data_structure/python_linked_lists.htm
  
## IMPORTED LIBRARIES

* from copy import deepcopy
  * Used to copy an object instead of variable assignment

## ISSUES

No known issues
