from .app import RenderApp
import pygame
import click


class App(RenderApp):
    name = 'Stills'

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.c = self.render()

    def drawn_image(self):
        return self.c

    def key_events(self, key):
        if key == pygame.K_RETURN:
            self.c = self.render()
        if key == pygame.K_s:
            pygame.image.save(self.screen, 'vision.png')
            print('Image saved')

    def show_help():
        print('Enter: change vision')
        print('S: save')
        super().show_help()


@click.command()
@click.option('--size', default=(1024, 512), help='Canvas size (w, h) - px')
@click.option('--fps', default=30, help='Animation fps')
def main(size, fps):
    App(pygame.display.set_mode(size), fps=fps).run()
