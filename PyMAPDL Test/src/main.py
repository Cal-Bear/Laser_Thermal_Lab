import numpy as np
import math 
from ansys.mapdl.core import launch_mapdl
from block import *
from ansys_functions import *
from block_matrix import *
import sys

def main():

    shape_dict = {'c' : create_wire_cube,
                  'x' : create_wire_cross,
                  'p' : print_op,
                  'e' :  no_op}

    print("Starting main...")

    #Create mapdl Object
    mapdl = launch_mapdl()
    mapdl.clear()

    # Define units and material details
    define_units(mapdl)
    
    # Read file and define matrix
    read_matrix = read_file(sys.argv)
    print("Matrix loaded:", read_matrix, "\n")
    mat = block_matrix(read_matrix, 'f')

    # Construct the mapdl volume from the patrix
    print("reading matrix...", "\n")
    mat.construct_matrix(mapdl, merge_volume, shape_dict)
    merge_all(mapdl) # one final merge, just in case

    # Print an area plot of the volume
    print("printing...")
    mapdl.aplot()

    # Mesh volume
    print("meshing...")
    mesh_volume(mapdl)


def read_file(arg):
    if len(arg) == 1: 
        # Default value return if no file given
        print('Using default matrix')
        return [[['p', 'p'], 
                 ['p', 'p']],

                [['p', 'p'], 
                 ['p', 'p']]]
    else:
        # Read designated file
        file_name = arg[1]
        try:
            f = open(file_name, "r")
        except FileNotFoundError:
            print("Invalid file name... Program aborting")
            quit()

        ret = []
        file_string = f.read().replace(" ", "")
        array_2d = [subl.split("\n") for subl in file_string.split("\n-\n") ]
        for subl in array_2d:
            ret.append([sub.split(",") for sub in subl])

        return ret


if __name__ == "__main__":
    main()



