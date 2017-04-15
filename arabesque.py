import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from expressions import mkexpr
from scipy.misc import imresize
import pygame


def mkXY(size):
    x, y = np.linspace(-1, 1, size), np.linspace(-1, 1, size)
    return np.meshgrid(x, y)


def color(X, Y, mode='rgb', show_expr=False):
    """
    Returns a colored array.
    Color channels are generated through random sin/cos expressions.
    All values in array are between 0 and 1.

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
    TF = {
        'rgb': lambda a: a,
        'hsv': lambda a: 2 * hsv_to_rgb(.5 * (1 + a)) - 1,
    }
    a, b, c = mkexpr(), mkexpr(), mkexpr()  # channels
    channels = [a, b, c]
    labels = LABELS[mode]
    if show_expr:
        for label, channel in zip(labels, channels):
            print('{}:'.format(label), channel)
    return TF[mode](np.dstack((channel(X, Y) for channel in channels)))


def binarize(c, step=.1):
    return step * np.round(c / step)


def smooth(image):
    return imresize(image, 1., interp='nearest')


def show(image):
    plt.imshow(image, interpolation='nearest')
    plt.show()


def save(image, fname='arabesque.png'):
    s = pygame.Surface((image.shape[0], image.shape[1]))
    pygame.surfarray.blit_array(s, make255(image))
    pygame.image.save(s, fname)


def saveall(image):
    save(image, fname='original.png')
    save(smooth(image), fname='smoothed.png')


def weight(c, weights):
    return c * np.array(weights)


def warp(c1, c2, t):
    return c1 + t * (c2 - c1)


def make255(c):
    return 255 * abs(c)


def animate_w(size, mode='rgb', fps=30):
    def rand(shape):
        return 2 * np.random.random(shape) - 1

    def show_help():
        print('Enter: change figure')
        print('Space bar: toggle flickering')
        print('R, G or B: focus on red, green or blue channel')
        print('Backspace: focus all channels')
        print('Up or down: increase or decrease flickering speed')
        print('Q: quit')
        print('H: show this help')
    X, Y = mkXY(size)
    c = color(X, Y, mode)
    w = np.array([1, 1, 1])
    speed = .05
    flicker = True
    try:
        screen = pygame.display.set_mode((size, size))
        clock = pygame.time.Clock()
        show_help()
        running = True
        while running:
            clock.tick(fps)
            # make the weights vary slightly
            w = np.clip(w + flicker * speed * rand(w.shape), 0, 1)
            pygame.surfarray.blit_array(screen, make255(weight(c, w)))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        c = color(X, Y, mode)
                    if event.key == pygame.K_SPACE:
                        flicker = not flicker
                        print('flickering ' + ('on' if flicker else 'off'))
                    if event.key == pygame.K_UP:
                        speed = min(speed + .05, .5)
                        print('flickering speed:', speed)
                    if event.key == pygame.K_DOWN:
                        speed = max(speed - .05, 0)
                        print('flickering speed:', speed)
                    if event.key == pygame.K_BACKSPACE:
                        w[:] = (1, 1, 1)
                        print('all channels focused')
                    if event.key == pygame.K_r:
                        w[:] = (1, 0, 0)
                        print('red channel focused')
                    if event.key == pygame.K_g:
                        w[:] = (0, 1, 0)
                        print('green channel focused')
                    if event.key == pygame.K_b:
                        w[:] = (0, 0, 1)
                        print('blue channel focused')
                    if event.key == pygame.K_h:
                        show_help()
                    if event.key == pygame.K_q:
                        running = False
                        print('quitting')
    finally:
        pygame.quit()


def saver(size, mode='rgb', fps=30):
    def show_help():
        print('Enter: change figure')
        print('S: save')
        print('Q: quit')
        print('H: show this help')
    X, Y = mkXY(size)
    c = color(X, Y, mode=mode)
    try:
        screen = pygame.display.set_mode((size, size))
        clock = pygame.time.Clock()
        show_help()
        running = True
        while running:
            clock.tick(fps)
            pygame.surfarray.blit_array(screen, make255(c))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        c = color(X, Y, mode)
                    if event.key == pygame.K_s:
                        pygame.image.save(screen, 'arabesque_s.png')
                        print('Image saved')
                    if event.key == pygame.K_h:
                        show_help()
                    if event.key == pygame.K_q:
                        running = False
                        print('quitting')
    finally:
        pygame.quit()


def animate_t(size, mode='rgb', fps=30):
    def rand(shape):
        return 2 * np.random.random(shape) - 1

    def ti(i, n):
        t = i * np.pi / n * np.ones(3)
        return .5 * (1 + np.sin(t))

    def show_help():
        print('Enter: change figure')
        print('Space bar: toggle warping')
        print('Up or down: increase or decrease warping speed')
        print('Q: quit')
        print('H: show this help')
    X, Y = mkXY(size)
    c1 = color(X, Y, mode)
    c2 = color(X, Y, mode)
    n = 3 * fps
    i = 0
    t = ti(i, n)
    warping = True
    speed = 1
    try:
        screen = pygame.display.set_mode((size, size))
        clock = pygame.time.Clock()
        show_help()
        running = True
        while running:
            clock.tick(fps)
            # lerp the image between c1 and c2
            i += warping * speed
            t = ti(i, n)
            pygame.surfarray.blit_array(screen, make255(warp(c1, c2, t)))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        c1 = color(X, Y, mode)
                        c2 = color(X, Y, mode)
                    if event.key == pygame.K_SPACE:
                        warping = not warping
                        print('warping ' + ('on' if warping else 'off'))
                    if event.key == pygame.K_UP:
                        speed = min(speed + 1, n // 4)
                        print('warping speed:', speed)
                    if event.key == pygame.K_DOWN:
                        speed = max(speed - 1, 0)
                        print('warping speed:', speed)
                    if event.key == pygame.K_h:
                        show_help()
                    if event.key == pygame.K_q:
                        running = False
                        print('quitting')
    finally:
        pygame.quit()


if __name__ == '__main__':
    plt.ion()
