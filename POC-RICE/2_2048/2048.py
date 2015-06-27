"""
Clone of 2048 game.
"""

#import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # replace with your code
    
    l_len=len(line)
    mod_list = [x for x in line if x>0]
    list_len = len(mod_list)
    final_list=[]
    index=0
    while index<list_len:
        #print index
        if mod_list[index]==0:
            #print "A"
            pass
        elif index<list_len-1:
            #print "B"
            if mod_list[index]==mod_list[index+1]:
                #print "C"
                final_list.append(mod_list[index]*2)
                index=index+1
            else:
                final_list.append(mod_list[index])
        elif index==list_len-1:
            #print "D"
            final_list.append(mod_list[index])
        #print final_list
        index=index+1
        
    return final_list+[0]*(l_len-len(final_list))   

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._grid = [[0*col+0*row for col in range(grid_width)] for row in range(grid_height)]
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._dir_dict = {}
        self._dir_dict[UP] = [(0,y) for y in range(0,grid_width)]
        self._dir_dict[DOWN] = [(grid_height-1,y) for y in range(0,grid_width)]
        self._dir_dict[LEFT] = [(x,0) for x in range(0,grid_height)]
        self._dir_dict[RIGHT] = [(x,grid_width-1) for x in range(0,grid_height)]

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self._grid = [[0*col+0*row for col in range(self._grid_width)] for row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        strs=""
        for elem in self._grid:
            strs += str(elem)+"\n"  
        return strs

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        initial_cells=self._dir_dict[direction] 
        flag_move=0 
        for in_cell in initial_cells:
            line=[]
            row = in_cell[0]
            col = in_cell[1]
            while row<self._grid_height and col<self._grid_width and row>=0 and col>=0:
                #print row,col
                line.append(self.get_tile(row,col))
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]
            new_line = merge(line)
            row = in_cell[0]
            col = in_cell[1]
            index=0
            while row<self._grid_height and col<self._grid_width and row>=0 and col>=0:
                if self.get_tile(row,col)!=new_line[index]:
                    flag_move=1
                self.set_tile(row,col,new_line[index])
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]
                index+=1
        if flag_move==1:
            self.new_tile()

    def new_tile(self):
        
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        row = random.randrange(0,self._grid_height)
        col = random.randrange(0,self._grid_width)
        prob = random.randrange(0,10)
        if prob==9:
            value = 4
        else:
            value = 2
        if self.get_tile(row, col)==0:
            self.set_tile(row,col,value)
        else:
            if self.get_num_empty!=0:
                self.new_tile()
            else:
                print "YOU LOOSE"

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._grid[row][col]
    
    def get_num_empty(self):
        """
        Return the value of the tile at position row, col.
        """
        count=0
        for row in range(0,self._grid_height):
            for col in range(0,self._grid_width):
                if self.get_tile(row,col)==0:
                    count+=1
        return count


import poc_2048_gui
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

