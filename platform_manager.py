import random
from game_platform import OyunPlatformu
from item import Havuc
from settings import *

class PlatformYoneticisi:
    def __init__(self, tum_sprite, platform_grubu, item_grubu):
        self.tum_sprite = tum_sprite
        self.platform_grubu = platform_grubu
        self.item_grubu = item_grubu
        self.min_y = YUKSEKLIK
        self.son_platform_x = GENISLIK // 2

    def baslangic_platform_olustur(self, adet, baslangic_y):
        y = baslangic_y
        for _ in range(adet):
            self.denge_platform_ekle(y)
            y -= random.randint(80, 120)

    def denge_platform_ekle(self, y=None):
        genislik = random.choice([PLATFORM_GENISLIK_KISA, PLATFORM_GENISLIK_UZUN])
        if len(self.platform_grubu) > 0:
            yon = random.choice([-1, 1])
            x = self.son_platform_x + (yon * random.randint(50, 150))
            x = max(0, min(x, GENISLIK - genislik))
        else:
            x = random.randint(0, GENISLIK - genislik)
        if y is None:
            y = self.min_y - random.randint(80, 120)
        platform = OyunPlatformu(x, y, genislik)
        self.tum_sprite.add(platform)
        self.platform_grubu.add(platform)
        self.min_y = y
        self.son_platform_x = x + genislik // 2
        if random.random() < 0.5:
            self.havuc_ekle(platform.rect.centerx, platform.rect.top - 30)
        return platform

    def havuc_ekle(self, x, y):
        havuc = Havuc(x, y)
        self.tum_sprite.add(havuc)
        self.item_grubu.add(havuc)

    def guncelle(self, kamera_kayma, skor, zaman):
        for platform in self.platform_grubu:
            platform.rect.y += kamera_kayma
            platform.guncelle(zaman, skor)
        for platform in list(self.platform_grubu):
            if platform.rect.top > YUKSEKLIK + 50:
                platform.kill()
        for item in list(self.item_grubu):
            item.rect.y += kamera_kayma
            item.update()
            if item.rect.top > YUKSEKLIK + 50:
                item.kill()
        if len([p for p in self.platform_grubu if p.rect.bottom > 0]) < 12:
            self.denge_platform_ekle()
