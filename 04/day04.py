import scipy.signal as signal
import numpy as np


def convolve_2d_signals(signal1, signal2):
    """
    Convolves two 2D signals using scipy's convolve2d function.

    Parameters:
    signal1 (2D array-like): The first input signal.
    signal2 (2D array-like): The second input signal.

    Returns:
    2D array: The result of convolving signal1 with signal2.
    """
    return signal.convolve2d(signal1, signal2, mode="same")


with open("04/input.txt") as f:
    data = f.readlines()

data = [line.strip() for line in data]
data = np.array([[char for char in line] for line in data])
data = data == "@"
data = data.astype(int)

kernel = np.array(
    [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
)

result = convolve_2d_signals(data, kernel)
result[data != 1] = 0

print("A) ", (result[data == 1] < 4).sum())


iterating = True
removed = 0
while iterating:
    convolved = convolve_2d_signals(data, kernel)
    convolved[data != 1] = 0
    to_remove = (convolved < 4) & (data == 1)
    removed += to_remove.sum()
    data[to_remove] = 0
    if to_remove.sum() == 0:
        iterating = False

print("B) ", removed)
