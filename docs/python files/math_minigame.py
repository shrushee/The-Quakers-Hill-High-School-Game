import asyncio
import pygame
from settings import *
import random
import sys

class MathMinigame:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.finished = False
        self.state = "playing"
        self.background = pygame.image.load("assets/chalkboard.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.font_big = pygame.font.Font("assets/fonts/Chalk Board.otf", 70)
        self.font_small = pygame.font.Font("assets/fonts/Chalk Board.otf", 40)

        self.score = 0
        self.question_number = 1
        self.total_questions = 10
        self.current_question = None
        self.player_answer = ""
        self.feedback = ""
        self.feedback_time = 0
        self.feedback_duration = 800  # milliseconds
        self.generate_question()

    def generate_question(self):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(['+', '-', '*', '/'])

        # Ensure that a >= b
        if b > a:
            a, b = b, a

        if op == '+':
            self.current_question = f"{a} + {b}"
            self.correct_answer = a + b
        elif op == '-':
            self.current_question = f"{a} - {b}"
            self.correct_answer = a - b
        elif op == '*':
            self.current_question = f"{a} * {b}"
            self.correct_answer = a * b
        elif op == '/':
            answer = random.randint(1, 20)     # whole-number result
            b = random.randint(1, 20)          # divisor
            a = answer * b                      # dividend

            self.current_question = f"{a} / {b}"
            self.correct_answer = answer

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

            #background
            self.screen.blit(self.background, (0, 0))

            #Title
            title_surf = self.font_big.render("Maths Minigame Complete!", True, (255, 255, 255))
            self.screen.blit(title_surf, (WIDTH//2 - 300, HEIGHT//2 - 150))

            #display results
            result_surf = self.font_big.render(f"Your Score: {self.score}/{self.total_questions}", True, (255, 255, 255))
            self.screen.blit(result_surf, (WIDTH//2 - 200, HEIGHT//2 - 50))

            #draw instructions
            inst_surf = self.font_small.render("Press SPACE to return to the overworld.", True, (255, 255, 255))
            self.screen.blit(inst_surf, (20, HEIGHT - 50))

            pygame.display.update()
            self.clock.tick(FPS)
            await asyncio.sleep(0)

    async def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                        if self.question_number > self.total_questions:
                            self.state = "results"
                            return

                    if event.unicode.isdigit():
                        self.player_answer += event.unicode

                    if event.key == pygame.K_BACKSPACE:
                        self.player_answer = self.player_answer[:-1]

                    if event.key == pygame.K_RETURN:
                        if self.player_answer:
                            if int(self.player_answer) == self.correct_answer:
                                self.score += 1
                                self.feedback = "Correct!"
                                self.feedback_color = (0, 255, 0)  # Green
                            else:
                                self.feedback = f"Wrong! The correct answer was {self.correct_answer}."
                                self.feedback_color = (255, 0, 0)  # Red
                            self.feedback_time = pygame.time.get_ticks()  # Start feedback timer
                            self.player_answer = ""

                            if self.feedback:
                                if pygame.time.get_ticks() - self.feedback_time > self.feedback_duration:
                                    self.feedback = ""  # Clear feedback after duration
                            #Next question
                            self.question_number += 1

                            #If all finished, exit minigame
                            if self.question_number > self.total_questions:
                                self.state = "results"

                            #Otherwise, generate next question
                            self.generate_question()

            if self.state == "results":
                    await self.show_results_screen()
                    self.game.minigame_cooldown = True
                    return

            #background
            self.screen.blit(self.background, (0, 0))

            #display question
            question_surf = self.font_big.render(self.current_question, True, (255, 255, 255))
            self.screen.blit(question_surf, (WIDTH//2 - 100, HEIGHT//2 - 100))

            #display player answer
            answer_surf = self.font_big.render(self.player_answer, True, (255, 255, 255))
            self.screen.blit(answer_surf, (WIDTH//2 - 100, HEIGHT//2))

            #display feedback
            if self.feedback:
                feedback_surf = self.font_small.render(self.feedback, True, self.feedback_color)
                self.screen.blit(feedback_surf, (WIDTH//2 - 100, HEIGHT//2 + 50))

            #display score
            score_surf = self.font_small.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_surf, (10, 10))

            #draw instructions
            inst_surf = self.font_small.render("Type your answer and press Enter. Complete 10 questions.", True, (255, 255, 255))
            self.screen.blit(inst_surf, (20, HEIGHT - 50))

            pygame.display.update()
            self.clock.tick(FPS)
            await asyncio.sleep(0)

        #return to overworld
        self.game.state = "overworld"
        self.game.minigame_cooldown = False
