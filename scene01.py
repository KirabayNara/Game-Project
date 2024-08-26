import time
import pygame
from screen_manager import screen, width, height
from dialogue_box import DialogueBox

def run_corridor_scene():

    # Definição de cores
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Carregando o som de fechar a porta
    door_close_sound = pygame.mixer.Sound("assets/sounds/door_close.MP3")
    door_close_sound.set_volume(0.5)

    # Carregando a imagem do corredor
    corridor_image = pygame.image.load("assets/images/corridor.png")
    corridor_image = pygame.transform.scale(corridor_image, (width, height))

    # Reproduz o som de fechar de porta
    door_close_sound.play()

    # Efeito de fade in na imagem de fundo
    for alpha in range(0, 255, 5): # 256 para cobrir de 0 a 255
        screen.fill(black)
        corridor_image.set_alpha(alpha) # Configura a transparência
        screen.blit(corridor_image, (0, 0))
        pygame.display.update()
        pygame.time.delay(50) # Tempo para o efeito fade in

    # Esperar 0.5 segundos
    time.sleep(0.5)

    # Criar o retangulo de diálogo e exibi-lo com fade in
    dialogue_box = DialogueBox(screen, screen.get_width(), screen.get_height())

    # Texto do protagonista
    font = pygame.font.SysFont("calibri", 20, False, True)
    protagonist_name = "Arthur"
    protagonist_text = "O ar aqui está estranho... Parece que algo se esconde nas sombras. O ar aqui está estranho... Parece que algo se esconde nas sombras. O ar aqui está estranho... Parece que algo se esconde nas sombras."

    # Exibindo o retangulo em fade in e texto com efeito animado em blocos de 2 linhas
    dialogue_box.fade_in()
    dialogue_box.display_text_gradually(protagonist_text, font, name=protagonist_name)
    dialogue_box.fade_out()
    time.sleep(0.5)

    dialogue_box.display_text_gradually("Arthur?!", font, name="")
    dialogue_box.fade_out()
    pygame.display.update()

def main():
    run_corridor_scene()

if __name__ == "__main__":
    main()
