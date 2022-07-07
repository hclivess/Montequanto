from numpy.random import seed
from numpy.random import normal
import matplotlib.pyplot as plt


def get_ndist_list(loc=0, scale=100, size=100):
    """return normal distribution values of given criteria as a list"""
    ndist_raw_list = list(normal(loc=loc, scale=scale, size=size))
    ndist_int = [int(item) for item in ndist_raw_list]
    return ndist_int


def define_x_axis(y_axis):
    """get an incremental number with length of y elements mirrored around 0"""
    x_axis = []
    x_axis_moved = []
    for entry in enumerate(y_axis):
        x_axis.append(entry[0])

    for entry in x_axis:
        x_axis_moved.append(int(entry-0.5*len(x_axis)))
    return x_axis_moved


def get_y_axis(ndist):
    """mirror values around 0"""
    left_y = ndist.copy()
    left_y.sort()

    right_y = left_y.copy()
    right_y.reverse()

    y_axis = left_y + right_y
    return y_axis

def get_curve(x_axis, y_axis, reverse=True):
    """glue x and y together"""
    if reverse:
        return list(zip(x_axis, [-y for y in y_axis]))
    else:
        return list(zip(x_axis, y_axis))

if __name__ == "__main__":
    y_axis = get_y_axis(ndist=get_ndist_list())
    x_axis = define_x_axis(y_axis)

    plt.plot(x_axis, y_axis)
    plt.show()