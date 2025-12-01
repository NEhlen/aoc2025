with open("input.txt") as f:
    lines = f.readlines()
    print(f"Number of lines: {len(lines)}")

num_zeros_A = 0
num_zeros_B = 0

pointer = 50
for line in lines:
    add = int(line[1:])
    mult = 1
    if line[0] == "L":
        mult *= -1

    # check how often pointer goes over zero on rotations
    n = add // 100

    add = add % 100
    new_pointer = pointer + add * mult
    if new_pointer >= 100:
        n += 1
    elif new_pointer <= 0 and pointer != 0:
        n += 1

    num_zeros_B += n
    print(
        f"Line: {line.strip()} | Pointer: {pointer} -> {new_pointer} | Zeros crossed: {n}"
    )
    pointer = new_pointer % 100
    if pointer == 0:
        num_zeros_A += 1

print(f"A) Number of times pointer is at 0: {num_zeros_A}")
print(f"B) Number of times pointer crosses 0: {num_zeros_B}")
