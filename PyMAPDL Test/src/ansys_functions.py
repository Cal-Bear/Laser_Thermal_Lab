import numpy as np
import math 
from ansys.mapdl.core import launch_mapdl
from block import *


#    +-----------------------------------------------------+
#    |                                                     |
#    |                 Main Functions                      |
#    |                                                     |
#    +-----------------------------------------------------+

def test_ansys():
    # Create mapdl Object
    mapdl = launch_mapdl()
    mapdl.clear()

    # Define units and material details
    define_units(mapdl)

    r0 = create_wire_cross(mapdl, [0, 0, 0], 10)
    mapdl.aplot()
    create_wire_cross(mapdl, [0, 0, 10], 10)
    mapdl.aplot()
    # merge_volume(mapdl, create_wire_cross_cube(mapdl, [0, 0, 10], 10))
    # merge_volume(mapdl, create_wire_cube(mapdl, [0, 10, 0], 10))
    # merge_volume(mapdl, create_wire_cross_cube(mapdl, [0, 10, 10], 10))

    # merge_volume(mapdl, create_wire_cube(mapdl, [10, 0, 0], 10))
    # merge_volume(mapdl, create_wire_cube(mapdl, [10, 0, 10], 10))
    # merge_volume(mapdl, create_wire_cube(mapdl, [10, 10, 0], 10))
    # merge_volume(mapdl, create_wire_cube(mapdl, [10, 10, 10], 10))



    print("printing...")
    # mapdl.aplot()


    # mesh_volume(mapdl)

    
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





#    +-----------------------------------------------------+
#    |                                                     |
#    |                Mapdl Functions                      |
#    |                                                     |
#    +-----------------------------------------------------+

def refresh_volumes(mapdl):
    ret = mapdl.geometry.vnum
    print("current stuff:", mapdl.geometry.vnum)
    mapdl.geometry.volume_select(ret, 'U')
    return ret

def merge_volume(mapdl, v):
    mapdl.geometry.volume_select('ALL')
    if v in mapdl.geometry.vnum:
        mapdl.vadd(*mapdl.geometry.vnum)
    else:
        mapdl.vadd(*mapdl.geometry.vnum, v)
    
    mapdl.geometry.volume_select(mapdl.geometry.vnum, 'U')

def merge_all(mapdl):
    mapdl.geometry.volume_select('ALL')
    if len(mapdl.geometry.vnum) > 1:
        mapdl.vadd(*mapdl.geometry.vnum)
    
    mapdl.geometry.volume_select(mapdl.geometry.vnum, 'U')


# test_ansys()