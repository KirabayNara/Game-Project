import pygame
import time

class DialogueBox:

    def __init__(self, screen, width, height, rect_height=100, color=(255, 255, 255), alpha=200):
        self.screen = screen
        self.width = width
        self.height = height
        self.rect_height = rect_height
        self.color = color
        self.alpha = alpha
        self.rect = pygame.Surface((self.width, self.rect_height))
        self.rect.set_alpha(0)  # Inicialmente invisível
        self.rect.fill(self.color)

        # Retangulo para o nome do personagem
        self.name_rect_height = 30
        self.name_rect = pygame.Surface((self.width, self.name_rect_height))
        self.name_rect.set_alpha(0)  # Inicialmente invisível
        self.name_rect.fill((200, 200, 200))  # Cor de fundo do retangulo

    def fade_in(self, speed=5):
        for alpha in range(0, self.alpha, speed):
            self.rect.set_alpha(alpha)
            self.name_rect.set_alpha(alpha)
            self.screen.blit(self.rect, (0, self.height - self.rect_height))
            self.screen.blit(self.name_rect, (0, self.height - self.rect_height - self.name_rect_height))
            pygame.display.update()
            time.sleep(0.02)  # Pequeno delay para o efeito de fade in

    def fade_out(self, speed=5):
        for alpha in range(self.alpha, 0, -speed):
            self.rect.set_alpha(alpha)
            self.name_rect.set_alpha(alpha)
            self.screen.blit(self.rect, (0, self.height - self.rect_height))
            self.screen.blit(self.name_rect, (0, self.height - self.rect_height - self.name_rect_height))
            pygame.display.update()
            time.sleep(0.02)  # Pequeno delay para o efeito fade in

    def display_text_gradually(self, text, font, name="", name_font=None, color=(0, 0, 0), name_color=(0, 0, 0), line_spacing=5, max_lines=2, delay=0.05):
        global rendered_text
        words = text.split(' ')
        lines = []
        current_line = ""

        # Construindo linhas de texto sem ultrapassar a largura do retângulo
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < self.width - 40:  # Margem de 20px em cada lado
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        lines.append(current_line)  # Adiciona a última linha

        y_offset = self.height - self.rect_height + 10  # Margem superior
        line_index = 0

        # Adiciona o retangulo do nome
        if name_font is None:
            name_font = font
        self.screen.blit(self.name_rect, (0, self.height - self.rect_height - self.name_rect_height))
        name_surface = name_font.render(name if name else "???", True, name_color)
        self.screen.blit(name_surface, (10, self.height - self.rect_height - self.name_rect_height + 5))
        pygame.display.update()

        # Animação gradual do texto
        while line_index < len(lines):
            rendered_lines = []
            interrupted = False

            # Desenha um bloco de linhas (até max_lines)
            for _ in range(max_lines):
                if line_index >= len(lines):
                    break

                displayed_text = ""
                for char in lines[line_index]:
                    displayed_text += char
                    rendered_text = font.render(displayed_text, True, color)
                    self.screen.blit(self.rect, (0, self.height - self.rect_height))

                    # Redesenha todas as linhas anteriores
                    for i, rendered_line in enumerate(rendered_lines):
                        self.screen.blit(rendered_line, (20, y_offset - (rendered_text.get_height() + line_spacing) * (len(rendered_lines) - i)))

                    self.screen.blit(rendered_text, (20, y_offset))
                    pygame.display.update()

                    # Verifica se a tecla "espaço" foi pressionada para interromper a animação
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
                    # Se a animação foi interrompida, exibe o texto completo imediatamente
                    rendered_text = font.render(lines[line_index], True, color)
                    self.screen.blit(self.rect, (0, self.height - self.rect_height))
                    for i, rendered_line in enumerate(rendered_lines):
                        self.screen.blit(rendered_line, (
                        20, y_offset - (rendered_text.get_height() + line_spacing) * (len(rendered_lines) - i)))
                    self.screen.blit(rendered_text, (20, y_offset))
                    pygame.display.update()

                rendered_lines.append(rendered_text)
                y_offset += rendered_text.get_height() + line_spacing
                line_index += 1

            # Adiciona o efeito de "..." piscando
            continue_text = font.render("...", True, color)
            continue_rect = continue_text.get_rect()
            continue_rect.topleft = (
            self.width - continue_text.get_width() - 20, self.height - continue_text.get_height() - 20)

            blinking = True
            while blinking:
                self.screen.blit(self.rect, (0, self.height - self.rect_height))

                # Redesenha todas as linhas anteriores
                for i, rendered_line in enumerate(rendered_lines):
                    self.screen.blit(rendered_line, (
                    20, y_offset - (rendered_text.get_height() + line_spacing) * (len(rendered_lines) - i)))

                self.screen.blit(continue_text, continue_rect.topleft)
                pygame.display.update()
                time.sleep(0.3)  # Tempo em que ficará apagado

                # Verifica se a tecla "espaço" foi pressionada para avançar para o próximo bloco
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        blinking = False
                        break

                if blinking:
                    self.screen.blit(self.rect, (0, self.height - self.rect_height))

                    for i, rendered_line in enumerate(rendered_lines):
                        self.screen.blit(rendered_line, (20, y_offset - (rendered_text.get_height() + line_spacing) * (len(rendered_lines) - i)))

                    self.screen.blit(continue_text, continue_rect.topleft)
                    pygame.display.update()
                    time.sleep(0.3)  # Tempo que ficará visível

            # Limpa a tela para o próximo bloco de linhas
            self.rect.fill(self.color)
            y_offset = self.height - self.rect_height + 10  # Reinicia o y_offset para o topo do retângulo
            self.screen.blit(self.rect, (0, self.height - self.rect_height))
            pygame.display.update()

            '''# Aguarda o jogador pressionar "espaço" para continuar
            waiting = True
            while waiting:
                self.screen.blit(self.rect, (0, self.height - self.rect_height))
                self.screen.blit(rendered_text, (20, y_offset - rendered_text.get_height() - line_spacing))
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        waiting = False'''

    # Finaliza o diálogo após o texto
    pygame.display.update()
