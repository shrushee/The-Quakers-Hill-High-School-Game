import asyncio
import pygame
import random
import sys
from settings import *

def draw_text_wrapped(surface, text, font, color, x, y, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)  # Add the last line

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * font.get_height() + 5))  # 5 pixels of spacing between lines

class GeographyMinigame:
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
                "question": "What is the capital city of Japan?",
                "options": ["Kyoto", "Tokyo", "Osaka", "Nagoya"],
                "answer": 2
            },
            {
                "question": "Which continent is the Sahara Desert located in?",
                "options": ["Asia", "Africa", "Australia", "South America"],
                "answer": 2
            },
            {
                "question": "Which country has the largest population?",
                "options": ["USA", "India", "China", "Russia"],
                "answer": 3
            },
            {
                "question": "Which landmark is found in Australia?",
                "options": ["Eiffel Tower", "Great Wall", "Sydney Opera House", "Statue of Liberty"],
                "answer": 3
            },
            {
                "question": "Which ocean is the largest?",
                "options": ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean"],
                "answer": 3
            },
            {
                "question": "What is the tallest mountain in the world?",
                "options": ["Mount Everest", "K2", "Kangchenjunga", "Lhotse"],
                "answer": 1
            },
            {
                "question": "What is the largest island in the world?",
                "options": ["Greenland", "New Guinea", "Borneo", "Madagascar"],
                "answer": 1
            },
            {
                "question": "The lines of longitude are:",
                "options": ["Horizontal", "Vertical", "Diagonal", "Curved"],
                "answer": 2
            },
            {
                "question": "Is Australia a continent, country, or island?",
                "options": ["Continent", "Country", "Island", "All of the above"],
                "answer": 4
            },
            {
                "question": "What is the name of the supercontinent that existed 200 million years ago?",
                "options": ["Earth", "Australia", "Pangea", "Mobius"],
                "answer": 3
            }
        ]

        random.shuffle(self.questions)
        self.current_question = self.questions[self.question_number]

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

            # Draw question
            draw_text_wrapped(
            self.screen,
            self.current_question["question"],
            self.font_big,
            (255, 255, 255),
            50,        # x position
            100,       # y position
            WIDTH - 100   # max width before wrapping
        )

            # Draw options
            for i, option in enumerate(self.current_question["options"], start=1):
                opt_surf = self.font_small.render(f"{i}. {option}", True, (255,255,255))
                self.screen.blit(opt_surf, (70, 200 + i * 50))

            #draw instructions
            inst_surf = self.font_small.render("Press 1, 2, 3 or 4 to answer a Geography question. Complete 10.", True, (255, 255, 255))
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

            title = self.font_big.render("Geography Minigame Complete!", True, (255,255,255))
            self.screen.blit(title, (WIDTH//2 - 300, HEIGHT//2 - 150))

            result = self.font_big.render(f"Score: {self.score}/{self.total_questions}", True, (255,255,255))
            self.screen.blit(result, (WIDTH//2 - 200, HEIGHT//2 - 50))

            inst = self.font_small.render("Press SPACE to return to the overworld.", True, (255,255,255))
            self.screen.blit(inst, (20, HEIGHT - 50))

            pygame.display.update()
            self.clock.tick(FPS)
            await asyncio.sleep(0)
