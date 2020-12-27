'''
import os
from matplotlib import pyplot as plt

y = []

for file_name in sorted(os.listdir('log')):
    file_name = os.path.join('log', file_name)
    with open(file_name, 'r') as f:
        s = f.read()
        if s[-1] == '\n':
            s = s[:-1]
        s = s.split(' ')[-1]
        y.append(float(s))
x = [i * 100 + 100 for i in range(len(y))]
plt.plot(x, y)
plt.xlabel('number of data')
plt.ylabel('run time')
plt.show()
'''
