import pygame
import random
from settings import *

class Arkaplan:
    def __init__(self):
        try:
            self.image = pygame.image.load("./assets/back.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (GENISLIK, YUKSEKLIK))
        except:
            self.image = pygame.Surface((GENISLIK, YUKSEKLIK))
            self.image.fill(GOK_MAVISI)
        
        self.paralaks = [
            {"hiz": 0.5, "x": 0},
            {"hiz": 1.0, "x": 0}
        ]

    def update(self, oyuncu_hiz):
        for katman in self.paralaks:
            katman["x"] -= katman["hiz"] * (oyuncu_hiz * 0.1)
            if katman["x"] <= -GENISLIK:
                katman["x"] = 0

    def draw(self, ekran):
        ekran.blit(self.image, (0, 0))
        for katman in self.paralaks:
            ekran.blit(self.image, (katman["x"], 0))
            ekran.blit(self.image, (katman["x"] + GENISLIK, 0))
