import numpy as np
import math 
from ansys.mapdl.core import launch_mapdl
from create_entity import *
# from entity_matrix import *


#    +-----------------------------------------------------+
#    |                                                     |
#    |                 Main Function                       |
#    |                                                     |
#    +-----------------------------------------------------+

def main():
    # Create mapdl Object
    mapdl = launch_mapdl()
    mapdl.clear()

    # Define units and material details
    define_units(mapdl)

    r0 = create_wire_cube(mapdl, [0, 0, 0], 20)

    r1 = create_wire_cube(mapdl, [20, 0, 0], 20)
    merge_volume(mapdl, r1)

    r2 = create_wire_cube(mapdl, [0, 0, 20], 20)
    merge_volume(mapdl, r2)

    r3 = create_wire_cube(mapdl, [20, 0, 20], 20)
    merge_volume(mapdl, r3)



    print("printing...")
    mapdl.aplot()


    mesh_volume(mapdl)

    
    print("done")

def map_coordinate(i):
    cx = i[0]
    cy = i[1]
    cz = i[2]

    fact = 20 + (2*1.5)

    return [cx*fact, cy*fact, cz*fact]

def define_units(mapdl):
    print("Defining units... ")

    # This example will use SI units.
    mapdl.prep7()
    mapdl.units("SI")  # SI - International system (m, kg, s, K).

    # Define a material (nominal steel in SI)
    mapdl.mp("EX", 1, 210e9)  # Elastic moduli in Pa (kg/(m*s**2))
    mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
    mapdl.mp("NUXY", 1, 0.3)  # Poisson's Ratio 

    print("Finished Defining Units \n")


def mesh_volume(mapdl):

    mapdl.geometry.volume_select('ALL')
    print("Mesh volumes: ", mapdl.geometry.vnum)

    print("Meshing... \n")
    mapdl.prep7()
    mapdl.et(1, "SOLID187")
    mapdl.vmesh(*mapdl.geometry.vnum)
    
    print("Printing mesh...")
    _ = mapdl.eplot()

    print("Finished Meshing... \n")
    



# Runs the main function
main()