import pygame

sounds = {}
sound_enabled = True

def init_sounds():
    global sound_enabled
    try:
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        sounds["jump"] = pygame.mixer.Sound("./assets/jump.wav")
        sounds["super_jump"] = pygame.mixer.Sound("./assets/super_jump.wav")
        sounds["jump-6x"] = pygame.mixer.Sound("./assets/jump-x6.wav")
        print("Sesler başarıyla yüklendi")
    except Exception as e:
        print(f"Ses yükleme hatası: {e}")
        sound_enabled = False

def play_sound(name):
    global sound_enabled
    if sound_enabled and name in sounds:
        try:
            sounds[name].play()
        except Exception as e:
            print(f"Ses çalma hatası: {e}")
            sound_enabled = False