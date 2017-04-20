import numpy as np
from apps.app import RenderApp
import pygame
from imageio import mimwrite


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
    def sint(self):
        return .5 * (1 + np.sin(2 * np.pi * self.freq * self.t * np.ones(3)))


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
        return self.c1 + self.timer.sint * (self.c2 - self.c1)

    def show_help(self):
        print('Enter: change figure')
        print('Space bar: toggle warping')
        print('Up or down: increase or decrease warping frequency')
        super().show_help()


def makevideo(size, freq=1, dt=.1):
    app = App(pygame.Surface(size), fps=30, freq=freq)
    images = []
    with app:
        print('rendering images...')
        for step in range(int(app.timer.period / app.timer.dt)):
            app.update()
            app.draw(flip=False)
            images.append(pygame.surfarray.array3d(app.screen))
        print('successfully rendered images')
    print('making animation...')
    mimwrite('visions.mp4', images, fps=10)
    print('successfully created animation')


if __name__ == '__main__':
    makevideo((512, 1024))
