import time
import pygame
from screen_manager import screen, width, height
from dialogue_box import DialogueBox
from background_effects import BackgroundEffects

def run_corridor_scene():

    # Carregando a classe BackgroundEffects
    bg_effects = BackgroundEffects(screen)

    # Carregando o som de fechar a porta
    door_close_sound = pygame.mixer.Sound("assets/sounds/door_close.MP3")
    door_close_sound.set_volume(0.4)

    # Carregando a imagem do corredor
    corridor_image = pygame.image.load("assets/images/corridor.png")
    corridor_image = pygame.transform.scale(corridor_image, (width, height))

    # Reproduz o som de fechar de porta
    door_close_sound.play()

    # Aplicar efeito de fade in na imagem do corredor
    bg_effects.fade_in(corridor_image)

    # Esperar 1 segundo
    time.sleep(3)

    # Criar o retangulo de diálogo e exibi-lo com fade in
    dialogue_box = DialogueBox(screen, screen.get_width(), screen.get_height())

    # Texto do protagonista
    font = pygame.font.SysFont("calibri", 20, False, True)
    protagonist_name = "Aodh"
    protagonist_text = ""
    narrator = "Narrator"

    # Exibindo o retangulo em fade in e texto com efeito animado em blocos de 2 linhas
    dialogue_box.fade_in()
    dialogue_box.display_text_with_choices(protagonist_text, [], font, name="")
    dialogue_box.fade_out()
    time.sleep(0.5)

    dialogue_box.display_text_with_choices(f"{protagonist_name}?", [], font, name="")
    time.sleep(0.5)

    dialogue_box.fade_out()
    bg_effects.fade_out(corridor_image)

def main():
    run_corridor_scene()

if __name__ == "__main__":
    main()
