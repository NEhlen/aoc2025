import numpy as np


with open("06/input.txt") as f:
    data = f.read()
    data = data.split("\n")
    data = [line for line in data if line.strip()]

##### PART A ####
data_A = [line.strip() for line in data if line.strip()]
data_A = [[char for char in line.strip().split(" ") if char] for line in data_A]
operators = np.array(data_A[-1])
numbers = np.array(data_A[:-1], dtype=int)


plus_cols = operators == "+"
mult_cols = operators == "*"


n_rows, m_cols = numbers.shape

results_A = np.empty(m_cols, dtype=int)

results_A[plus_cols] = np.sum(numbers[:, plus_cols], axis=0)
results_A[mult_cols] = np.prod(numbers[:, mult_cols], axis=0)

print("A) ", np.sum(results_A))


##### PART B ####
operators = data[-1]
number_cols = data[:-1]
cur_char = ""
results_B = []
for idx, char in enumerate(operators):
    if char.strip():
        cur_char = char
        cur_nmbr = int("".join([row[idx] for row in number_cols]).strip())
    else:
        try:
            if cur_char == "+":
                cur_nmbr += int("".join([row[idx] for row in number_cols]).strip())
            elif cur_char == "*":
                cur_nmbr *= int("".join([row[idx] for row in number_cols]).strip())
        except ValueError:
            pass
    if idx + 1 == len(operators) or (operators[idx + 1].strip() != ""):
        results_B.append(cur_nmbr)

print(results_B)
print("B) ", sum(results_B))
