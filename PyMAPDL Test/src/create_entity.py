import numpy as np
import math 
from ansys.mapdl.core import launch_mapdl



def create_wire_cube(mapdl, center, w, r):

    # Difference in size between corners and beams
    d = r * 1.5
    
    # get x y z values of the cube
    cx = center[0]
    cy = center[1]
    cz = center[2]

    # Make top layer
    k010 = [cx-w, cy+w, cz-w]
    k011 = [cx-w, cy+w, cz+w]
    k111 = [cx+w, cy+w, cz+w]
    k110 = [cx+w, cy+w, cz-w]
    
    # Make bottom layer
    k000 = [cx-w, cy-w, cz-w]
    k001 = [cx-w, cy-w, cz+w]
    k101 = [cx+w, cy-w, cz+w]
    k100 = [cx+w, cy-w, cz-w]
    

    # extrude top layer beams
    extrude_beam_offset(mapdl, r, k010, k011, d)
    create_block(mapdl, d, k011)
    extrude_beam_offset(mapdl, r, k011, k111, d)
    create_block(mapdl, d, k111)
    extrude_beam_offset(mapdl, r, k111, k110, d)
    create_block(mapdl, d, k110)
    extrude_beam_offset(mapdl, r, k110, k010, d)
    create_block(mapdl, d, k010)

    # merge top layer
    mapdl.vadd(*mapdl.geometry.vnum)


    # extrude middle beams
    extrude_beam_offset(mapdl, r, k000, k010, d)
    extrude_beam_offset(mapdl, r, k100, k110, d)
    extrude_beam_offset(mapdl, r, k101, k111, d)
    extrude_beam_offset(mapdl, r, k001, k011, d)
    
    # merge top layer and middle beams
    mapdl.vadd(*mapdl.geometry.vnum)


    # extrude bottom layer beams
    extrude_beam_offset(mapdl, r, k000, k001, d)
    create_block(mapdl, d, k001)
    extrude_beam_offset(mapdl, r, k001, k101, d)
    create_block(mapdl, d, k101)
    extrude_beam_offset(mapdl, r, k101, k100, d)
    create_block(mapdl, d, k100)
    extrude_beam_offset(mapdl, r, k100, k000, d)
    create_block(mapdl, d, k000)

    # merge entire block
    mapdl.vadd(*mapdl.geometry.vnum)

    ret = mapdl.geometry.vnum
    mapdl.geometry.volume_select(ret, 'U')
    return ret[0]

def create_wire_cross_cube(mapdl, center, w, r):

    # Difference in size between corners and beams
    d = r * 1.5
    
    # get x y z values of the cube
    cx = center[0]
    cy = center[1]
    cz = center[2]

    # Make top layer
    k010 = [cx-w, cy+w, cz-w]
    k011 = [cx-w, cy+w, cz+w]
    k111 = [cx+w, cy+w, cz+w]
    k110 = [cx+w, cy+w, cz-w]
    
    # Make bottom layer
    k000 = [cx-w, cy-w, cz-w]
    k001 = [cx-w, cy-w, cz+w]
    k101 = [cx+w, cy-w, cz+w]
    k100 = [cx+w, cy-w, cz-w]
    

    # extrude top layer beams
    extrude_beam_offset(mapdl, r, k010, k011, d)
    create_block(mapdl, d, k011)
    extrude_beam_offset(mapdl, r, k011, k111, d)
    create_block(mapdl, d, k111)
    extrude_beam_offset(mapdl, r, k111, k110, d)
    create_block(mapdl, d, k110)
    extrude_beam_offset(mapdl, r, k110, k010, d)
    create_block(mapdl, d, k010)

    # merge top layer
    mapdl.vadd(*mapdl.geometry.vnum)


    # extrude middle beams
    extrude_beam_offset(mapdl, r, k000, k010, d)
    extrude_beam_offset(mapdl, r, k100, k110, d)
    extrude_beam_offset(mapdl, r, k101, k111, d)
    extrude_beam_offset(mapdl, r, k001, k011, d)
    
    # merge top layer and middle beams
    mapdl.vadd(*mapdl.geometry.vnum)


    # extrude bottom layer beams
    extrude_beam_offset(mapdl, r, k000, k001, d)
    create_block(mapdl, d, k001)
    extrude_beam_offset(mapdl, r, k001, k101, d)
    create_block(mapdl, d, k101)
    extrude_beam_offset(mapdl, r, k101, k100, d)
    create_block(mapdl, d, k100)
    extrude_beam_offset(mapdl, r, k100, k000, d)
    create_block(mapdl, d, k000)

    # merge edge block
    mapdl.vadd(*mapdl.geometry.vnum)

    mapdl.aplot()

    # Create cross beams
    extrude_beam(mapdl, r, k000, k111)
    #mapdl.vovlap(*mapdl.geometry.vnum)
    mapdl.vadd(*mapdl.geometry.vnum)

    extrude_beam(mapdl, r, k001, k110)
    # mapdl.vovlap(*mapdl.geometry.vnum)
    mapdl.vadd(*mapdl.geometry.vnum)

    extrude_beam(mapdl, r, k100, k011)
    # mapdl.vovlap(*mapdl.geometry.vnum)
    mapdl.vadd(*mapdl.geometry.vnum)

    extrude_beam(mapdl, r, k101, k010)
    #mapdl.vovlap(*mapdl.geometry.vnum)
    mapdl.vadd(*mapdl.geometry.vnum)

    create_block(mapdl, 1.5 * r, center)
    #mapdl.vovlap(*mapdl.geometry.vnum)
    mapdl.vadd(*mapdl.geometry.vnum)


    ret = mapdl.geometry.vnum
    mapdl.geometry.volume_select(ret, 'U')
    return ret[0]



def create_vovlap_test(mapdl, center, w, r):

    # Difference in size between corners and beams
    d = r * 1.15
    
    # get x y z values of the cube
    cx = center[0]
    cy = center[1]
    cz = center[2]

    # Make top layer
    k010 = [cx-w, cy+w, cz-w]
    k011 = [cx-w, cy+w, cz+w]
    k111 = [cx+w, cy+w, cz+w]
    k110 = [cx+w, cy+w, cz-w]
  
    # create first volumes
    extrude_beam(mapdl, r, k010, k011)
    create_block(mapdl, d, k011)

    mapdl.vovlap(*mapdl.geometry.vnum)
    mapdl.vadd(*mapdl.geometry.vnum)

    # create second volumes
    extrude_beam(mapdl, r, k011, k111)
    create_block(mapdl, d, k010)

    mapdl.vovlap(*mapdl.geometry.vnum)
    mapdl.vadd(*mapdl.geometry.vnum)
    
    #create third volumes
    extrude_beam(mapdl, r, k110, k010)
    create_block(mapdl, d, k111)

    mapdl.vovlap(*mapdl.geometry.vnum)
    mapdl.vadd(*mapdl.geometry.vnum)

    #create last volumes
    create_block(mapdl, d, k110)
    mapdl.vovlap(*mapdl.geometry.vnum)
    mapdl.vadd(*mapdl.geometry.vnum)
    
    extrude_beam(mapdl, r, k111, k110)
    mapdl.vovlap(*mapdl.geometry.vnum)
    mapdl.vadd(*mapdl.geometry.vnum)

    print("Final volumes:", mapdl.geometry.vnum)
    ret = mapdl.geometry.vnum
    mapdl.geometry.volume_select(ret, 'U')
    return ret[0]



def create_block(mapdl, w, center):
    # get x y z values of the cube
    cx = center[0]
    cy = center[1]
    cz = center[2]

    k0 = mapdl.k("", cx-w, cy-w, cz-w)
    k1 = mapdl.k("", cx+w, cy-w, cz-w)
    k2 = mapdl.k("", cx+w, cy-w, cz+w)
    k3 = mapdl.k("", cx-w, cy-w, cz+w)

    a0 = mapdl.a(k0, k1, k2, k3)
    mapdl.vext(a0, dy=w*2)


def merge_volume(mapdl, v):
    mapdl.geometry.volume_select('ALL')
    mapdl.vadd(*mapdl.geometry.vnum, v)
    
    mapdl.geometry.volume_select(mapdl.geometry.vnum, 'U')


def extrude_beam_offset(mapdl, r, start, end, offset):
    s = np.array(end) - np.array(start)
    x = s / np.linalg.norm(s)
    extrude_beam(mapdl, r, np.array(start) + offset * x, np.array(end) - offset * x)



def extrude_beam(mapdl, r, start, end):
    # calculate perpendicular point
    k = np.array(end) - np.array(start)
    x = np.array(start) - np.array([2, -5, 8])
    x -= x.dot(k) * x
    x = np.round(x, 0) + start

    # set keypoints
    k0 = mapdl.k("", *start)
    k1 = mapdl.k("", *end)
    kx = mapdl.k("", *x)

    # create volume
    l0 = mapdl.l(k1, k0)
    c0 = mapdl.al(* mapdl.circle(k0, r, k1, kx))
    mapdl.vdrag(c0, nlp1=l0)





