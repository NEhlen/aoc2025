import numpy as np

inputfile = "12/input.txt"

with open(inputfile) as f:
    data = f.read().strip()

    chunks = data.split("\n\n")

    shapes, areas = chunks[:-1], chunks[-1]


def parse_shape(shape: str) -> list[tuple[int, int]]:
    lines = shape.splitlines()
    idx = int(lines[0][:-1])
    shape = np.array([[c == "#" for c in line] for line in lines[1:]], dtype=int)
    return idx, shape


def parse_areas(areas: str) -> list[tuple[int, int, list[int]]]:
    area_list = []
    for line in areas.splitlines():
        area, requirements = line.split(": ")
        x, y = area.split("x")
        area_list.append(
            (int(x), int(y), [int(req.strip()) for req in requirements.split(" ")])
        )
    return area_list


shapes = {parse_shape(shape)[0]: parse_shape(shape)[1] for shape in shapes}
areas = parse_areas(areas)


def check_validity(
    shape_dict: dict[str, np.ndarray], area_info: tuple[int, int, list[int]]
) -> bool:
    x, y, requirements = area_info
    area = x * y
    counts = [count * shape_dict[idx].sum() for idx, count in enumerate(requirements)]
    return sum(counts) <= area


valid_areas = 0
for area_info in areas:
    if check_validity(shapes, area_info):
        valid_areas += 1

print("A)", valid_areas)
