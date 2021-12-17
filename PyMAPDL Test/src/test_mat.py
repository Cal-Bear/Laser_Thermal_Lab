import numpy as np
import math 
from ansys.mapdl.core import launch_mapdl
from create_entity import *


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


    r0 = create_wire_cube(mapdl, [0, 0, 0], 10, 1)
    mapdl.aplot()

    r1 = create_wire_cube(mapdl, [0, 22, 0], 10, 1)
    mapdl.aplot()

    r2 = create_wire_cube(mapdl, [22, 0, 0], 10, 1)
    mapdl.aplot()

    r3 = create_wire_cube(mapdl, [0, 0, 22], 10, 1)
    mapdl.aplot()

    print("Return:", r0, r1, r2, r3)
    print("current selections: ", mapdl.geometry.vnum)

    mapdl.vadd(r0, r1, r2, r3)


    print("printing...")
    mapdl.aplot()

    



    print("done")



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

    print("Meshing... \n")
    mapdl.prep7()
    mapdl.et(1, "SOLID187")
    mapdl.vmesh(*mapdl.geometry.vnum)

    
    print("Printing mesh...")
    _ = mapdl.eplot(vtk=True, show_edges=True, show_axes=False, line_width=2, background="w")

    print("Finished Meshing... \n")
    # mapdl.et(1, "SOLID186")
    # mapdl.vsweep("all")
    # _ = mapdl.eplot()



# Runs the main function
main()