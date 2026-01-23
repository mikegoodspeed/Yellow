import pygame

from cutscene import Screen, ScreenManager


def _blit_centered_text(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: tuple[int, int, int],
    center: tuple[int, int],
) -> pygame.Rect | None:
    if not text:
        return None
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=center)
    surface.blit(text_surface, rect)
    return rect


class TimedTextScreen(Screen):
    def __init__(
        self,
        manager: ScreenManager,
        font: pygame.font.Font,
        primary_text: str,
        secondary_text: str,
        next_screen: str,
        secondary_delay: float = 3.0,
        post_secondary_delay: float = 3.0,
    ):
        super().__init__(manager)
        self.font = font
        self.primary_text = primary_text
        self.secondary_text = secondary_text
        self.next_screen = next_screen
        self.secondary_delay = secondary_delay
        self.post_secondary_delay = post_secondary_delay
        self.elapsed = 0.0
        self.secondary_shown = False
        self.post_secondary_elapsed = 0.0

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
                self.manager.switch(self.next_screen)

    def render(self, surface: pygame.Surface):
        surface.fill(pygame.Color("black"))
        text_color = (235, 200, 110)
        center = (surface.get_width() // 2, surface.get_height() // 2)
        _blit_centered_text(surface, self.font, self.primary_text, text_color, center)
        if self.secondary_shown:
            secondary_center = (center[0], center[1] + 50)
            _blit_centered_text(surface, self.font, self.secondary_text, text_color, secondary_center)


class TutorialTextScreen1(TimedTextScreen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(
            manager,
            font,
            "Oh no! Yellow has been abducted!",
            "Your goal is to find, rescue, and return Yellow safely home.",
            next_screen="TutorialTextScreen2",
        )


class TutorialTextScreen2(TimedTextScreen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(
            manager,
            font,
            "To do so, you'll need to battle several other circlings",
            "I'm going to teach you the basics now.",
            next_screen="TutorialManaScreen1",
        )
