import asyncio
import pygame
import sys
from settings import *
from player import Oyuncu
from platform_manager import PlatformYoneticisi
from game_platform import OyunPlatformu
from sound import init_sounds

class Oyun:
    def __init__(self):
        pygame.init()
        init_sounds()
        self.ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
        pygame.display.set_caption("Jump Jump Rabbit")
        self.saat = pygame.time.Clock()
        self.oyun_baslat()

    def oyun_baslat(self):
        # Font yükleme
        try:
            self.font_buyuk = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 24)
            self.font_kucuk = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 16)
        except:
            self.font_buyuk = pygame.font.Font(None, 36)
            self.font_kucuk = pygame.font.Font(None, 24)

        # Hareketli arkaplan yükleme
        try:
            self.arkaplan = pygame.image.load("./assets/back.png").convert()
            self.arkaplan = pygame.transform.scale(self.arkaplan, (GENISLIK, YUKSEKLIK))
        except:
            self.arkaplan = pygame.Surface((GENISLIK, YUKSEKLIK))
            self.arkaplan.fill(GOK_MAVISI)

        # Arkaplan kaydırma değişkenleri
        self.arkaplan_y1 = 0
        self.arkaplan_y2 = -YUKSEKLIK

        # Sprite grupları
        self.tum_sprite = pygame.sprite.LayeredUpdates()
        self.platform_grubu = pygame.sprite.Group()
        self.item_grubu = pygame.sprite.Group()

        # Oyuncu oluşturma
        self.oyuncu = Oyuncu(GENISLIK // 2, YUKSEKLIK - 100)
        self.tum_sprite.add(self.oyuncu)

        # Platform yöneticisi
        self.platform_yonetici = PlatformYoneticisi(self.tum_sprite, self.platform_grubu, self.item_grubu)

        # Başlangıç platformu
        baslangic_platform = OyunPlatformu(
            GENISLIK // 2 - PLATFORM_GENISLIK_UZUN // 2,
            YUKSEKLIK - 50,
            PLATFORM_GENISLIK_UZUN,
            sabit=True
        )
        self.platform_grubu.add(baslangic_platform)
        self.tum_sprite.add(baslangic_platform)
        
        # Başlangıç platformları oluştur
        self.platform_yonetici.baslangic_platform_olustur(15, YUKSEKLIK - 80)

        # Oyun değişkenleri
        self.kayma = 0
        self.toplam_kayma = 0
        self.skor = 0
        self.oyun_aktif = True
        self.zaman = pygame.time.get_ticks()

    async def calistir(self):
        while True:
            suanki_zaman = pygame.time.get_ticks()
            dt = suanki_zaman - self.zaman
            self.zaman = suanki_zaman

            # Olay yönetimi
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and not self.oyun_aktif:
                        # Oyunu yeniden başlat
                        self.oyun_baslat()

            # Arkaplan kaydırma
            self.arkaplan_y1 += ARKAPLAN_KAYMA_HIZI
            self.arkaplan_y2 += ARKAPLAN_KAYMA_HIZI
            
            if self.arkaplan_y1 > YUKSEKLIK:
                self.arkaplan_y1 = self.arkaplan_y2 - YUKSEKLIK
            if self.arkaplan_y2 > YUKSEKLIK:
                self.arkaplan_y2 = self.arkaplan_y1 - YUKSEKLIK

            # Oyun mantığı
            if self.oyun_aktif:
                self.oyuncu.guncelle(self.platform_grubu, self.item_grubu, self.zaman)
                
                # Platform güncellemeleri
                for platform in self.platform_grubu:
                    platform.guncelle(self.zaman, self.skor)
                
                # Kamera kaydırma
                if self.oyuncu.rect.top <= YUKSEKLIK // 3:
                    self.kayma = YUKSEKLIK // 3 - self.oyuncu.rect.top
                    self.oyuncu.rect.top = YUKSEKLIK // 3
                    self.toplam_kayma += self.kayma
                    self.platform_yonetici.guncelle(self.kayma, self.skor, self.zaman)
                    self.skor += self.kayma // 5
                
                # Oyun bitiş kontrolü
                if self.oyuncu.rect.top > YUKSEKLIK:
                    self.oyun_aktif = False

            # Çizimler
            self.ekran.blit(self.arkaplan, (0, self.arkaplan_y1))
            self.ekran.blit(self.arkaplan, (0, self.arkaplan_y2))

            # Sprite'ları çiz
            for sprite in sorted(self.tum_sprite, key=lambda s: s.rect.y):
                if -100 < sprite.rect.y < YUKSEKLIK + 100:
                    self.ekran.blit(sprite.image, sprite.rect)

            # HUD
            skor_yazi = self.font_buyuk.render(f"SKOR: {self.skor}", True, BEYAZ)
            self.ekran.blit(skor_yazi, (20, 20))
            
            combo_yazi = self.font_kucuk.render(f"COMBO: x{self.oyuncu.combo}", True, BEYAZ)
            self.ekran.blit(combo_yazi, (20, 60))
            
            havuc_yazi = self.font_kucuk.render(f"HAVUÇ: {self.oyuncu.havuc_sayisi}", True, BEYAZ)
            self.ekran.blit(havuc_yazi, (20, 100))

            # Oyun bitiş ekranı
            if not self.oyun_aktif:
                bitis_yuzey = pygame.Surface((GENISLIK, YUKSEKLIK), pygame.SRCALPHA)
                bitis_yuzey.fill((0, 0, 0, 180))
                self.ekran.blit(bitis_yuzey, (0, 0))
                
                bitis_yazi = self.font_buyuk.render("OYUN BİTTİ", True, BEYAZ)
                skor_yazi = self.font_buyuk.render(f"Son Skor: {self.skor}", True, BEYAZ)
                yeniden_yazi = self.font_kucuk.render("R: Yeniden Başlat", True, BEYAZ)
                
                self.ekran.blit(bitis_yazi, (GENISLIK // 2 - bitis_yazi.get_width() // 2, YUKSEKLIK // 2 - 60))
                self.ekran.blit(skor_yazi, (GENISLIK // 2 - skor_yazi.get_width() // 2, YUKSEKLIK // 2))
                self.ekran.blit(yeniden_yazi, (GENISLIK // 2 - yeniden_yazi.get_width() // 2, YUKSEKLIK // 2 + 60))

            pygame.display.flip()
            await asyncio.sleep(0)  # Web için kritik!
            self.saat.tick(FPS)

async def main():
    oyun = Oyun()
    await oyun.calistir()

if __name__ == "__main__":
    asyncio.run(main())