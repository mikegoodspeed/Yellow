import pygame

from cutscene import Screen, ScreenManager


class TutorialTextScreen1(Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font
        self.elapsed = 0.0
        self.secondary_delay = 3.0
        self.secondary_shown = False
        self.post_secondary_elapsed = 0.0
        self.post_secondary_delay = 3.0

    def on_enter(self):
        self.elapsed = 0.0
        self.secondary_shown = False
        self.post_secondary_elapsed = 0.0

    def update(self, timestamp: float):
        self.elapsed += timestamp
        if not self.secondary_shown and self.elapsed >= self.secondary_delay:
            self.secondary_shown = True
        if self.secondary_shown:
            self.post_secondary_elapsed += timestamp
            if self.post_secondary_elapsed >= self.post_secondary_delay:
                self.manager.switch("TutorialTextScreen2")

    def render(self, surface: pygame.Surface):
        surface.fill(pygame.Color("black"))
        primary_text = "Oh no! Yellow has been abducted!"
        secondary_text = "Your goal is to find, rescue, and return Yellow safely home."
        antialias = True
        text_color = (235, 200, 110)
        text = self.font.render(primary_text, antialias, text_color)
        center_coordinates = (surface.get_width() // 2, surface.get_height() // 2)
        rect = text.get_rect(center=center_coordinates)
        surface.blit(text, rect)
        if self.secondary_shown:
            text = self.font.render(secondary_text, antialias, text_color)
            center_coordinates = (surface.get_width() // 2, surface.get_height() // 2 + 50)
            rect = text.get_rect(center=center_coordinates)
            surface.blit(text, rect)


class TutorialTextScreen2(Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font
        self.elapsed = 0.0
        self.secondary_delay = 3.0
        self.secondary_shown = False
        self.post_secondary_elapsed = 0.0
        self.post_secondary_delay = 3.0
        self.primary_text = "To do so, you'll need to battle several other circlings"
        self.secondary_text = "I'm going to teach you the basics now."

    def on_enter(self):
        self.elapsed = 0.0
        self.secondary_shown = False
        self.post_secondary_elapsed = 0.0

    def update(self, timestamp: float):
        self.elapsed += timestamp
        if not self.secondary_shown and self.elapsed >= self.secondary_delay:
            self.secondary_shown = True
        if self.secondary_shown:
            self.post_secondary_elapsed += timestamp
            if self.post_secondary_elapsed >= self.post_secondary_delay:
                self.manager.switch("TutorialManaScreen1")

    def render(self, surface: pygame.Surface):
        surface.fill(pygame.Color("black"))
        antialias = True
        text_color = (235, 200, 110)
        text = self.font.render(self.primary_text, antialias, text_color)
        center_coordinates = (surface.get_width() // 2, surface.get_height() // 2)
        rect = text.get_rect(center=center_coordinates)
        surface.blit(text, rect)
        if self.secondary_shown:
            text = self.font.render(self.secondary_text, antialias, text_color)
            center_coordinates = (surface.get_width() // 2, surface.get_height() // 2 + 50)
            rect = text.get_rect(center=center_coordinates)
            surface.blit(text, rect)
