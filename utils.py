from random import uniform
from math import log, sqrt, pi, sin, cos

class Boat:
    def __init__(self):
        self.load_time = 0
        self.times     = [0] * 4
        self.type      = gen_boat()
        self.times[0]  = boat_arrival()

    def __lt__(b1, b2):
        return b1.times[0] < b2.times[0]

    def __gt__(b1, b2):
        return b1.times[0] > b2.times[0]

class Port:
    def __init__(self):
        self.docks = [None] * 3

    def available_dock(self):
        for i, d in enumerate(self.docks):
            if d == None:
                return i
        return -1
    
    def refresh_load_times(self, time):
        for b in self.docks:
            if b != None:
                if b.load_time - time > 0:
                    b.load_time -= time
                else:
                    b.load_time = 0
                    b.times[3] = load_time

    def ready_boats(self):
        for i, b in enumerate(self.docks):
            if b != None and b.load_time == 0:
                return i
        return -1

    def avance(self):
        min = 10e6
        for i, b in enumerate(self.docks):
            if b != None and b.load_time < min:
                idx = i
                min = b.load_time
        self.refresh_load_times(min)
        return min

    def __setitem__(self, index, value):
        self.docks[index] = value

    def __getitem__(self, index):
        return self.docks[index]

def gen_exp(lambd):
    u = uniform(0, 1)
    return (-1 / lambd) * log(u)

def gen_normal(m, s):
    u1 = uniform(0, 1)
    u2 = uniform(0, 1)
    z1 = sqrt(-2 * log(u1)) * sin(2 * pi * u2)
    z2 = sqrt(-2 * log(u1)) * cos(2 * pi * u2)
    return m + sqrt(s) * z2

def gen_boat():
    r = uniform(0, 1)
    if r <= 0.25:
        return 0
    if r <= 0.50:
        return 1
    return 2

def boat_arrival():
    return gen_exp(8) * 60

def load_time(boat_type):
   if boat_type == 0:
       return gen_normal(9, 1) * 60
   if boat_type == 1:
       return gen_normal(12, 2) * 60
   return gen_normal(18, 3) * 60

def tugboat_free_ride():
    return gen_exp(15)

def tug_boat_to_dock():
    return gen_exp(2) * 60

def tug_boat_off_dock():
    return gen_exp(1) * 60