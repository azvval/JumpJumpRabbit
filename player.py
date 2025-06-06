import pygame
from settings import *
from sound import play_sound

class Oyuncu(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.cerceve_genislik = 42
        self.cerceve_yukseklik = 42
        self.idle_cerceveler = []
        self.jump_cerceveler = []
        self.sprite_yukle()
        self.image = self.idle_cerceveler[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.hiz_y = 0
        self.yerde_mi = False
        self.combo = 0
        self.combo_sayac = 0
        self.COMBO_SIFIRLAMA = 60
        self.havuc_sayisi = 0
        self.anim_index = 0
        self.anim_hiz = 0.15
        self.aktif_animasyon = self.idle_cerceveler

    def sprite_yukle(self):
        try:
            idle_sheet = pygame.image.load("./assets/Idle.png").convert_alpha()
            jump_sheet = pygame.image.load("./assets/Jump.png").convert_alpha()
            for i in range(4):
                cerceve = idle_sheet.subsurface(pygame.Rect(i * 42, 0, 42, 42))
                self.idle_cerceveler.append(cerceve)
            for i in range(8):
                cerceve = jump_sheet.subsurface(pygame.Rect(i * 42, 0, 42, 42))
                self.jump_cerceveler.append(cerceve)
        except:
            self.image = pygame.Surface((42, 42))
            self.image.fill((255, 0, 0))
            self.idle_cerceveler = [self.image]
            self.jump_cerceveler = [self.image]

    def guncelle(self, platformlar, itemlar, zaman):
        tuslar = pygame.key.get_pressed()
        
        # Sağ-sol hareket
        if tuslar[pygame.K_LEFT]:
            self.rect.x -= OYUNCU_HIZ
        if tuslar[pygame.K_RIGHT]:
            self.rect.x += OYUNCU_HIZ
        
        # Sınır kontrolü
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(GENISLIK, self.rect.right)
        
        # Yerçekimi
        self.hiz_y += YERCEKIMI
        self.rect.y += self.hiz_y
        self.yerde_mi = False

        # Platform çarpışma kontrolü
        for platform in platformlar:
            if self.rect.colliderect(platform.rect) and self.hiz_y > 0:
                self.rect.bottom = platform.rect.top + 1
                self.hiz_y = 0
                self.yerde_mi = True
                platform.kirilmaya_basla(zaman)

        # Havuç toplama
        for item in itemlar:
            if self.rect.colliderect(item.rect):
                item.kill()
                self.havuc_sayisi += 1
                play_sound("super_jump")

        # Zıplama kontrolleri
        if tuslar[pygame.K_SPACE] and self.yerde_mi:
            self.zipla()

        # Özel zıplamalar
        if tuslar[pygame.K_z] and self.yerde_mi:
            if self.havuc_sayisi >= 6:
                self.hiz_y = SUPER_ZIP_GUCU
                self.havuc_sayisi -= 6
                play_sound("jump-6x")
            elif self.havuc_sayisi >= 3:
                self.hiz_y = YUKSEK_ZIP_GUCU
                self.havuc_sayisi -= 3
                play_sound("super_jump")
            self.combo += 1
            self.combo_sayac = self.COMBO_SIFIRLAMA

        # Animasyon güncelleme
        self.animasyon_guncelle()
        
        # Combo sıfırlama
        if self.combo_sayac > 0:
            self.combo_sayac -= 1
        else:
            self.combo = 0

    def animasyon_guncelle(self):
        if self.yerde_mi:
            self.aktif_animasyon = self.idle_cerceveler
        else:
            self.aktif_animasyon = self.jump_cerceveler
        
        self.anim_index += self.anim_hiz
        if self.anim_index >= len(self.aktif_animasyon):
            self.anim_index = 0
        
        self.image = self.aktif_animasyon[int(self.anim_index)]

    def zipla(self):
        self.hiz_y = ZIPLAMA_GUCU
        self.combo += 1
        self.combo_sayac = self.COMBO_SIFIRLAMA
        play_sound("jump")
