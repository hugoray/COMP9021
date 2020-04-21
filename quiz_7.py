# COMP9021 19T3 - Rachid Hamadi
# Quiz 7 *** Due Thursday Week 9
#
# Randomly generates a grid of 0s and 1s and determines
# the maximum number of "spikes" in a shape.
# A shape is made up of 1s connected horizontally or vertically (it can contain holes).
# A "spike" in a shape is a 1 that is part of this shape and "sticks out"
# (has exactly one neighbour in the shape).


from random import seed, randrange
import sys
from collections import defaultdict


dim = 10


def display_grid():
    for row in grid:
        print('   ', *row) 


# Returns the number of shapes we have discovered and "coloured".
# We "colour" the first shape we find by replacing all the 1s
# that make it with 2. We "colour" the second shape we find by
# replacing all the 1s that make it with 3.

direction = [(-1,0),(1,0),(0,-1),(0,1)]


def mov(i, j, color):
    if 0 <= i < 10 and 0 <= j < 10 and grid[i][j] == 1:
        grid[i][j] = color
        for item in direction:
            x, y = item
            mov(x + i, y + j, color)
    else:
        return

def colour_shapes():
    color = 2
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 1:
                mov(i, j, color)
                color += 1
    groupdict = defaultdict(list)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 0:
                groupdict[grid[i][j]].append((i,j))
    return groupdict

def check(i,j,grid):
    count = 0
    if i == 0 or i == 9:
        count += 1

    if j == 0 or j == 9:
        count += 1

    for item in direction:
        x = item[0]
        y = item[1]
        new_x = i + x
        new_y = j + y

        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y] == 0:
            count += 1
    if count == 3:
        return count


def max_number_of_spikes(nb_of_shapes):
    spikesdict = defaultdict(int)
    for i in nb_of_shapes:
        if len(nb_of_shapes[i]) < 2:
            pass
        else:
            for x,y in nb_of_shapes[i]:
                if check(x,y,grid):
                    spikesdict[grid[x][y]] += 1

    return max(spikesdict.values())
    # Replace pass above with your code


# Possibly define other functions here    


try: 
    for_seed, density = (int(x) for x in input('Enter two integers, the second '
                                               'one being strictly positive: '
                                              ).split()
                    )
    if density <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[int(randrange(density) != 0) for _ in range(dim)]
            for _ in range(dim)
       ]
print('Here is the grid that has been generated:')
display_grid()
nb_of_shapes = colour_shapes()
print('The maximum number of spikes of some shape is:',
      max_number_of_spikes(nb_of_shapes)
     )
