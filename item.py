import pygame
from settings import *

class Havuc(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.orijinal_image = pygame.image.load("./assets/Idle1.png").convert_alpha()
            self.orijinal_image = pygame.transform.scale(
                self.orijinal_image,
                (HAVUC_GENISLIK, HAVUC_YUKSEKLIK)
            )
        except Exception as e:
            print(f"Havuç sprite yüklenemedi: {e}")
            self.orijinal_image = pygame.Surface((HAVUC_GENISLIK, HAVUC_YUKSEKLIK))
            self.orijinal_image.fill(HAVUC_RENGI)
        self.image = self.orijinal_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.aci = 0

    def update(self):
        self.aci = (self.aci + 4) % 10
        self.image = pygame.transform.rotate(self.orijinal_image, self.aci)
        self.rect = self.image.get_rect(center=self.rect.center)
