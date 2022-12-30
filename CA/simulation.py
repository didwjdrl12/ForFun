# initial values
from copy import deepcopy
import sys

import numpy as np
from numpy.core.umath import pi
from numpy.ma import sin

scale = 50  # 1m -> 50 cells
size_x = 6 * scale
size_y = 6 * scale
damping = 0.99
omega = 1 / (2 * pi)

initial_P = 300
vertPos = size_y- 3*scale
horizPos = size_x- 3*scale
wallTop = size_x - 4*scale
wall_x_pos = 2 * scale
max_pressure = initial_P / 2
min_presure = -initial_P / 2


class Simulation:
    def __init__(self):
        self.frame = 0
        self.pressure = [[0.0 for x in range(size_x)] for y in range(size_y)]
        self.prev_pressure = [[0.0 for x in range(size_x)] for y in range(size_y)]
        # outflow velocities from each cell
        self._velocities = [[[0.0, 0.0, 0.0, 0.0] for x in range(size_x)] for y in range(size_y)]
        self.pressure[vertPos][horizPos] = initial_P
        self.chladniplate = np.zeros((size_x,size_y))
        self.diff = np.zeros((size_x,size_y))

    def updateV(self):
        """Recalculate outflow velocities from every cell basing on preassure difference with each neighbour"""
        V = self._velocities
        P = self.pressure
        for i in range(size_y):
            for j in range(size_x):
                if wall[i][j] == 1:
                    V[i][j][0] = V[i][j][1] = V[i][j][2] = V[i][j][3] = 0.0
                    continue
                cell_pressure = P[i][j]
                V[i][j][0] = V[i][j][0] + cell_pressure - P[i - 1][j] if i > 0 else cell_pressure
                V[i][j][1] = V[i][j][1] + cell_pressure - P[i][j + 1] if j < size_x - 1 else cell_pressure
                V[i][j][2] = V[i][j][2] + cell_pressure - P[i + 1][j] if i < size_y - 1 else cell_pressure
                V[i][j][3] = V[i][j][3] + cell_pressure - P[i][j - 1] if j > 0 else cell_pressure

    def updateP(self):
        self.prev_pressure = deepcopy(self.pressure)
        for i in range(size_y):
            for j in range(size_x):
                self.pressure[i][j] -= 0.5 * damping * sum(self._velocities[i][j])


    def updateAct(self):
        diff_phase = 20
        # for i in range(50,250):
        #     self.pressure[50][i] = initial_P * sin(omega * self.frame)
        #     self.pressure[250][i] = initial_P * sin(omega * (self.frame+diff_phase))
        self.pressure[51][100] = initial_P/5 * sin(omega * self.frame)
        self.pressure[51][150] = initial_P/5 * sin(omega * self.frame)
        self.pressure[51][200] = initial_P/5 * sin(omega * self.frame)
        self.pressure[100][51] = initial_P/5 * sin(omega * self.frame)
        self.pressure[100][249] = initial_P/5 * sin(omega * self.frame)
        self.pressure[150][51] = initial_P/5 * sin(omega * self.frame)
        self.pressure[150][249] = initial_P/5 * sin(omega * self.frame)
        self.pressure[200][51] = initial_P/5 * sin(omega * self.frame)
        self.pressure[200][249] = initial_P/5 * sin(omega * self.frame)
        self.pressure[249][100] = initial_P/5 * sin(omega * self.frame)
        self.pressure[249][150] = initial_P/5 * sin(omega * self.frame)
        self.pressure[249][200] = initial_P/5 * sin(omega * self.frame)
        
    
    def updateCp(self):
        np_pressure = np.array(self.pressure)
        # print("pressure max", np.max(np_pressure))
        np_prev_pressure = np.array(self.prev_pressure)
        # print("prev max", np.max(np_prev_pressure))
        self.diff  = np_pressure - np_prev_pressure
        # print("diff max", np.max(self.diff))
        self.norm_diff =  np.abs(self.diff)
        
        self.chladniplate = 0.95 * self.chladniplate + 0.05 *self.norm_diff
        self.chladniplate = np.clip(self.chladniplate,0,255)
        # print("chladni max", np.max(self.chladniplate))
        
    def step(self):
        self.updateAct()
        self.updateV()
        self.updateP()
        self.updateCp()
        self.frame += 1


argc = len(sys.argv)
if argc > 1 and sys.argv[1] == '1':
    wall = [[1 if x == wall_x_pos and wallTop < y < size_y else 0
             for x in range(size_x)] for y in range(size_y)]
    print(wall)
elif argc > 1 and sys.argv[1] == '2':
    wall = [[1 if (x == wall_x_pos and wallTop + scale < y < size_y) or
                  (wall_x_pos - scale < x < wall_x_pos and
                   x - wall_x_pos == y - wallTop - scale - 1) or
                  (wall_x_pos < x < wall_x_pos + scale and
                   x - wall_x_pos == -y + wallTop + scale + 1)
             else 0
             for x in range(size_x)] for y in range(size_y)]
elif argc>1 and sys.argv[1] =='3': #square
    wall = np.zeros((size_x,size_y))
    for i in range(50,250):
        wall[50][i] = 1
        wall[i][50] = 1
        wall[250][i] = 1
        wall[i][250] = 1

else:
    wall = [[1 if (x == wall_x_pos and wallTop + scale < y < size_y) or
                  (wall_x_pos - scale < x < wall_x_pos and
                   x - wall_x_pos == y - wallTop - scale - 1) or
                  (wall_x_pos < x < wall_x_pos + scale and
                   x - wall_x_pos == -y + wallTop + scale + 1) or
                  (wall_x_pos - 0.75 * scale < x < wall_x_pos - scale / 2 and
                   x - wall_x_pos == -y + wallTop - scale / 2 + 1) or
                  (wall_x_pos + scale / 2 < x < wall_x_pos + 0.75 * scale and
                   x - wall_x_pos == y - wallTop + scale / 2 - 1)
             else 0
             for x in range(size_x)] for y in range(size_y)]

class Actuator:
    def __init__(self,init_speed,init_phase,init_amplitude):
        self.speed = init_speed
        self.phase = init_phase
        self.amplitude = init_amplitude
    def output(self,frame):
        return self.amplitude * sin(self.speed* frame + self.phase)
