import asyncio
import pygame, sys
import random
from settings import *
from level import Level
from math_minigame import MathMinigame
from english_minigame import EnglishMinigame
from history_minigame import HistoryMinigame
from geo_minigame import GeographyMinigame
from science_minigame import ScienceMinigame
from art_minigame import ArtMinigame
from music_minigame import MusicMinigame

class Game:
    def __init__(self):

        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('QHHS')
        self.clock = pygame.time.Clock()

        self.state = "title"
        self.minigame_cooldown = False

        self.background = pygame.image.load("assets/qhhs.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.font_big = pygame.font.Font("assets/fonts/Pixel Game.otf", 95)
        self.font_small = pygame.font.Font("assets/fonts/Pixel Game.otf", 40)

        self.minigame_state_map = {
            "minigame1": "minigame1",
            "minigame2": "minigame2",
            "minigame3": "minigame3",
            "minigame4": "minigame4",
            "minigame5": "minigame5",
            "minigame6": "minigame6",
            "minigame7": "minigame7"
        }

        self.minigame_subject_map = {
            "minigame1": "Mathematics",
            "minigame2": "English",
            "minigame3": "History",
            "minigame4": "Geography",
            "minigame5": "Science",
            "minigame6": "Art",
            "minigame7": "Music"
        }

        self.minigames_to_play = random.sample(
            list(self.minigame_state_map.keys()), 5
        )
        self.all_minigames = list(self.minigame_state_map.values())
        self.current_minigame_index = 0
        self.current_target_minigame = self.minigames_to_play[0]

        self.level = Level(self)
        self.total_score = 0

        self.ui_font = pygame.font.Font("assets/fonts/Pixel Game.otf", 40)

    def run_title_screen(self):
        self.screen.blit(self.background, (0, 0))

        #Fade in
        if not hasattr(self, "title_alpha"):
            self.title_alpha = 255

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(self.title_alpha)
        self.screen.blit(overlay, (0, 0))

        if self.title_alpha > 0:
            self.title_alpha -= 3

        # Title text
        title = self.font_big.render("The QUAKERS HILL HIGH SCHOOL Game", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

        # Shadow
        shadow = self.font_big.render("The QUAKERS HILL HIGH SCHOOL Game", True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 2 - 97))

        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)

        # Prompt text
        prompt = self.font_small.render("Press SPACE to Start", True, (255, 255, 255))
        prompt_shadow = self.font_small.render("Press SPACE to Start", True, (0, 0, 0))

        prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        prompt_shadow_rect = prompt.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 2 + 53))

        self.screen.blit(prompt_shadow, prompt_shadow_rect)
        self.screen.blit(prompt, prompt_rect)

        # Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.state = "overworld"

    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.state == "title":
                self.run_title_screen()

            elif self.state == "overworld":
                self.run_overworld()

            elif self.state == "minigame1":
                await MathMinigame(self).run()

            elif self.state == "minigame2":
                await EnglishMinigame(self).run()

            elif self.state == "minigame3":
                await HistoryMinigame(self).run()

            elif self.state == "minigame4":
                await GeographyMinigame(self).run()

            elif self.state == "minigame5":
                await ScienceMinigame(self).run()

            elif self.state == "minigame6":
                await ArtMinigame(self).run()

            elif self.state == "minigame7":
                await MusicMinigame(self).run()

            elif self.state == "final_results":
                await self.show_final_results()

            pygame.display.update()
            self.clock.tick(FPS)
            await asyncio.sleep(0)   # yields to the browser each frame

    def run_overworld(self):
        self.screen.fill('black')
        self.level.run()

    def run_minigame1(self):
        self.screen.fill((30, 30, 30))
        font = pygame.font.Font(None, 50)
        text = font.render("MATHEMATICS", True, 'White')
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)

    async def show_final_results(self):
        running = True

        if self.total_score >= 50:
            rank = "A"
        elif self.total_score >= 40:
            rank = "B"
        elif self.total_score >= 30:
            rank = "C"
        elif self.total_score >= 20:
            rank = "D"
        else:
            rank = "F"

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.reset_game()
                        return

            self.screen.blit(self.background, (0,0))

            title = self.font_big.render("Day Complete!", True, (255,255,255))
            self.screen.blit(title, (WIDTH//2 - 300, 150))

            score_text = self.font_big.render(f"Total Score: {self.total_score}", True, (255, 255, 255))
            self.screen.blit(score_text, (WIDTH//2 - 250, 300))

            rank_text = self.font_big.render(f"Rank: {rank}", True, (255, 255, 255))
            self.screen.blit(rank_text, (WIDTH//2 - 150, 400))

            inst = self.font_small.render("Press SPACE to play again", True, (255, 255, 255))
            self.screen.blit(inst, (WIDTH//2 - 200, 550))

            pygame.display.update()
            self.clock.tick(FPS)
            await asyncio.sleep(0)   # yields to the browser each frame

    def reset_game(self):
        self.total_score = 0
        self.current_minigame_index = 0
        self.minigames_to_play = random.sample(self.all_minigames, 5)
        self.current_target_minigame = self.minigames_to_play[0]
        self.state = "overworld"

async def main():
    game = Game()
    await game.run()

if __name__ == '__main__':
    asyncio.run(main())
