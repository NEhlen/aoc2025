import ast

from z3 import Int, Optimize, Sum, sat

inputfile = "10/input.txt"
with open(inputfile) as f:
    lines = f.readlines()

machines = []
for line in lines:
    line = line.strip()
    light_arrangement, line = line.split("]")
    light_arrangement = [b == "#" for b in light_arrangement[1:]]
    buttons, joltage = line.split("{")
    buttons = [ast.literal_eval(b) for b in buttons.split(" ") if b.strip()]
    buttons = [b if type(b) is tuple else (b,) for b in buttons]
    joltage = [int(j) for j in joltage[:-1].split(",")]
    machines.append((light_arrangement, buttons, joltage))


total_A = 0
total_B = 0
for count, machine in enumerate(machines):
    print(f"Processing machine {count + 1} of {len(machines)}")
    light_arrangement, buttons, joltage_requirement = machine
    lights = [False] * len(light_arrangement)

    # find mininum button presses using BFS
    def bfsA(lights, buttons, goal):
        queue = [(lights, 0)]
        seen = set()
        while queue:
            current_lights, steps = queue.pop(0)
            lights_tuple = tuple(current_lights)
            if lights_tuple in seen:
                continue
            seen.add(lights_tuple)
            if current_lights == goal:
                return steps
            for button in buttons:
                new_lights = current_lights[:]
                for idx in button:
                    new_lights[idx] = not new_lights[idx]
                queue.append((new_lights, steps + 1))
        return float("inf")

    presses_A = bfsA(lights, buttons, light_arrangement)
    total_A += presses_A

    presses_A = bfsA(lights, buttons, light_arrangement)
    total_A += presses_A

    # Part B:
    # this is integer linear programming, I'm not going to
    # implement a full ILP solver here, so I'll use Z3
    # Use Optimize instead of Solver to find minimal solution
    opt = Optimize()
    button_vars = [Int(f"b{i}") for i in range(len(buttons))]

    # Each button variable must be non-negative
    for var in button_vars:
        opt.add(var >= 0)

    # For each joltage position, sum of button presses must equal requirement
    for j_idx in range(len(joltage_requirement)):
        # Find which buttons affect this joltage counter
        affecting_buttons = [
            button_vars[b_idx]
            for b_idx, button in enumerate(buttons)
            if j_idx in button
        ]
        if affecting_buttons:
            opt.add(Sum(affecting_buttons) == joltage_requirement[j_idx])
        else:
            # No button affects this counter, so requirement must be 0
            if joltage_requirement[j_idx] != 0:
                presses_B = float("inf")
                break
    else:
        # Minimize total button presses
        opt.minimize(Sum(button_vars))

        if opt.check() == sat:
            model = opt.model()
            presses_B = sum(model[var].as_long() for var in button_vars)
        else:
            presses_B = float("inf")

    total_B += presses_B


print("Solution A) ", total_A)
print("Solution B) ", total_B)
