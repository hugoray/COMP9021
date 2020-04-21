# COMP9021 19T3 - Rachid Hamadi
# Assignment 2 *** Due Sunday Week 10


# IMPORT ANY REQUIRED MODULE
import numpy as np
import copy
from collections import defaultdict

direction = [(-1,0),(1,0),(0,-1),(0,1)]

def mov(i, j, m, color, grid):
    if 0 <= i < len(grid) and 0 <= j < len(grid[0]) and grid[i][j] == m:
        grid[i][j] = color
        for item in direction:
            x, y = item
            mov(x + i, y + j, m, color, grid)
    else:
        return

def check(i,j,grid,alist):
    # i代表高，j代表宽
    if 0 < i < len(grid)-1 and 0 < j < len(grid[0])-1:
        if grid[i][j] != 0:
            return
        if int(grid[i+1][j] != 0) + int(grid[i-1][j] != 0) + int(grid[i][j+1] != 0) + int(grid[i][j-1] !=0) == 3:
            grid[i][j] = 7
            check(i-1,j,grid,alist)
            check(i,j-1,grid,alist)
            check(i+1,j,grid,alist)
            check(i,j+1,grid,alist)
            alist.append((i,j))
        else:
            return
    elif i == 0 or j == 0 or i == len(grid)-1 or j == len(grid)-1:
        if grid[i][j] == 0:
            grid[i][j] = 7
            alist.append((i,j))

class MazeError(Exception):
    def __init__(self, message):
        self.messsage = message

    #def __repr__(self):
        #return self.message


class Maze:
    def __init__(self, filename):
        self.filename = filename
        try:
            file = open(self.filename)
        except FileNotFoundError:
            raise MazeError('Incorrect input.')
        self.open()
        self.maze_mapping()
        self.analyse_gates()
        self.analyse_walls()
        self.analyse_inner_points()
        self.analyse_acc_areas()
        self.analyse_cul_de_sacs()
        self.analyse_pillars()
        self.analyse_path()
        self.analyse()
        self.draw_walls()
        self.draw_graph()
        self.display()
        # REPLACE PASS ABOVE WITH YOUR CODE
    
    # POSSIBLY DEFINE OTHER METHODS

    def open(self):
        with open(self.filename) as f:
            contents = []
            code = f.readlines()
            for i in code:
                line = ''.join(x for x in i.split())
                if line:
                    for item in line:
                        if item not in ('0','1','2','3'):
                            raise MazeError('Incorrect input.')
                    contents.append(line)
            # 计算输入的长度、高度 长度在2-31，高度在2-41之内
            contents_width = len(contents[0])
            contents_height = len(contents)
            if not 2 <= contents_width <= 31 or not 2 <= contents_height <= 41:
                raise MazeError('Incorrect input.')

            # 检测每行长度是否相等
            for i in range(contents_height):
                if len(contents[i]) != contents_width:
                    raise MazeError('Incorrect input.')
                # 检测该矩阵的最下行和最右列是否有2、3 and 1、3
                for j in range(len(contents[i])):
                    if i == contents_height - 1:
                        if contents[i][j] == '2' or contents[i][j] == '3':
                            raise MazeError('Input does not represent a maze.')
                    if j == contents_width - 1:
                        if contents[i][j] == '1' or contents[i][j] == '3':
                            raise MazeError('Input does not represent a maze.')
            self.contents = contents

    def maze_mapping(self):
        contents = self.contents
        mapping = np.zeros((len(contents) * 2 - 1, len(contents[0]) * 2 - 1), dtype=int)
        # convert the items in contents to the symbols in mapping
        # 注意为了避免相邻的图形不能形成闭环，所以这边采用3*3的构造法
        for i in range(len(contents)):
            for j in range(len(contents[i])):
                if contents[i][j] == '0':
                    pass
                elif contents[i][j] == '1':
                    mapping[2*i][2*j] = 1
                    mapping[2*i][2*j+1] = 1
                    mapping[2*i][2*j+2] = 1
                elif contents[i][j] == '2':
                    mapping[2*i][2*j] = 1
                    mapping[2*i+1][2*j] = 1
                    mapping[2*i+2][2*j] = 1
                elif contents[i][j] == '3':
                    mapping[2*i][2*j] = 1
                    mapping[2*i+1][2*j] = 1
                    mapping[2*i+2][2*j] = 1
                    mapping[2*i][2*j+1] = 1
                    mapping[2*i][2*j+2] = 1
        self.mapping = copy.deepcopy(mapping)

    def analyse_gates(self):
        mapping = copy.deepcopy(self.mapping)
        count_gates = 0
        gates_dir = []
        for i in range(len(mapping)):
            for j in range(len(mapping[i])):
                if i == 0 or i == len(mapping)-1:
                    if (0 < j < len(mapping[i])-1) and j % 2 == 1 and mapping[i][j] == 0:
                        count_gates += 1
                        gates_dir.append((i, j))
                else:
                    if i % 2 == 1 and mapping[i][j] == 0:
                        if j == len(mapping[i]) - 1:
                            count_gates += 1
                            gates_dir.append((i, j))
                        elif j == 0:
                            count_gates += 1
                            gates_dir.append((i, j))
        self.count_gates = count_gates
        self.gates_dir = gates_dir
        self.num_gates = len(gates_dir)

    def analyse_walls(self):
        mapping = copy.deepcopy(self.mapping)
        color = 2
        for i in range(len(mapping)):
            for j in range(len(mapping[i])):
                if mapping[i][j] == 1:
                    mov(i, j, 1, color, mapping)
                    color += 1
        groupdict = defaultdict(list)
        for i in range(len(mapping)):
            for j in range(len(mapping[0])):
                if mapping[i][j] != 0:
                    groupdict[mapping[i][j]].append((i, j))
        count = 0
        for item in groupdict.keys():
            count += 1
        self.walls = groupdict
        self.num_walls = count
        #print(count)

    def analyse_inner_points(self):
        mapping = copy.deepcopy(self.mapping)
        gates_dir = self.gates_dir
        color = -1
        for i in range(len(mapping)):
            for j in range(len(mapping[i])):
                if mapping[i][j] == 0:
                    mov(i, j, 0, color, mapping)
                    color -= 1
        groupdict = defaultdict(list)
        for i in range(len(mapping)):
            for j in range(len(mapping[0])):
                if mapping[i][j] < 0:
                    groupdict[mapping[i][j]].append((i, j))

        del_list =[]
        add_list =[]
        for item in gates_dir:
            for alpha in groupdict.keys():
                if item in groupdict[alpha]:
                    del_list.append(alpha)

        del_list = list(set(del_list))
        for item in groupdict.keys():
            if item not in del_list:
                add_list.append(item)
        add_list = list(set(add_list))
        self.add_list =add_list

        for item in del_list:
            del groupdict[item]

        count = 0

        dict_values = list(groupdict.values())
        for i in range(len(dict_values)):
            for j in range(len(dict_values[i])):
                x,y = dict_values[i][j]
                if x % 2 == 1 and y % 2 == 1:
                    count += 1
        self.num_inner_points = count

    def analyse_acc_areas(self):
        mapping = copy.deepcopy(self.mapping)
        gates_dir = self.gates_dir
        color = -1
        for i in range(len(mapping)):
            for j in range(len(mapping[i])):
                if mapping[i][j] == 0:
                    mov(i, j, 0, color, mapping)
                    color -= 1
        groupdict = defaultdict(list)
        self.blanks = groupdict
        for i in range(len(mapping)):
            for j in range(len(mapping[0])):
                if mapping[i][j] < 0:
                    groupdict[mapping[i][j]].append((i, j))

        add_list =[]
        for item in gates_dir:
            for alpha in groupdict.keys():
                if item in groupdict[alpha]:
                    add_list.append(alpha)

        add_list = list(set(add_list))
        self.num_acc_areas = len(add_list)

    def analyse_cul_de_sacs(self):
        mapping = copy.deepcopy(self.mapping)
        blanks = copy.deepcopy(self.blanks)
        add_list = self.add_list
        temp = []
        alist = []
        for i in add_list:
            del blanks[i]
        for i in blanks:
            for j in blanks[i]:
                temp.append(j)
        for i in range(1, len(mapping)-1):
            for j in range(1, len(mapping[0])-1):
                x, y = i, j
                if [x, y] in temp:
                    continue
                if int(mapping[x + 1][y] != 0) + int(mapping[x - 1][y] != 0) + int(mapping[x][y + 1] != 0) + int(mapping[x][y - 1] != 0) == 3:
                    check(x,y,mapping,alist)
        self.mapping_2 = copy.deepcopy(mapping)
        #print(mapping)
        color = 8
        for i in range(len(mapping)):
            for j in range(len(mapping[i])):
                if mapping[i][j] == 7:
                    mov(i, j, 7, color, mapping)
                    color += 1
        groupdict = defaultdict(list)
        for i in range(len(mapping)):
            for j in range(len(mapping[0])):
                if mapping[i][j] > 7:
                    groupdict[mapping[i][j]].append((i, j))
        #print(groupdict)
        del_list = []
        for i in groupdict:
            for j in groupdict[i]:
                if j not in temp:
                    del_list.append(i)
        del_list = list(set(del_list))
        for i in del_list:
            del groupdict[i]
        self.cul_de_sacs = copy.deepcopy(groupdict)
        self.num_cul_de_sacs = len(groupdict.keys())

    def analyse_pillars(self):
        contents = self.contents
        pillars = []
        for i in range(len(contents)):
            for j in range(len(contents[0])):
                if contents[i][j] == '0':
                    if i == 0 and j == 0:
                        pillars.append((i, j))
                    elif i == 0 and contents[i][j - 1] in ['0', '2']:
                        pillars.append((i, j))
                    elif j == 0 and contents[i - 1][j] in ['0', '1']:
                        pillars.append((i, j))
                    elif contents[i][j - 1] in ['0', '2'] and contents[i - 1][j] in ['0', '1']:
                        pillars.append((i, j))
        #print(pillars)
        self.pillar_list = copy.deepcopy(pillars)

    def analyse_path(self):
        def get_key(dict, value):
            return [k for k, v in dict.items() if v == value]
        mapping = copy.deepcopy(self.mapping_2)
        gates_dir = self.gates_dir
        pillar_list = self.pillar_list

        for i in pillar_list:
            x,y = i
            mapping[x*2][y*2] = 1

        for i in range(len(mapping)):
            for j in range(len(mapping[i])):
                if mapping[i][j] == 7:
                    mapping[i][j] = 1
        #print(mapping)
        color = -2
        for i in range(len(mapping)):
            for j in range(len(mapping[i])):
                if mapping[i][j] == 0:
                    mov(i, j, 0, color, mapping)
                    color -= 1
        groupdict = defaultdict(list)
        for i in range(len(mapping)):
            for j in range(len(mapping[0])):
                if mapping[i][j] < 0:
                    groupdict[mapping[i][j]].append((i, j))
        final_path = []
        for i in groupdict.keys():
            count = 0
            for j in groupdict[i]:
                if j in gates_dir:
                    count += 1
            if count == 2:
                final_path.append(i)
        #print(final_path)
        blist = list(groupdict.keys())
        clist = []
        for i in blist:
            if i not in final_path:
                clist.append(i)
        #print(clist)
        for i in clist:
            del groupdict[i]
        dlist = list(groupdict.values())
        elist = []
        for i in range(len(dlist)):
            for j in range(len(dlist[i])):
                x,y = dlist[i][j]
                m = x-1,y
                n = x,y-1
                p = x+1,y
                q = x,y+1
                count = 0
                if m in dlist[i]:
                    count += 1
                if n in dlist[i]:
                    count += 1
                if p in dlist[i]:
                    count += 1
                if q in dlist[i]:
                    count += 1
                if count > 2:
                    elist.append(i)
        elist = list(set(elist))
        flist = []
        glist = []
        for item in elist:
            flist.append(dlist[item])

        for item in flist:
            glist.append(get_key(groupdict,item))
        #print(glist)
        for i in range(len(glist)):
            del groupdict[glist[i][0]]

        self.final_path = groupdict
        print(groupdict)
        self.num_final_path = (len(final_path)-len(flist))

    def analyse(self):
        num_walls = self.num_walls
        num_gates = self.num_gates
        num_inner_points = self.num_inner_points
        num_acc_areas = self.num_acc_areas
        num_cul_de_sacs = self.num_cul_de_sacs
        num_final_path = self.num_final_path

        if num_gates == 0:
            print('The maze has no gate.')
        elif num_gates == 1:
            print('The maze has a single gate.')
        else:
            print(f'The maze has {num_gates} gates.')

        if num_walls == 0:
            print('The maze has no wall.')
        elif num_walls == 1:
            print('The maze has walls that are all connected.')
        else:
            print(f'The maze has {num_walls} sets of walls that are all connected.')

        if num_inner_points == 0:
            print('The maze has no inaccessible inner point.')
        elif num_inner_points == 1:
            print('The maze has a unique inaccessible inner point.')
        else:
            print(f'The maze has {num_inner_points} inaccessible inner points.')

        if num_acc_areas == 0:
            print('The maze has no accessible area.')
        elif num_acc_areas == 1:
            print('The maze has a unique accessible area.')
        else:
            print(f'The maze has {num_acc_areas} accessible areas.')

        if num_cul_de_sacs == 0:
            print('The maze has no accessible cul-de-sac.')
        elif num_cul_de_sacs == 1:
            print('The maze has accessible cul-de-sacs that are all connected.')
        else:
            print(f'The maze has {num_cul_de_sacs} sets of accessible cul-de-sacs that are all connected.')

        if num_final_path == 0:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        elif num_final_path == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print(f'The maze has {num_final_path} entry-exit paths with no intersections not to cul-de-sacs.')

    def draw_walls(self):
        maze = copy.deepcopy(self.contents)
        maze1 = []
        for i in range(len(maze)):
            maze1.append([])
            for j in range(len(maze[i])):
                maze1[i].append(int(maze[i][j]))
        #print(maze1)
        maze2 = copy.deepcopy(maze1)
        wall_list = []
        for i in range(len(maze1)):
            for j in range(len(maze1[0])):
                a = j
                while maze1[i][a] == 1 or maze1[i][a] == 3:
                    maze1[i][a] = 0
                    a += 1
                if a - j >= 1:
                    draw = [(j, i), (a, i)]
                    wall_list.append(draw)
        for i in range(len(maze2[0])):
            for j in range(len(maze2)):
                a = j
                while maze2[a][i] == 2 or maze2[a][i] == 3:
                    maze2[a][i] = 0
                    a += 1
                if a - j >= 1:
                    draw = [(i, j), (i, a)]
                    wall_list.append(draw)
        #print(wall_list)
        self.wall_list = wall_list

    def draw_graph(self):
        mapping = self.mapping
        final_path = self.final_path
        path_list = []
        for i in range(len(sorted(final_path.values()))):
            path_list.append(list(final_path.values())[i])

        for i in range(len(path_list)):
            for j in range(len(path_list[i])):
                x, y = path_list[i][j]
                if x == 0:
                    path_list[i].append((x - 1, y))
                elif y == 0:
                    path_list[i].append((x, y - 1))
                elif x == len(mapping) - 1:
                    path_list[i].append((x + 1, y))
                elif y == len(mapping[0]) - 1:
                    path_list[i].append((x, y + 1))
        #print(path_list)

        alist = []
        blist = []
        for i in range(len(path_list)):
            path_x = copy.deepcopy(sorted(path_list[i], key=lambda x: (x[0], x[1])))
            path_y = copy.deepcopy(sorted(path_list[i], key=lambda x: (x[1], x[0])))
            path_x_list = [path_x[0]]
            path_y_list = [path_y[0]]
            for i in range(len(path_x)):
                if path_x[i][-1] - path_x_list[-1][-1] == 1 and path_x[i][0] == path_x_list[-1][0]:
                    path_x_list.append(path_x[i])
                else:
                    if len(path_x_list) > 1:
                        alist.append((path_x_list[0], path_x_list[-1]))
                    path_x_list = [path_x[i]]
                if path_y[i][0] - path_y_list[-1][0] == 1 and path_y[i][1] == path_y_list[-1][1]:
                    path_y_list.append(path_y[i])
                else:
                    if len(path_y_list) > 1:
                        blist.append((path_y_list[0], path_y_list[-1]))
                    path_y_list = [path_y[i]]
                if len(path_x_list) > 1 and i == len(path_x) - 1:
                    alist.append((path_x_list[0], path_x_list[-1]))
                if len(path_y_list) > 1 and i == len(path_y) - 1:
                    blist.append((path_y_list[0], path_y_list[-1]))
        alist = sorted(alist, key=lambda x: (x[0]))
        alist.extend(sorted(blist, key=lambda x: (x[0][1])))
        self.path_draw = alist

    def display(self):
        name = self.filename
        name = name.split('.')
        tex_name = name[0] + '.tex'
        tex = open(tex_name, 'w')

        tex.write('''\\documentclass[10pt]{article}
\\usepackage{tikz}
\\usetikzlibrary{shapes.misc}
\\usepackage[margin=0cm]{geometry}
\\pagestyle{empty}
\\tikzstyle{every node}=[cross out, draw, red]

\\begin{document}

\\vspace*{\\fill}
\\begin{center}
\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n''')

        tex.write('% Walls\n')
        wall_list = self.wall_list
        for i in wall_list:
            (x1, y1), (x2, y2) = i
            tex.write(f'    \\draw ({x1},{y1}) -- ({x2},{y2});\n')

        tex.write('% Pillars\n')
        pillars = self.pillar_list
        for i in pillars:
            x, y = i
            tex.write(f'    \\fill[green] ({y},{x}) circle(0.2);\n')

        tex.write('% Inner points in accessible cul-de-sacs\n')
        cul_de_sacs = list((self.cul_de_sacs).values())
        cross = []
        for i in range(len(cul_de_sacs)):
            for j in cul_de_sacs[i]:
                cross.append(j)
        cross.sort()
        for i in range(len(cross)):
            x1, y1 = cross[i]
            if x1 % 2 == 1 and y1 % 2 == 1:
                tex.write(f'    \\node at ({y1 / 2},{x1 / 2}) {{}};\n')

        tex.write('% Entry-exit paths without intersections\n')
        path = self.path_draw
        for i in range(len(path)):
            (x1, y1), (x2, y2) = path[i]
            tex.write(f'    \draw[dashed, yellow] ({y1 / 2},{x1 / 2}) -- ({y2 / 2},{x2 / 2});\n')

        tex.write('''\\end{tikzpicture}
\\end{center}
\\vspace*{\\fill}

\\end{document}\n''')
        # REPLACE PASS ABOVE WITH YOUR CODE

