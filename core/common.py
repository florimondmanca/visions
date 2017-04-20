import numpy as np
from matplotlib.colors import hsv_to_rgb
from core.expressions import mkexpr


def makeshape(size):
    try:
        size[0], size[1]
        return size[:2]
    except TypeError:
        return (size, size)


def mkXY(shape):
    nx, ny = shape
    x, y = np.linspace(-1, 1, nx), np.linspace(-1, 1, ny)
    return np.meshgrid(x, y)


def color(X, Y, mode='rgb', show_expr=False):
    """
    Returns a colored array.
    Color channels are generated through random sin/cos expressions.
    All values in returned array are between 0 and 1.

    Parameters
    ----------
    X, Y : meshgrid
    mode: 'rgb' | 'hsv'
    show_expr: True | False
    """
    LABELS = {
        'rgb': ('Red', 'Green', 'Blue'),
        'hsv': ('Hue', 'Saturation', 'Value'),
    }
    TRANSF = {
        'rgb': lambda a: a,
        'hsv': lambda a: 2 * hsv_to_rgb(.5 * (1 + a)) - 1,
    }
    a, b, c = mkexpr(), mkexpr(), mkexpr()  # channels
    channels = [a, b, c]
    labels = LABELS[mode]
    if show_expr:
        for label, channel in zip(labels, channels):
            print('{}:'.format(label), channel)
    tf = TRANSF[mode]
    return tf(np.dstack((channel(X, Y) for channel in channels)))


def make255(c):
    return 255 * abs(c)
