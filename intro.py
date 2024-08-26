import pygame
from pygame.locals import *
from sys import exit
import time
from screen_manager import screen, width, height

def run_intro():

    # Definição de cores
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Definição da fonte
    font = pygame.font.SysFont("calibri", 20, bold=False, italic=True)

    # Carregando o som de caneta escrevendo
    writing_sound = pygame.mixer.Sound("assets/sounds/writing_sound.mp3")
    writing_sound.set_volume(1.0)

    # Carregando o som de lareira de fundo
    fireplace_sound = pygame.mixer.Sound("assets/sounds/fireplace_sound.MP3")
    fireplace_sound.set_volume(0.5)

    # Texto de introdução
    intro_text = '"Muitos de vocês talvez nunca me entendam, talvez me culpem, talvez me julguem. Mas sinceramente essa é a única forma que encontro de resolver isso... ' \
                 'A culpa foi minha, e preciso concertar as coisas... Me perdem, Cian, Maeve... Rhiannon. Prometo que vou concertar as coisas. Nunca entendi o motivo de todos ' \
                 'serem tão complacentes comigo, talvez por eu ser do alto escalão da guarda real? Talvez por eu ser considerado da realeza? Mesmo assim, ainda sou humano, ainda ' \
                 'cometo erros, e quero pagar pelos meus... Por favor, cuidem de Taliesin, o pobrizinho está muito velho e precisa que fiquem de olho nele. Por hora é isso, se cuidem ' \
                 'e não façam a burrice de me procurar, vou voltar, eu prometo. Rhiannon, vou concertar as coisas."'

    # Função para quebrar o texto em linhas e deixá-lo alinhado a tela
    def wrap_text(text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''

        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '

        lines.append(current_line)
        return lines

    # Função para definir a velocidade de exibição dos blocos de texto
    def set_text_speed(speed):
        return 1.0 / speed # Quanto maior o valor de speed, mais rapido o texto será exibido

    # Função para ajustar o volume do som
    def set_sound_volume(sound, volume):
        sound.set_volume(volume)

    # Função para exibir o texto gradualmente, com suporte para interrupção com a tecla "espaço" linha por linha
    def display_text_gradually(lines, x, y, max_lines, delay=0.05, line_spacing=5, blinking=None):
        current_line = 0
        interrupted = False

        while current_line < len(lines):
            screen.fill(black)

            # Inicia o som de escrita para o bloco atual
            writing_sound.play()

            # Exibe o bloco de 8 linhas com efeito gradual
            for i in range(max_lines):
                if current_line + i < len(lines):
                    displayed_text = ""
                    for char in lines[current_line + i]:
                        displayed_text += char
                        render_text = font.render(displayed_text, True, white)
                        screen.blit(render_text, (x, y + i * (font.get_height() + line_spacing)))
                        pygame.display.update()

                        # Verifica se a tecla "espaço" foi pressionada
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                return
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                interrupted = True
                                break

                        if interrupted:
                            break
                        time.sleep(delay)

                    if interrupted:
                        # Se a exibição foi interrompida, desenha a linha inteira restante
                        render_text = font.render(lines[current_line + i], True, white)
                        screen.blit(render_text, (x, y + i * (font.get_height() + line_spacing)))
                        pygame.display.update()

                    if interrupted:
                        break

            # Se a exibição foi interrompida, desenha o bloco inteiro
            if interrupted:
                for j in range(i, max_lines):
                    if current_line + j < len(lines):
                        render_text = font.render(lines[current_line + j], True, white)
                        screen.blit(render_text, (x, y + j * (font.get_height() + line_spacing)))
                pygame.display.update()

            # Exibe a mensagem "continuar..." piscando após cada bloco
            continue_text = font.render("continuar...", True, white)
            continue_rect = continue_text.get_rect()
            continue_rect.topleft = (width - continue_text.get_width() - 20, height - continue_text.get_height() - 20)

            #Loop de Piscar com probabilidade de interrupção pelo jogador
            blinking = True
            while blinking:
                screen.fill(black, continue_rect) # Limpa a área onde o texto é desenhado
                pygame.display.update()
                time.sleep(0.3) # Tempo em que ficará apagado

                #verifica se a tecla espaço foi pressionada
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        blinking = False
                        interrupted = True
                        break

                if blinking:
                    screen.blit(continue_text, continue_rect.topleft)
                    pygame.display.update()
                    time.sleep(0.3) # Tempo que o texto ficará visível

                # Verifica se a tecla "espaço" foi pressionada
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        blinking = False
                        interrupted = True
                        break

            # Se o jogador pressionou "espaço" durante o piscar, avança imediatamente para o próximo bloco
            if interrupted:
                current_line += max_lines
                interrupted = False
                continue

            # Aguarda o jogador pressionar "espaço" para cotinuar
            if not interrupted:
                waiting = True
                while waiting:
                    # Exibe a mensagem "continuar..." após o loop de piscar
                    screen.blit(continue_text, continue_rect.topleft)
                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            waiting = False

            # Avança para o próximo bloco de texto
            current_line += max_lines
            interrupted = False

    # Loop principal do jogo
    '''running = True
    text_speed = set_text_speed(15) # Ajuste a velocidade do texto (quanto maior o valor, mais rápido o texto)
    set_sound_volume(writing_sound, 1.0)
    set_sound_volume(fireplace_sound, 0.5)

    # Iniciar a reprodução do som de lareira em loop
    fireplace_sound.play(-1)

    # Quebrando o texto em linhas para caber na tela
    wrapped_lines = wrap_text(intro_text, font, width - 100)
    max_lines = 8

    # Inicializa a flag de conclusão
    intro_done = False

    while running:
        screen.fill(black)
        display_text_gradually(wrapped_lines, 50, height // 4, max_lines, delay=text_speed)

        # Loop que identifica quando o jogo é fechado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return False # Sau do jogo completamente
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False # Encerra a introdução

    pygame.quit()
    return True'''

    # Inicializa o som da lareira
    fireplace_sound.play(-1)

    # Quebra o texto em linhas
    wrapped_lines = wrap_text(intro_text, font, width - 100)
    max_lines = 8

    # Exibindo o texto gradualmente
    display_text_gradually(wrapped_lines, 50, height // 4, max_lines, delay=set_text_speed(15))

    fireplace_sound.stop()

    return True  # Retorna True após a introdução terminar

def main():
    run_intro()

if __name__ == "__main__":
    main()
