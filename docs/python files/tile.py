import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, sprite_type, surface=None):
        super().__init__(groups)
        self.sprite_type = sprite_type

        if surface is None:
            surface = pygame.Surface((TILESIZE, TILESIZE))
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.copy()
        self.obstacle_sprites = obstacle_sprites