import numpy as np

with open("03/input.txt") as f:
    lines = f.readlines()

total_A = 0
for line in lines:
    linearr = list(map(int, line.strip()))
    first_idx = np.argmax(linearr[:-1])
    last_idx = np.argmax(linearr[(first_idx + 1) :])
    first = linearr[first_idx]
    last = linearr[first_idx + 1 + last_idx]
    total_A += first * 10 + last

print("Solution A) ", total_A)


total_B = 0
for line in lines:
    linearr = list(map(int, line.strip()))
    digit_idx = -1
    cur_num = 0
    for digit_num in range(12):
        if digit_num == 11:
            digit_idx = np.argmax(linearr[(digit_idx + 1) :]) + digit_idx + 1
        else:
            digit_idx = (
                np.argmax(linearr[(digit_idx + 1) : (-12 + digit_num + 1)])
                + digit_idx
                + 1
            )
        digit = linearr[digit_idx]
        cur_num = cur_num * 10 + digit
    total_B += cur_num
print("Solution B) ", total_B)
