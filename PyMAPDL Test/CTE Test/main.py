import numpy as np
import math 
from ansys.mapdl.core import launch_mapdl

DEBUG_FUNCTIONS = False
DEBUG_MAIN = True

def main():

    # Create mapdl Object
    mapdl = launch_mapdl()
    mapdl.clear()

    # Create volume and mesh
    create_volume(mapdl)
    mapdl.eplot(show_edges=True, show_node_numbering=True)


    # boundary conditions
    define_boundries(mapdl)
    
    # run simulation
    run(mapdl)
    


def create_volume(mapdl):

    def meshVolume(vol, mat):
        mapdl.mat(mat)
        mapdl.geometry.volume_select(vol, 'S')
        mapdl.et(1, 'SOLID187')
        mapdl.vmesh(vol)
        mapdl.geometry.volume_select(vol, 'U')


    print("Creating Volume... ")
    mapdl.prep7()

    # Define materials/initial values
    mapdl.units("BIN")
    mapdl.tref(20)
        
    mapdl.mp("EX", 1, 30023280.0)
    mapdl.mp("ALPX", 1, 8.388888889e-06)
  
    mapdl.mp("EX", 2, 25023280.0)
    mapdl.mp("ALPX", 2, 1.388888889e-05)


    # Create object 1
    mapdl.block(9, 11, 0, 10, -1, 1)
    v1 = mapdl.geometry.vnum[0]
    print(mapdl.geometry.vnum)
    mapdl.geometry.volume_select(v1, 'U')

    # Create Object 2
    mapdl.block(-1, 1, 0, 10, -1, 1)
    v2 = mapdl.geometry.vnum[0]
    print(mapdl.geometry.vnum)
    mapdl.geometry.volume_select(v2, 'U')


    # Create object case
    mapdl.block(-3, -2, 0, 10, -1, 1)
    mapdl.block(2, 3, 0, 10, -1, 1)

    mapdl.block(-3, 3, -1, -0, -1, 1)
    mapdl.block(-3, 3, 10, 11, -1, 1)
    mapdl.vplot()

    mapdl.vadd(*mapdl.geometry.vnum)
    v3 = mapdl.geometry.vnum[0]
    print(mapdl.geometry.vnum)
    mapdl.vplot()
    mapdl.geometry.volume_select(v3, 'U')
   

    
    meshVolume(v3, 1)
    meshVolume(v1, 2)
    meshVolume(v2, 2)

    print("Volume Processing Done... \n")
    

def define_boundries(mapdl):

    def fix_end(mapdl):
        mapdl.nsel("S", "LOC", "Y", 0)
        mapdl.d("all", "all")
        mapdl.allsel()

    print("starting boundary conditions... ")

    fix_end(mapdl)
    mapdl.gst(1, 1)

    mapdl.allsel()
    mapdl.tunif(300)


def run(mapdl):
    mapdl.run("/SOLU")  
    mapdl.solve()
    mapdl.finish()
    result = mapdl.result

    result = mapdl.result
    print(result)

    print("display displacement:\n")
    result.plot_nodal_displacement(0, show_displacement=True, displacement_factor=0.4, n_colors=20)

    print("displaying values:\n")

    # di = mapdl.post_processing.nodal_displacement('Y')
    # print(di)


    print("Finished Running")





if __name__ == "__main__":
    main()
