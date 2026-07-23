import asyncio
import pygame
import random
import sys
from settings import *

class ArtMinigame:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.state = "playing"

        # Chalkboard background
        self.background = pygame.image.load("assets/chalkboard.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # Chalk font
        self.font_big = pygame.font.Font("assets/fonts/Chalk Board.otf", 60)
        self.font_small = pygame.font.Font("assets/fonts/Chalk Board.otf", 40)

        self.score = 0
        self.question_number = 0
        self.total_questions = 10

        self.feedback = ""
        self.feedback_color = (255,255,255)
        self.feedback_time = 0
        self.feedback_duration = 800
        self.questions = [
            {
                "image": "assets/art_silhouettes/paintbrush.png",
                "options": ["Paintbrush", "Pencil", "Marker", "Crayon"],
                "answer": 1
            },
            {
                "image": "assets/art_silhouettes/palette.png",
                "options": ["Shield", "Plate", "Palette", "Mask"],
                "answer": 3
            },
            {
                "image": "assets/art_silhouettes/statue.png",
                "options": ["Trophy", "Lamp", "Vase", "Statue"],
                "answer": 4
            },
            {
                "image": "assets/art_silhouettes/vase.png",
                "options": ["Cup", "Bottle", "Vase", "Jar"],
                "answer": 3
            },
            {
                "image": "assets/art_silhouettes/guitar.png",
                "options": ["Guitar", "Violin", "Banjo", "Ukulele"],
                "answer": 1
            },
            {
                "image": "assets/art_silhouettes/sonic cameo.png",
                "options": ["Mario", "Sonic", "Knuckles", "Pikachu"],
                "answer": 2
            },
            {
                "image": "assets/art_silhouettes/bird.png",
                "options": ["Alligator", "Eagle", "Ostrich", "Bird"],
                "answer": 4
            },
                        {
                "image": "assets/art_silhouettes/butterfly.png",
                "options": ["Caterpillar", "Beetle", "Butterfly", "Moth"],
                "answer": 3
            },
                        {
                "image": "assets/art_silhouettes/deer.png",
                "options": ["Moose", "Deer", "Bear", "Rudolph"],
                "answer": 2
            },
                        {
                "image": "assets/art_silhouettes/elephant.png",
                "options": ["Lion", "Zebra", "Giraffe", "Elephant"],
                "answer": 4
            },
        ]

        random.shuffle(self.questions)
        self.current_question = self.questions[self.question_number]

        # Preload silhouette images
        self.loaded_images = {}
        for q in self.questions:
            img = pygame.image.load(q["image"]).convert_alpha()
            img = pygame.transform.scale(img, (300, 300))
            self.loaded_images[q["image"]] = img

    def next_question(self):
        self.question_number += 1
        if self.question_number >= self.total_questions:
            self.state = "results"
        else:
            self.current_question = self.questions[self.question_number]

    async def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                        choice = int(event.unicode)

                        if choice == self.current_question["answer"]:
                            self.score += 1
                            self.feedback = "Correct!"
                            self.feedback_color = (0,255,0)
                        else:
                            self.feedback = "Incorrect!"
                            self.feedback_color = (255,0,0)

                        self.feedback_time = pygame.time.get_ticks()
                        self.next_question()

            if self.state == "results":
                await self.show_results_screen()
                self.game.minigame_cooldown = True
                return


            # Clear feedback after time
            if self.feedback:
                if pygame.time.get_ticks() - self.feedback_time > self.feedback_duration:
                    self.feedback = ""

            # Draw background
            self.screen.blit(self.background, (0, 0))

            # Draw silhouette image
            silhouette = self.loaded_images[self.current_question["image"]]
            self.screen.blit(silhouette, (WIDTH//2 - 150, 120))

            # Draw options
            for i, option in enumerate(self.current_question["options"], start=1):
                opt_surf = self.font_small.render(f"{i}. {option}", True, (255,255,255))
                self.screen.blit(opt_surf, (70, 450 + i * 50))

            #draw instructions
            inst_surf = self.font_small.render("Press 1, 2, 3 or 4 to guess a silhouette. Complete 10.", True, (255, 255, 255))
            self.screen.blit(inst_surf, (20, HEIGHT - 50))

            # Draw feedback
            if self.feedback:
                fb_surf = self.font_small.render(self.feedback, True, self.feedback_color)
                self.screen.blit(fb_surf, (WIDTH//2 - fb_surf.get_width()//2, HEIGHT - 150))

            pygame.display.update()
            self.clock.tick(FPS)
            await asyncio.sleep(0)

    async def show_results_screen(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):

                        #Add score to total score and move to next minigame or final results
                        self.game.total_score += self.score

                        #Advance to next minigame
                        self.game.current_minigame_index += 1

                        if self.game.current_minigame_index < len(self.game.minigames_to_play):
                            self.game.current_target_minigame = self.game.minigames_to_play[self.game.current_minigame_index]
                            self.game.minigame_cooldown = True
                            self.game.state = "overworld"
                        else:
                            self.game.state = "final_results"
                        return

            self.screen.blit(self.background, (0, 0))

            title = self.font_big.render("Art Minigame Complete!", True, (255,255,255))
            self.screen.blit(title, (WIDTH//2 - 300, HEIGHT//2 - 150))

            result = self.font_big.render(f"Score: {self.score}/{self.total_questions}", True, (255,255,255))
            self.screen.blit(result, (WIDTH//2 - 200, HEIGHT//2 - 50))

            inst = self.font_small.render("Press SPACE to return to the overworld.", True, (255,255,255))
            self.screen.blit(inst, (20, HEIGHT - 50))

            pygame.display.update()
            self.clock.tick(FPS)
            await asyncio.sleep(0)
