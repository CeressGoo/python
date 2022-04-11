import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 50)
y = (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))
print(y)

plt.plot(x, y)
plt.show()