import numpy as np
import matplotlib.pyplot as plt

def get_ndist_list(loc=0, scale=100, size=100):
    return np.random.normal(loc=loc, scale=scale, size=size).astype(int).tolist()

def define_x_axis(y_axis):
    half_len = len(y_axis) // 2
    return np.arange(-half_len, half_len).tolist()

def get_y_axis(ndist):
    left_y = sorted(ndist)
    return left_y + left_y[::-1]

def get_curve(x_axis, y_axis, reverse=True):
    y_values = [-y if reverse else y for y in y_axis]
    return list(zip(x_axis, y_values))

if __name__ == "__main__":
    y_axis = get_y_axis(get_ndist_list())
    x_axis = define_x_axis(y_axis)

    plt.plot(x_axis, y_axis)
    plt.show()
