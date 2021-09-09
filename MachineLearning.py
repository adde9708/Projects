import numpy as np

import torch

from math import *

from scipy import stats

import matplotlib.pyplot as plt

speed = [100, 80, 130, 111, 96, 110, 90, 94, 86, 150, 120, 144, 146]

rotation = [180, 90, 260, 360, 720, 144, 146, 80, 94, 86, 120, 1080, 333]

weights = torch.randn(53, 43, 6, 4)

inputs = torch.randn(16, 43, 23, 33)

tr = torch.nn.functional.conv2d(inputs, weights)

x = np.mean(speed)

y = stats.mode(speed)

z = np.median(speed)

s = np.std(speed)

p = np.percentile(speed, 90)

v = np.var(speed)

r = np.random.uniform(23, 35, 10000)

print(r)

print(y)

print(x)

print(z)

print(s)

print(v)

print(p)

print(tr)

plt.hist(r)

plt.show()
