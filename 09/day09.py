import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

with open("09/input.txt") as f:
    data = f.read().strip().splitlines()
    points = [[int(c) for c in line.split(",")] for line in data]
points = np.array(points)


def manhattan(a, b):
    return np.abs(a - b).sum()


def area(a, b):
    diff = b - a
    return (np.abs(diff[0]) + 1) * (np.abs(diff[1]) + 1)


def part_a(points: np.ndarray) -> list[tuple[int, int, int, int]]:
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]

    areas = []
    for idx, p0 in enumerate(hull_points):
        for jdx, p1 in enumerate(hull_points[(idx + 1) :]):
            areas.append((idx, jdx + idx + 1, manhattan(p0, p1), area(p0, p1)))

    areas = sorted(areas, key=lambda x: x[2], reverse=True)
    return areas


print("Part A)", part_a(points)[0])

plt.plot(points[:, 0], points[:, 1], "-o", color="tab:orange")
plt.fill(points[:, 0], points[:, 1], color="tab:green", alpha=0.5)
plt.savefig("09/plot.png")
plt.show()

# solve semi-visually by looking at the plot
# the shape is an ellipse with noise and a horizontal cut around the major axis from the left.
# symmetry forces the biggest area to be based on one of the two points that cut into the ellipse
# they define the right lower or right upper corner of the biggest area respectively.
# by looking at the linesegments right below or above these points we can figure out what the y-value
# for the other corner of the area can be maximally/minimally (depending on whether the largest upper area or the largest lower area is bigger)
# we then just check the area for all rectangles defined by one of these two points and all points with y values between the boundary [lower, 32214] or [66751, higher]
# and x values smaller than the lower/upper point
# by constraining one point to one of the two potential points, the check only needs to be done on
# a small subset of all points
# this can be checked by brute force.

distances_to_next_point = [
    manhattan(points[i], points[(i + 1) % len(points)]) for i in range(len(points))
]
# get the points in the middle of the ellipse
max_distance_idx = np.argmax(distances_to_next_point)
p0 = points[max_distance_idx]
p1 = points[(max_distance_idx - 1) % len(points)]

# one of thes two points needs to be in the biggest area
# check the lower one with smaller y value
if p0[1] < p1[1]:
    lower_point = p0
    higher_point = p1
else:
    lower_point = p1
    higher_point = p0

# potential other point is the smallest x value that has a lower y-value than the lowest point
# and higher y value than 32214

potential_other_points = points[
    (points[:, 1] < lower_point[1]) & (points[:, 1] >= 32214)
]

areas = []
for other_point in potential_other_points:
    areas.append(area(lower_point, other_point))


# do the same for the highest point

potential_other_points = points[
    (points[:, 1] > higher_point[1]) & (points[:, 1] <= 66751)
]
for other_point in potential_other_points:
    areas.append(area(higher_point, other_point))


print("Part B)", max(areas))
