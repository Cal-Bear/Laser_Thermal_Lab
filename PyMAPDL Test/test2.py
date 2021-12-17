from ansys.mapdl.core import launch_mapdl
mapdl = launch_mapdl()
from create_entity import *

mapdl.clear()
mapdl.prep7()

create_block(mapdl, 1, [-5, 5, 0])
create_block(mapdl, 1, [5, 5, -4])
create_block(mapdl, 1, [5, -5, 0])
create_block(mapdl, 2, [5, 5, 6])

mapdl.aplot()

