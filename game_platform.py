import pygame
import random
from settings import *

class OyunPlatformu(pygame.sprite.Sprite):
    def __init__(self, x, y, genislik=PLATFORM_GENISLIK_UZUN, sabit=False):
        super().__init__()
        self.genislik = genislik
        self.image = self.platform_olustur(genislik)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.kirilma_suresi = KIRILMA_SURESI
        self.kirilma_baslangic = 0
        self.kiriliyor = False
        self.kirildi = False
        self.sabit = sabit
        self.hareketli_mi = False if sabit else (random.random() < 0.3)
        self.hiz = random.choice([1, 2]) if not sabit else 0
        self.yon = random.choice([-1, 1]) if not sabit else 0

    def kirilmaya_basla(self, zaman):
        if not self.sabit and not self.kiriliyor and not self.kirildi:
            self.kiriliyor = True
            self.kirilma_baslangic = zaman

    def guncelle(self, zaman, skor):
        if not self.sabit:
            if self.kiriliyor and not self.kirildi:
                suanki_sure = max(MIN_KIRILMA_SURESI,
                                KIRILMA_SURESI - (skor // 1000) * KIRILMA_HIZLANMA)
                if zaman - self.kirilma_baslangic > suanki_sure:
                    self.kirildi = True
                    self.kill()
                else:
                    kalan_oran = 1 - (zaman - self.kirilma_baslangic) / suanki_sure
                    self.image = self.platform_olustur(int(self.genislik * kalan_oran))
                    self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            if self.hareketli_mi:
                self.rect.x += self.hiz * self.yon
                if self.rect.left <= 0 or self.rect.right >= GENISLIK:
                    self.yon *= -1

    @classmethod
    def platform_olustur(cls, genislik):
        try:
            bas = pygame.image.load("./assets/platform_start.png").convert_alpha()
            orta = pygame.image.load("./assets/platform_middle.png").convert_alpha()
            son = pygame.image.load("./assets/platform_end.png").convert_alpha()
            yukseklik = PLATFORM_YUKSEKLIK
            bas = pygame.transform.scale(bas, (20, yukseklik))
            orta = pygame.transform.scale(orta, (20, yukseklik))
            son = pygame.transform.scale(son, (20, yukseklik))
            if genislik < 40:
                genislik = 40
            orta_sayisi = max(1, (genislik - 40) // 20)
            yuzey = pygame.Surface((20 + orta_sayisi * 20 + 20, yukseklik), pygame.SRCALPHA)
            yuzey.blit(bas, (0, 0))
            for i in range(orta_sayisi):
                yuzey.blit(orta, (20 + i * 20, 0))
            yuzey.blit(son, (20 + orta_sayisi * 20, 0))
            return pygame.transform.scale(yuzey, (genislik, yukseklik))
        except Exception as e:
            print(f"Platform sprite yüklenemedi: {e}")
            yuzey = pygame.Surface((genislik, PLATFORM_YUKSEKLIK), pygame.SRCALPHA)
            renk = (50, 200 - int(150 * (genislik / PLATFORM_GENISLIK_UZUN)), 50)
            pygame.draw.rect(yuzey, renk, (0, 0, genislik, PLATFORM_YUKSEKLIK))
            pygame.draw.rect(yuzey, (20, 90, 20), (0, 0, genislik, PLATFORM_YUKSEKLIK), 2)
            return yuzey
