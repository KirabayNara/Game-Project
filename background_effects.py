import pygame
import time

class BackgroundEffects:

    def __init__(self, screen):
        self.screen = screen

    def fade_in(self, image, speed=5):
        # Configura a imagem e seu alpha inicial
        image = image.convert()
        for alpha in range(256, -1, -speed):
            self.screen.blit(image, (0, 0)) # Desenha a imagem no fundo
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            overlay.set_alpha(alpha) # Define a transparencia da sobreposição
            overlay.fill((0, 0, 0)) # Preenche a sobreposição com preto
            self.screen.blit(overlay, (0, 0)) # Desenha a sobreposição na tela
            pygame.display.update()
            time.sleep(0.02)
    def fade_out(self, image, speed=5):
        # Configura a imagem e seu alpha inicial
        image = image.convert()
        for alpha in range(0, 256, -speed):
            self.screen.blit(image, (0, 0))
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            overlay.set_alpha(alpha)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            pygame.display.update()
            time.sleep(0.02)