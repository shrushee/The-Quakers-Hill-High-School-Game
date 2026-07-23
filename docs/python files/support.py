from csv import reader
from os import walk
import pygame

"""Import functions to read csv files and import folders of images"""
def import_csv_layout(path):
    terrain_map = []
    FLIP_FLAGS = 0xE0000000  # mask for Tiled flip bits

    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            cleaned_row = []
            for cell in row:
                gid = int(cell)

                # Remove Tiled flip flags
                if gid == -1:
                    cleaned_row.append(-1)  
                else:
                    tile_id = gid & ~FLIP_FLAGS
                    cleaned_row.append(tile_id)
            terrain_map.append(cleaned_row)

    return terrain_map

def import_folder(path):
    surface_list = []
    try:
        for _,__,img_files in walk(path):
            for image in img_files:
                full_path = path + '/' + image
                image_surface = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surface)
            break
    except:
        pass

    return surface_list