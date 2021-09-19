import math
import os
from random import randrange
from bisect import bisect_left
from numpy import equal

os.system("cls")

v = 800 # m/s
a = 0 # deg
x = 0 # m
y = 4000 # m
p = -0.00015*y+1.225 # kg/m^3
C = 0.29
A = 0.02 # m^2 # 7.62 : 4.806442e-5, 
m = 130 # kg
g = 9.8067 # m/s^2
timestep = 0.005# s
time = 0 # s

mach_numbers_G7 = {
    0 : 0.23, 0.4: 0.229, 0.5 : 0.2,
    0.6 : 0.171, 0.7 : 0.164, 0.8: 0.144,
    0.825 : 0.141, 0.85 : 0.137, 0.875 : 0.137,
    0.9 : 0.142, 0.925 : 0.154, 0.95 : 0.177,
    0.975 : 0.236, 1 : 0.306, 1.025 : 0.334,
    1.05 : 0.341, 1.075 : 0.345, 1.1 : 0.347,
    1.15 : 0.348, 1.2 : 0.348, 1.3 : 0.343,
    1.4	: 0.336, 1.5 : 0.328, 1.6	: 0.321,
    1.8	 : 0.304, 2 : 0.292, 2.2 : 0.282,
    2.4	: 0.27
}
G7_keys = list(mach_numbers_G7.keys())

class Trajectory:
    angle = 0
    pos_points = []
    v_points = []
    time = 0
    apex = (0, 0)

    def __init__(self, angle):
        self.angle = angle

    def add_pos_point(self, point):
        self.pos_points.append(point)

    def add_v_point(self, point):
        self.v_points.append(point)
    
    def set_time(self, t):
        self.time = t

    def d_final(self):
        return self.pos_points[-2][0]

    def v_final(self, v_point):
        return round(components_to_v(v_point[0], v_point[1]), 1)

    def make_copy(self):
        copy = Trajectory(self.angle)
        copy.pos_points = self.pos_points.copy()
        copy.v_points = self.v_points.copy()
        copy.time = self.time
        return copy

    def print_data(self):
        print("Angle:", str(round(self.angle, 3)) + "°", 
              "Range:", round(self.pos_points[-2][0], 1), 
              "Time:", self.time,
              "Final Velocity:", self.v_final(self.v_points[-2]),
              "Apex Height:", round(self.apex[1], 1), "Apex Distance:", round(self.apex[0], 1))

def v_to_components(v, a):
    vy = v*math.sin(math.radians(a))
    vx = v*math.cos(math.radians(a))
    return vx, vy

def components_to_v(vx, vy):
    return math.sqrt(vx**2 + vy**2)

def Cd_G7(v):
    mach_v = v / 343
    return mach_numbers_G7[take_closest(G7_keys, mach_v)]

def Cd_G1(v):
    mach_v = v / 343
    mach_numbers = {
        (0, 0.3) : 0.25,
        (0.3, 0.7) : 0.13,
        (0.7, 0.8) : 0.17,
        (0.8, 0.9) : 0.35,
        (0.9, 0.95) : 0.43,
        (0.95, 1) : 0.475,
        (1, 1.05) : 0.55,
        (1.05, 1.1) : 0.607,
        (1.1, 1.15) : 0.614,
        (1.15, 1.2) : 0.616,
        (1.2, 1.5) : 0.612,
        (1.5, 1.75) : 0.59,
        (1.75, 2) : 0.57,
        (2, 2.5) : 0.55,
        (2.5, 3) : 0.525,
        (3, 3.5) : 0.51,
        (4, 4.5) : 0.495
    }

    for i in mach_numbers.keys():
        if i[0] <= mach_v <= i[1]:
            return mach_numbers[i]
        
def take_closest(myList, myNumber):
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before

def convert_deg_to_mils(deg):
    return deg * 17.777778

def calculate_trajectory(a, v, x, y, p, C, A, m, g, timestep, time):
    vx, vy = v_to_components(v, a)
    trajectory = Trajectory(a)
    trajectory.pos_points.clear()
    trajectory.add_pos_point((x, y))
    trajectory.add_v_point((vx, vy))
    while vy >= 0:
        p = -0.00015*y+1.225
        x += vx*timestep
        y += vy*timestep
        C = Cd_G7(components_to_v(vx, vy))
        vx -= ((p*C*A*vx**2)/(2*m))*timestep
        vy -= ((p*C*A*vy**2)/(2*m))*timestep+(g*timestep)
        time += timestep
        trajectory.add_v_point((vx, vy))
        trajectory.add_pos_point((x, y))
        trajectory.apex = (x, y) if y > trajectory.apex[1] else trajectory.apex

    while y > 0:
        p = -0.00015*y+1.225
        x += vx*timestep
        y += vy*timestep
        C = Cd_G7(components_to_v(vx, vy))
        vx -= ((p*C*A*vx**2)/(2*m))*timestep
        vy -= -((p*C*A*vy**2)/(2*m))*timestep+(g*timestep)
        time += timestep
        trajectory.add_v_point((vx, vy))        
        trajectory.add_pos_point((x, y))
        trajectory.apex = (x, y) if y > trajectory.apex[1] else trajectory.apex

    trajectory.set_time(round(time, 1))
    return trajectory

def findAngle(d, high, low, ang, tolerance, counter):
    #print(high, low)
    traj = calculate_trajectory(ang, v, x, y, p, C, A, m, g, timestep, time)
    #traj.print_data()

    if counter <= 0 or abs(d - traj.d_final()) < d * tolerance:
        return traj

    if traj.d_final() < d:
        low = ang
        return findAngle(d, high, low, ang + (high-low) / 2, 0.01, counter-1)
    else:
        high = ang
        return findAngle(d, high, low, ang - (high-low) / 2, 0.01, counter-1)     
        

