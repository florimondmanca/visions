from common import mkXY, color, make255, RenderApp
import pygame


class App(RenderApp):
    name = 'Stills'

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.c = color(self.X, self.Y, self.mode)

    def drawn_image(self):
        return self.c

    def key_events(self, key):
        if key == pygame.K_RETURN:
            self.c = color(self.X, self.Y, self.mode)
        if key == pygame.K_s:
            pygame.image.save(self.screen, 'vision.png')
            print('Image saved')

    def show_help():
        print('Enter: change vision')
        print('S: save')
        super().show_help()


if __name__ == '__main__':
    App(size=(800, 600), fps=30, mode='rgb').run()
