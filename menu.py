import pygame

from cutscene import Screen


class TitleScreen(Screen):
    def __init__(self, manager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.switch("MenuScreen")

    def render(self, surface: pygame.Surface):
        extremely_dark_blue = (0, 10, 47)
        background_color = pygame.Color(extremely_dark_blue)
        surface.fill(background_color)
        title_text = "Yellow - Press Enter/Return Key"
        antialias = True
        text_color = (235, 200, 110)
        text = self.font.render(title_text, antialias, text_color)
        center_coordinates = (surface.get_width() // 2, surface.get_height() // 2)
        rect = text.get_rect(center=center_coordinates)
        surface.blit(text, rect)


class MenuScreen(Screen):
    def __init__(self, manager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font
        self.options = ["Start Game", "Quit"]
        self.selected = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected == 0:
                    self.manager.switch("CutScene1")
                else:
                    self.manager.quit()

    def render(self, surface):
        selected_option_color = (255, 255, 100)
        default_option_color = (200, 200, 200)
        extremely_dark_blue = (0, 10, 47)
        surface.fill(extremely_dark_blue)
        surface_width, surface_height = surface.get_size()
        for i, option in enumerate(self.options):
            color = selected_option_color if i == self.selected else default_option_color
            text = self.font.render(option, True, color)
            spacing = i * 57.5
            center_position = (surface_width // 2, surface_height // 2 + spacing)
            rect = text.get_rect(center=center_position)
            surface.blit(text, rect)
