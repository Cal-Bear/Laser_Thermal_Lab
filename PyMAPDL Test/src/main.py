import numpy as np
import math 
from ansys.mapdl.core import launch_mapdl
from block import *
from ansys_functions import *
from block_matrix import *
import sys



def main():
    print("Starting main...")
    
    read_matrix = read_file(sys.argv)
    print(read_matrix)
    a = block_matrix(read_matrix)
    a.print_short()
    a.print_full()


    print(str(sys.argv))

def read_file(arg):
    if len(arg) == 1: 
        # Default value return if no file given
        return [[['a', 'b'], 
                 ['c', 'd']],

                [['e', 'f'], 
                 ['g', 'h']]]
    else:
        # Read designated file
        file_name = arg[1]
        try:
            f = open(file_name, "r")
        except FileNotFoundError:
            print("Invalid file name... Program aborting")
            quit()

        ret = []
        array_2d = [subl.split("\n") for subl in f.read().split("\n-\n") ]
        for subl in array_2d:
            ret.append([sub.split(" ") for sub in subl])

        return ret


if __name__ == "__main__":
    main()



