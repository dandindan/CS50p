import numpy as np
import matplotlib.pyplot as plt

# create some sample data with 3 dimensions
data = np.random.rand(10, 3)

# plot each line as a series of dots
for i in range(data.shape[0]):
    x = data[i, 0]
    y = data[i, 1]
    z = data[i, 2]
    plt.scatter(x, y, z)

# set the axis labels and title
plt.set_xlabel('X')
plt.set_ylabel('Y')
plt.set_zlabel('Z')
plt.title('Multi-Dimensional Plot')

# show the plot
plt.show()
