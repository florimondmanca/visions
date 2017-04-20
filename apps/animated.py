import numpy as np
from apps.app import RenderApp
import pygame


class Timer:

    def __init__(self, fps, freq):
        self.counter = 0
        self.fps = fps
        self.freq = freq

    def tick(self):
        self.counter += 1 / self.fps

    def accelerate(self, df=.1):
        self.freq = min(self.freq + df, self.fps // 2)
        print('Timer freq:', self.freq)

    def slowdown(self, df=.1):
        self.freq = max(0, self.freq - df)
        print('Timer freq:', self.freq)

    @property
    def t(self):
        return self.counter

    @property
    def sint(self):
        return .5 * (1 + np.sin(2 * np.pi * self.freq * self.t * np.ones(3)))


class App(RenderApp):
    name = "Warps"

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.c1, self.c2 = self.render(2)
        self.timer = Timer(self.fps, freq=0.1)
        self.warping = True

    def key_events(self, key):
        if key == pygame.K_RETURN:
            self.c1, self.c2 = self.render(2)
        if key == pygame.K_SPACE:
            self.warping = not self.warping
            print('warping ' + ('on' if self.warping else 'off'))
        if key == pygame.K_UP:
            self.timer.accelerate()
        if key == pygame.K_DOWN:
            self.timer.slowdown()

    def update(self):
        self.timer.tick()

    def drawn_image(self):
        return self.c1 + self.timer.sint * (self.c2 - self.c1)

    def show_help(self):
        print('Enter: change figure')
        print('Space bar: toggle warping')
        print('Up or down: increase or decrease warping frequency')
        super().show_help()


if __name__ == '__main__':
    App(size=(1024, 600), fps=30, mode='rgb').run()
