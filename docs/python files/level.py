import pygame
from settings import *
from tile import Tile
from player import Player
from support import *

class Level:
    def __init__(self, game):
        self.game = game
       
        #Get display surface
        self.display_surface = pygame.display.get_surface()

        #Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
    
        #Creating minigame zones
        self.minigame_zones = [
            ("minigame1", pygame.Rect(288, 2831, 10, 200)),
            ("minigame2", pygame.Rect(400, 2861, 700, 10)),
            ("minigame3", pygame.Rect(1640, 1683, 500, 10)),
            ("minigame4", pygame.Rect(288, 2195, 10, 300)),
            ("minigame5", pygame.Rect(512, 1779, 700, 10)),
            ("minigame6", pygame.Rect(1472, 627, 800, 10)),
            ("minigame7", pygame.Rect(2304, 627, 10, 100))
        ]
        self.active_minigame_zone = None  # Track the currently active minigame zone

        #Sprite setup
        self.create_map()

        self.font_prompt = pygame.font.Font("assets/fonts/Pixel Game.otf", 30)
        self.show_prompt = False

        self.arrow_image = pygame.image.load("assets/marker.png").convert_alpha()
        self.arrow_image = pygame.transform.scale(self.arrow_image, (60, 60))

    def draw_ui(self):
        #Score counter
        shadow = self.game.ui_font.render(f"Score: {self.game.total_score}", True, (0, 0, 0))
        self.display_surface.blit(shadow, (22, 22))
        score_text = self.game.ui_font.render(f"Score: {self.game.total_score}", True, (255, 255, 255))
        self.display_surface.blit(score_text, (20, 20))

        #Progress bar background
        bar_x = 20
        bar_y = 70
        bar_width = 300
        bar_height = 25

        pygame.draw.rect(self.display_surface, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))

        #Progress fill
        progress = self.game.current_minigame_index / len(self.game.minigames_to_play)
        fill_width =  int(bar_width * progress)

        pygame.draw.rect(self.display_surface, (0, 200, 0), (bar_x, bar_y, fill_width, bar_height))

        shadow_progress = self.game.ui_font.render(
        f"{self.game.current_minigame_index}/{len(self.game.minigames_to_play)} Classes",
        True, (0, 0, 0)
    )
        self.display_surface.blit(shadow_progress, (bar_x + 322, bar_y - 3))

        #Progress text
        progress_text = self.game.ui_font.render(
            f"{self.game.current_minigame_index}/{len(self.game.minigames_to_play)} Classes",
            True,
            (255, 255, 255)
        )
        self.display_surface.blit(progress_text, (bar_x + 320, bar_y - 5))

        #Next subject
        next_subject = self.game.minigame_subject_map[self.game.current_target_minigame]
        shadow_next = self.game.ui_font.render(f"Next Subject: {next_subject}", True, (0, 0, 0))
        self.display_surface.blit(shadow_next, (22, 122))

        next_text = self.game.ui_font.render(f"Next Subject: {next_subject}", True, (255, 255, 255))
        self.display_surface.blit(next_text, (20, 120))

        # Today's Timetable
        timetable_x = WIDTH - 300
        timetable_y = 20

        shadow_title = self.game.ui_font.render("Today's Timetable", True, (0, 0, 0))
        self.display_surface.blit(shadow_title, (timetable_x + 2, timetable_y + 2))
        title = self.game.ui_font.render("Today's Timetable", True, (255, 255, 255))
        self.display_surface.blit(title, (timetable_x, timetable_y))

        for i, minigame_name in enumerate(self.game.minigames_to_play):
            subject = self.game.minigame_subject_map[minigame_name]
            shadow_entry = self.game.ui_font.render(f"{i+1}. {subject}", True, (0, 0, 0))
            self.display_surface.blit(shadow_entry, (timetable_x + 2, timetable_y + 52 + i * 40))
            entry_text = self.game.ui_font.render(f"{i+1}. {subject}", True, (255, 255, 255))
            self.display_surface.blit(entry_text, (timetable_x, timetable_y + 50 + i * 40))

    def check_minigame_triggers(self):
        player_rect = self.player.rect
        keys = pygame.key.get_pressed()
        for minigame_name, zone in self.minigame_zones:
            mapped = self.game.minigame_state_map[minigame_name]
            if mapped != self.game.current_target_minigame:
                continue

            if not self.game.minigame_cooldown:  # Check if the cooldown is not active
                if player_rect.colliderect(zone):
                    self.show_prompt = True
                    self.active_minigame_zone = minigame_name  # Set the active minigame zone

                    if keys[pygame.K_SPACE]:
                        self.game.state = minigame_name
                else:
                    self.show_prompt = False  # Hide the prompt if the player is not in any zone
                    self.active_minigame_zone = None  # Reset the active minigame zone
            else:
                self.show_prompt = False  # Hide the prompt if the cooldown is active

                in_any_zone = any(player_rect.colliderect(zone) for _, zone in self.minigame_zones)
                if not in_any_zone:
                    self.game.minigame_cooldown = False  # Reset the cooldown when the player leaves the zone

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('assets/tiles/qhhs map_boundary.csv'),
            'buildings': import_csv_layout('assets/tiles/qhhs map_buildings.csv'),
            'rail1': import_csv_layout('assets/tiles/qhhs map_railing layer.csv'),
            'rail2': import_csv_layout('assets/tiles/qhhs map_rail layer 2.csv'),
        }

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != -1:
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites], self.obstacle_sprites, 'invisible')
                        if style == 'buildings':
                            Tile((x,y),[self.obstacle_sprites], self.obstacle_sprites, 'obstacle')
        self.player = Player((2471, 2841), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        #update and draw game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.check_minigame_triggers()
        self.draw_navigation_arrow()
        self.draw_ui()

        if self.show_prompt and self.active_minigame_zone == self.game.current_target_minigame:
            subject = self.game.minigame_subject_map[self.active_minigame_zone]
            prompt_text = f"Press SPACE to start {subject.upper()}!"

            prompt_surf = self.font_prompt.render(prompt_text, True, (255, 255, 255))
            prompt_bg = pygame.Surface((prompt_surf.get_width() + 20, prompt_surf.get_height() + 20))
            prompt_bg.fill((0, 0, 0))
            prompt_bg.set_alpha(200)  # Set transparency

            #position the prompt in the center of the screen
            x = WIDTH // 2 - prompt_bg.get_width() // 2
            y = HEIGHT - 100

            self.display_surface.blit(prompt_bg, (x, y))
            self.display_surface.blit(prompt_surf, (x + 10, y + 10))

    def draw_navigation_arrow(self):
        player_pos = pygame.math.Vector2(self.player.rect.center)

        target_pos = None
        for minigame_name, zone in self.minigame_zones:
            mapped = self.game.minigame_state_map[minigame_name]
            if mapped == self.game.current_target_minigame:
                target_pos = pygame.math.Vector2(zone.center)
                break
        if target_pos is None:
            return  # No target position found, exit the function

        direction = target_pos - player_pos
        angle = direction.angle_to(pygame.math.Vector2(0, -1))  # Angle in degrees

        rotated_arrow = pygame.transform.rotate(self.arrow_image, angle)
        arrow_rect = rotated_arrow.get_rect(center=(WIDTH // 2, 80))

        self.display_surface.blit(rotated_arrow, arrow_rect)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('assets/qhhs map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

        # map size
        self.map_width = self.floor_surf.get_width()
        self.map_height = self.floor_surf.get_height()

    def custom_draw(self, player):

        #offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # clamp X
        self.offset.x = max(0, min(self.offset.x, self.map_width - self.display_surface.get_width()))

        # clamp Y
        self.offset.y = max(0, min(self.offset.y, self.map_height - self.display_surface.get_height()))

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)