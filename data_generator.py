import numpy as np
import pandas as pd

GRANULARITY = 10
BOX_SIZE = 10
NUM_POINTS = 100

def forward_eq_line(source, point):
    point["x"] = point[0]
    point["y"] = point[1]
    point["z"] = point[2]    
    a = np.vstack([source["x"], source["y"], source["z"]])
    d = np.vstack([source["dirx"], source["diry"],source["dirz"]])
    p = np.vstack([point["x"],point["y"],point["z"]])
    
    mid_point = a + ((p - a)*d/np.linalg.norm(d))*d
    end_point = a + source["len"]*d
                 
    L1 = np.linalg.norm(mid_point - a)
    L2 = np.linalg.norm(end_point - mid_point)
    M  = np.linalg.norm(end_point - mid_point)
    SL = (3.7*(10**10))/(L1+L2)
    calc_dose = (SL/(4*np.pi*M))*(np.arctan(L1/M)+np.arctan(L2/M))*(2.2*(10**-6))*180/np.pi
    return calc_dose


def point_source(source, x, y, z):

    dist = np.linalg.norm([source['x'] - x,
                           source['y'] - y,
                           source['z'] - z])

    return source['C'] * source['E'] / dist ** 2


def line_source_by_summation(source, x, y, z):

    intensity = 0
    for i in range(1, GRANULARITY + 1):
        # print(t)
        t = source["len"] / GRANULARITY
        [sx, sy, sz] = [p + t * i * q for (p, q) in zip([source["x"], source["y"], source["z"]],
                                                        [source["dirx"], source["diry"], source["dirz"]])]

        dist = np.linalg.norm([sx - x, sy - y, sz - z])
        #intensity += ((source['C'] * source['E'] / dist ** 2) / GRANULARITY)
        point["x"] = x
        point["y"] = y
        point["z"] = z
        
        intensity += ((forward_eq_line(source, point) / GRANULARITY)
    return intensity


def line_source_by_formula(source, x, y, z):

    #Acting as if the source contains the end points of the line
    pass


def sphere_source_by_summation(source, x, y, z):

    intensity = 0

if __name__ == '__main__':

    source = {"C": 2,
              "E": 2,
              "x": 0,
              "y": 1,
              "z": 1,
              "dim": 1,
              "dirx": 1,
              "diry": 0,
              "dirz": 0,
              "len": 2}

    l_values = []

    for _ in range(NUM_POINTS):
        (x, y, z) = BOX_SIZE * np.random.rand(3)

        l_values.append({"X": x,
                         "Y": y,
                         "Z": z,
                         "Dose": line_source_by_summation(source, x, y, z),
                         "dim": 1})

    df = pd.DataFrame(l_values)

    df.to_csv('data.csv', index=False)
