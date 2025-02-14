import pygame, sys

from singleton import Singleton
from camera import Camera
from player import Player
from level import Level
import settings as config
from button import Button

class Game(Singleton):
    def __init__(self) -> None:
        self.__alive = True
        self.window = pygame.display.set_mode(config.DISPLAY, config.FLAGS)
        self.clock = pygame.time.Clock()

        self.camera = Camera()
        self.lvl = Level()
        self.player = Player(
            config.HALF_XWIN - config.PLAYER_SIZE[0] / 2,
            config.HALF_YWIN + config.HALF_YWIN / 2,
            *config.PLAYER_SIZE,
            config.PLAYER_COLOR
        )

        self.score = 0
        self.score_txt = config.SMALL_FONT.render("0 m", 1, config.GRAY)
        self.score_pos = pygame.math.Vector2(10, 10)

        self.gameover_txt = config.SMALL_FONT.render("Press Enter to Restart", 2, config.GRAY)
        self.gameover_rect = self.gameover_txt.get_rect(center=(config.HALF_XWIN, config.HALF_YWIN))

        # New menu attributes
        self.in_menu = True
        self.start_button = Button("START", 200, 50, (config.HALF_XWIN - 100, config.HALF_YWIN), 5)

        # Background music
        pygame.mixer.music.load(config.BG_MUSIC)
        pygame.mixer.music.play(-1)

    def close(self):
        self.__alive = False

    def reset(self):
        self.camera.reset()
        self.lvl.reset()
        self.player.reset()

    def _event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.close()
                if event.key == pygame.K_RETURN and self.player.dead:
                    self.reset()
            
            if self.in_menu:
                if self.start_button.check_click():
                    self.in_menu = False
            else:
                self.player.handle_event(event)

    def _update_loop(self):
        if not self.in_menu:
            self.player.update()
            self.lvl.update()
            if not self.player.dead:
                self.camera.update(self.player.rect)
                self.score = -self.camera.state.y // 50
                self.score_txt = config.SMALL_FONT.render(f"{self.score} m", 1, config.GRAY)

    def _render_loop(self):
        self.window.fill(config.WHITE)
        
        if self.in_menu:
            title = config.LARGE_FONT.render("DoodleJump", True, config.GRAY)
            title_rect = title.get_rect(center=(config.HALF_XWIN, config.HALF_YWIN - 100))
            self.window.blit(title, title_rect)
            self.start_button.draw(self.window)
        else:
            self.lvl.draw(self.window)
            self.player.draw(self.window)
            if self.player.dead:
                self.window.blit(self.gameover_txt, self.gameover_rect)
            self.window.blit(self.score_txt, self.score_pos)
        
        pygame.display.update()
        self.clock.tick(config.FPS)

    def run(self):
        while self.__alive:
            self._event_loop()
            self._update_loop()
            self._render_loop()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
