


class block_matrix:
    
    block_width = 10

    def __init__(self, input):
        ''' Creates an block matrix, which houses the different object values
            inout = input matrix of the top corner of the matrix

            Represented as a list of 2D matricies, starting from the outside and going in

            [[[a, b], 
              [c, d]],

             [[e, f], 
              [g, h]]]

        '''
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
    
    def generate_blocks(self):
    


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

        





a = block_matrix([[['a']]])
a.print_short()
a.print_full()




