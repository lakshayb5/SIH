import numpy as np
import pandas as pd

GRANULARITY = 10
BOX_SIZE = 10
NUM_POINTS = 100


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
        intensity += ((source['C'] * source['E'] / dist ** 2) / GRANULARITY)

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
