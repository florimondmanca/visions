import numpy as np
from .app import RenderApp
import pygame
import click


class Timer:

    def __init__(self, fps, freq):
        self.t = 0
        self.fps = fps
        self.freq = freq
        self.period = 1 / self.freq
        self.dt = 1 / self.fps

    def tick(self):
        self.t += self.dt

    def accelerate(self, df=.1):
        self.freq = min(self.freq + df, self.fps // 2)
        self.period = 1 / self.freq
        print('Timer freq:', self.freq)

    def slowdown(self, df=.1):
        self.freq = max(0, self.freq - df)
        self.period = 1 / self.freq
        print('Timer freq:', self.freq)

    @property
    def cost(self):
        return .5 * (1 + np.cos(2 * np.pi * self.freq * self.t * np.ones(3)))


class App(RenderApp):
    name = "Warps"

    def __init__(self, *args, freq=.1, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.c1, self.c2 = self.render(2)
        self.timer = Timer(self.fps, freq)
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
        return self.c1 + self.timer.cost * (self.c2 - self.c1)

    def show_help(self):
        print('Enter: change figure')
        print('Space bar: toggle warping')
        print('Up or down: increase or decrease warping frequency')
        super().show_help()


@click.command()
@click.option('--size', default=(1024, 512), help='Canvas size (h, w) - px')
@click.option('--freq', default=.1, help='Oscillation frequency - Hz')
@click.option('--fps', default=30, help='Animation fps')
def main(size, freq, fps):
    screen = pygame.display.set_mode(size)
    App(screen, fps=fps, freq=freq).run()
