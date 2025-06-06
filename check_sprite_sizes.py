import pygame

pygame.init()

# Basit bir ekran aç
pygame.display.set_mode((100, 100))

idle_sheet = pygame.image.load("./assets/Idle.png").convert_alpha()
jump_sheet = pygame.image.load("./assets/Jump.png").convert_alpha()

print("Idle sheet size:", idle_sheet.get_width(), "x", idle_sheet.get_height())
print("Jump sheet size:", jump_sheet.get_width(), "x", jump_sheet.get_height())
