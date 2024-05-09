import numpy as np
import matplotlib.pyplot as plt

f = 50 #Hz
x = np.linspace(0, 300e-3, 300)
y = np.copysign(1, np.sin(2 * np.pi * f * x))
y2 = np.sin(2 * np.pi * f * x)

plt.plot(x, y)
#plt.plot(x, y2)
plt.show()
