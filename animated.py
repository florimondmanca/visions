import numpy as np
from common import color, RenderApp
import pygame


class App(RenderApp):
    """docstring for App."""

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.c1 = color(self.X, self.Y, self.mode)
        self.c2 = color(self.X, self.Y, self.mode)
        self.freq = 1  # Hz
        self._step = 0
        self.nsteps = 100
        self.t = 0
        self.warping = True
        self.step = 0

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        self._step = value
        i, n = self.step, self.nsteps
        t = i / n
        self.t = .5 * (1 + np.sin(2 * np.pi * t * np.ones(3)))

    def key_events(self, key):
        if key == pygame.K_RETURN:
            self.c1 = color(self.X, self.Y, self.mode)
            self.c2 = color(self.X, self.Y, self.mode)
        if key == pygame.K_SPACE:
            self.warping = not self.warping
            print('warping ' + ('on' if self.warping else 'off'))
        if key == pygame.K_UP:
            self.freq = min(self.freq + .25, self.fps // 2)
            print('warping:', self.freq, 'Hz')
        if key == pygame.K_DOWN:
            self.freq = max(self.freq - .25, 0)
            print('warping:', self.freq, 'Hz')

    def update(self):
        self.step += 2 * self.warping * self.freq

    def drawn_image(self):
        return self.c1 + self.t * (self.c2 - self.c1)

    def show_help(self):
        print('Enter: change figure')
        print('Space bar: toggle warping')
        print('Up or down: increase or decrease warping frequency')
        super().show_help()


if __name__ == '__main__':
    App(size=(400, 300), fps=30, mode='rgb').run()
