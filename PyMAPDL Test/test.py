import numpy as np
import math
import os.path 
from ansys.mapdl.core import launch_mapdl

DEBUG_FUNCTIONS = False
DEBUG_MAIN = True


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

    # Creates the volume
    create_volume(mapdl)
    print(os.path.isfile('ex1.iges'))
    
    #mapdl.igesin('ex1.iges')

    mapdl.lplot()
    mapdl.vplot()

    # Creates the volume
    mesh_volume(mapdl)

    # Creates boundary conditions
    boundary_conditions(mapdl)

    # Runs simulations
    run(mapdl)

    print("Finished Running")











#    +-----------------------------------------------------+
#    |                                                     |
#    |              Operation Functions                    |
#    |                                                     |
#    +-----------------------------------------------------+

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


def create_volume(mapdl):
    print("Creating Volume... ") 

    bot = create_bottom_circle(mapdl)
    top = create_top_circle(mapdl, 3)
    if DEBUG_MAIN:
        print("Printing Volume... ")
        #mapdl.vplot()
    
        mapdl.vglue("ALL")

        #areas = mapdl.vsel("ALL")
        #mapdl.vinv(1, 2)
    
    print("Volume Processing Done... \n")


#TODO: This is currently a work in progress
def mesh_volume(mapdl):
    
    print("Creating Mesh... ")

    print(mapdl.vlist("ALL"))
    print("Meshing... \n")
    mapdl.prep7()
    mapdl.et(1, "SOLID187")
    mapdl.vmesh("all")





    mapdl.eplot(vtk=True, show_edges=True, show_axes=False, line_width=2, background="w")

    print("Finished Meshing... \n")
    

#TODO: This is currently a work in progress
def boundary_conditions(mapdl):
    mapdl.nsel("S", "LOC", "Z", 0)
    mapdl.nsel("R", "LOC", "x", -5, 5)
    mapdl.nsel("R", "LOC", "y", -5, 5)
    mapdl.d("ALL", "UX")
    mapdl.d("ALL", "UY")
    mapdl.d("ALL", "UZ")
    
    mapdl.nsel("S", "LOC", "Z", 6)
    mapdl.nsel("R", "LOC", "y", -5, 12)
    mapdl.f("ALL", "FZ", 1000)  

    _ = mapdl.allsel()


def run(mapdl):
    mapdl.run("/SOLU")
    mapdl.antype("STATIC")
    mapdl.solve()
    mapdl.finish()

    result = mapdl.result
    result.plot_principal_nodal_stress(
        0,
        "SEQV",
        lighting=False,
        background="w",
        show_edges=True,
        text_color="k",
        add_text=False,
    )
    result.plot_nodal_displacement(0)




def create_bottom_circle(mapdl):
        c0 = mapdl.k("", 0, 0, 0)

        bottom_circle = mapdl.al(*mapdl.circle(c0, 22))

        k0 = mapdl.k("", 0, 0, 0)
        k1 = mapdl.k("", 0, 0, 3)
        
        output = extrude_shape(mapdl, bottom_circle, k0, k1)

        mapdl.kdele(k0)
        mapdl.kdele(k1)
        mapdl.kdele(c0)
        
        return output

def create_top_circle(mapdl, height):
    c0 = mapdl.k("", 0, 0, height)

    circ1 = mapdl.al(*mapdl.circle(c0, 20))
    circ2 = mapdl.al(*mapdl.circle(c0, 24))
    top_circle = mapdl.asba(circ2, circ1)

    k0 = mapdl.k("", 0, 0, height)
    k1 = mapdl.k("", 0, 0, height + 3)
    output = extrude_shape(mapdl, top_circle, k0, k1)
    mapdl.kdele(k0)
    mapdl.kdele(k1)
    mapdl.kdele(c0)
    return output

def extrude_shape(mapdl, shape, k0, k1):
    l0 = mapdl.l(k0, k1)
    output = mapdl.vdrag(shape, nlp1=l0)
    mapdl.ldele(l0)

    if  DEBUG_FUNCTIONS:
            mapdl.vplot()
            print(output)

    return output


if __name__ == "__main__":
    main()
