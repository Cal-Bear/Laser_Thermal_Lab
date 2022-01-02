from ansys_functions import *

class block_matrix:
    
    block_width = 10


    def __init__(self, input, type = 's'):
        ''' Creates an block matrix, which houses the different object values
            inout = input matrix of the top corner of the matrix

            Represented as a list of 2D matricies, starting from the outside and going in

            [[[a, b], 
              [c, d]],

             [[e, f], 
              [g, h]]]

        '''
        if type == 'f':
            self.short = None
            self.full = input
        else:
            self.short = input
            self.full = self.expand(input)
        
    

    def expand(self, input):
        ''' Expands the shortened matrix into a full matrix through mirrorinf values
                across the x, y, and x axes

            input = input matrix of the top left corner of the matrix. 
            [0,  ]
            [ ,  ]
            -----
            [ ,  ]
            [ ,  ]

            e.g. 
            In: ['a', 'b']
                ['c', 'd']
                -----
                ['e', 'f']
                ['g', 'h']
            
            Out:['a', 'b', 'b', 'a']
                ['c', 'd', 'd', 'c']
                ['c', 'd', 'd', 'c']
                ['a', 'b', 'b', 'a']
                -----
                ['e', 'f', 'f', 'e']
                ['g', 'h', 'h', 'g']
                ['g', 'h', 'h', 'g']
                ['e', 'f', 'f', 'e']
                -----
                ['e', 'f', 'f', 'e']
                ['g', 'h', 'h', 'g']
                ['g', 'h', 'h', 'g']
                ['e', 'f', 'f', 'e']
                -----
                ['a', 'b', 'b', 'a']
                ['c', 'd', 'd', 'c']
                ['c', 'd', 'd', 'c']
                ['a', 'b', 'b', 'a']
        '''

        ret = []
        for i in (self.short + self.short[::-1]):
            inner = []
            for j in (i + i[::-1]):
                inner.append(j + j[::-1])
            ret.append(inner)

        return ret
    

    def generate_blocks(self, mapdl):
        return None


    def print_short(self):
        for i in self.short:
            for j in i:
                print(j)
            print("-----")
    

    def print_full(self):
        for i in self.full:
            for j in i:
                print(j)
            print("-----")


    def construct_matrix(self, mapdl, merge, dict):
        
        self.print_full()
        blocks = self.full
        first = True

        for i in range(len(blocks)):
            for j in range(len(blocks[i])):
                for k in range(len(blocks[i][j])):
                    # Determing block type
                    print("block type: ", blocks[i][j][k])
                    letter = blocks[i][j][k]
                    if letter in dict.keys():
                        f = dict[letter]
                    else:
                        print("Key", letter, "could not be found")
                        f = dict["e"]

                    # Create the volume
                    curr = f(mapdl, 
                      [i*block_matrix.block_width, 
                       j*block_matrix.block_width, 
                       k*block_matrix.block_width], 
                      block_matrix.block_width)

                    # Merge the volume
                    if not first and curr != None:
                        try:
                            merge(mapdl, curr)
                        except Exception as e:
                            print("\n","Skipping merge operation and attempting to move on...","\n")
                            refresh_volumes(mapdl)
                            mapdl.aplot()
                            continue 
                    else:
                        first = False
                    
                    
                    
















