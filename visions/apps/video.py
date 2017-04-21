from .animated import App
from imageio import mimwrite
import pygame
import click


@click.command()
@click.option('--size', default=(512, 1024), help='Canvas size (h, w) - px')
@click.option('--freq', default=.1, help='oscillation frequency - Hz')
@click.option('--fps', default=10, help='FPS for the animation')
@click.option('--filename', default='visions.mp4', help='Export filename')
def main(size, freq, fps, filename):
    app = App(pygame.Surface(size), fps=fps, freq=freq)
    images = []
    with app:
        print('rendering images...')
        for step in range(int(app.timer.period * fps)):
            app.update()
            app.draw(flip=False)
            images.append(pygame.surfarray.array3d(app.screen))
        print('successfully rendered images')
    print('making animation...')
    mimwrite('renders/videos/' + filename, images, fps=fps)
    print('successfully created animation')
