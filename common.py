import numpy as np
from matplotlib.colors import hsv_to_rgb
from expressions import mkexpr
import pygame
from contextlib import contextmanager


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


def save(image, fname='vision.png'):
    s = pygame.Surface((image.shape[0], image.shape[1]))
    pygame.surfarray.blit_array(s, make255(image))
    pygame.image.save(s, fname)


def make255(c):
    return 255 * abs(c)


@contextmanager
def pygamecontext():
    pygame.init()
    yield
    pygame.quit()


class RenderApp:
    app = 'Visions'
    name = ''

    def __init__(self, size, fps, mode):
        shape = makeshape(size)
        self.screen = pygame.display.set_mode(shape)
        pygame.display.set_caption('{} - {}'.format(self.app, self.name))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.mode = mode
        self.X, self.Y = mkXY(shape)
        self.X = self.X.T
        self.Y = self.Y.T
        self.running = False

    def _events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.key_events(event.key)
            self.other_events(event)

    def key_events(self, key):
        if key == pygame.K_q:
            self.running = False
            print('Quitting...')
        if key == pygame.K_h:
            print(self.show_help())

    def other_events(self, event):
        pass

    def update(self):
        pass

    def drawn_image(self):
        raise NotImplementedError

    def draw(self):
        pygame.surfarray.blit_array(self.screen, make255(self.drawn_image()))
        pygame.display.flip()

    def run(self):
        self.running = True
        with pygamecontext():
            while self.running:
                self.clock.tick(self.fps)
                self._events()
                self.update()
                self.draw()

    def show_help(self):
        print('Q: quit')
        print('H: show this help')
