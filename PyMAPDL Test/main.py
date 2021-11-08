import numpy as np
import math 
from ansys.mapdl.core import launch_mapdl

DEBUG_FUNCTIONS = False
DEBUG_MAIN = False


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

    # Creates the volume
    #TODO: Complete meshing
    #mesh_volume(mapdl)

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

    print("Finished Defining Units \n\n")


def create_volume(mapdl):
    print("Creating Volume... ")
    

    # --------- Structure Variations  --------- 

    degree_offset = 60
    h = 30
    res = 10
    # --------- Structure Variations  --------- 

    create_bottom_circle(mapdl)

    #draw_line(mapdl, lambda x: x, degree_offset, 3, 21, 1, h, res)
    #draw_line(mapdl, lambda x: -x, degree_offset, 3, 21, 1, h, res)
    draw_line(mapdl, lambda x: 0,  degree_offset, 3, 21, 1, h, res)

    create_top_circle(mapdl, h)

    if DEBUG_MAIN:
        mapdl.lplot(show_line_numbering = False, show_keypoint_numbering = False)
        print("Printing Volume... ")
    
    print("Volume Processing Done... \n\n")


#TODO: This is currently a work in progress
def mesh_volume(mapdl):
    
    print("Creating Mesh... ")
    plate_esize = 0.01
    mapdl.esize(plate_esize)

    body = mapdl.asel("ALL")
    print(body, "\n\n\n")
    mapdl.amesh(body)



    print("Finished Meshing... \n\n")
    








#    +-----------------------------------------------------+
#    |                                                     |
#    |            create_volume Functions                  |
#    |                                                     |
#    +-----------------------------------------------------+

def draw_line(mapdl, f, offset, initial_z, circ_rad, beam_rad, height, resolution = 0.1):

    def f_gen(f, theta, r):
        def ret(z):
            a = math.atan(f(z)/r)
            x = r * math.cos(a + theta)
            y = r * math.sin(a + theta)
            return x, y
        return ret

    deg = 0
    while deg < 360 :
        x = circ_rad * math.cos(math.radians(deg))
        y = circ_rad * math.sin(math.radians(deg))
        z = initial_z

        f1 = f_gen(f, math.radians(deg), circ_rad)
        sweep_z_function(mapdl, f1, beam_rad, x, y, z, height, resolution)

        deg += offset

def create_bottom_circle(mapdl):
        bottom_point = mapdl.k("", 0, 0, 0)
        bottom_circle = create_circle(mapdl, bottom_point, ID = 20, OD = 22)

        k0 = mapdl.k("", 0, 0, 0)
        k1 = mapdl.k("", 0, 0, 3)
        extrude_shape(mapdl, bottom_circle, k0, k1)

def create_top_circle(mapdl, height):
        bottom_point = mapdl.k("", 0, 0, height)
        bottom_circle = create_circle(mapdl, bottom_point, ID = 20, OD = 22)

        k0 = mapdl.k("", 0, 0, height)
        k1 = mapdl.k("", 0, 0, height + 3)
        extrude_shape(mapdl, bottom_circle, k0, k1)

def sweep_z_function(mapdl, f, r = 1, x = 0, y = 0, z = 0, length = 10, res = 0.1):

    z1 = res
    x0, y0, z0 = x, y, 0
    while z1 <= length:
        x1, y1 = f(z1)

        k0 = mapdl.k("", x0, y0, z0 + z)
        k1 = mapdl.k("", x1, y1, z1 + z)

        if x1 >= x0:
            shape = mapdl.al(*mapdl.circle(k1, r))
        else:
            shape = mapdl.al(*mapdl.circle(k0, r))

        
        l0 = mapdl.l(k1, k0)

        curr = mapdl.vdrag(shape, nlp1=l0)

        x0, y0, z0 = x1, y1, z1
        z1 += res

    if DEBUG_FUNCTIONS:
            mapdl.vplot()

#    +-----------------------------------------------------+
#    |                                                     |
#    |                Extra Functions                      |
#    |                                                     |
#    +-----------------------------------------------------+

def create_circle(mapdl, c0, ID = 20, OD = 22):
        circ1 = mapdl.al(*mapdl.circle(c0, ID))
        circ2 = mapdl.al(*mapdl.circle(c0, OD))
        output = mapdl.asba(circ2, circ1)

        if  DEBUG_FUNCTIONS:
            mapdl.aplot()
            print(output)

        return output

def extrude_shape(mapdl, shape, k0, k1):
    l0 = mapdl.l(k0, k1)
    output = mapdl.vdrag(shape, nlp1=l0)

    if  DEBUG_FUNCTIONS:
            mapdl.vplot()
            print(output)

    return output


if __name__ == "__main__":
    main()
