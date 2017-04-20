from core.common import mkXY, make255, color
import pygame


class RenderApp:
    app = 'Visions'
    name = ''

    def __init__(self, screen, fps, mode='rgb'):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.mode = mode
        self.X, self.Y = mkXY(self.screen.get_size())
        self.running = False

    def __enter__(self):
        pygame.init()
        self.running = True

    def __exit__(self, *args):
        pygame.quit()

    def render(self, size=1):
        if size == 1:
            return color(self.X, self.Y, self.mode)
        renders = []
        for _ in range(size):
            renders.append(color(self.X, self.Y, self.mode))
        return renders

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

    def draw(self, flip=True):
        pygame.surfarray.blit_array(self.screen, make255(self.drawn_image()))
        if flip:
            pygame.display.flip()

    def run(self, flip=True):
        with self:
            while self.running:
                self.clock.tick(self.fps)
                self._events()
                self.update()
                self.draw()

    def show_help(self):
        print('Q: quit')
        print('H: show this help')
