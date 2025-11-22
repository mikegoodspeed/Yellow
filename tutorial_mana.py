import pygame

from cutscene import Screen, ScreenManager


class TutorialManaScreen1(Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font
        self.primary_text = "This mana orb represents your energy."
        self.tertiary_text = "Making any action will consume mana."
        self.secondary_text = "Mana will auto-regenerate over time."
        self.text_color = (235, 200, 110)
        self.background_color = pygame.Color("black")
        self.next_hint_text = "Press Return/Enter to continue."
        self.next_hint_color = (255, 255, 255)
        self.mana_image = pygame.image.load("Mana_Original.png").convert_alpha()
        bg_color = self.mana_image.get_at((0, 0))
        self.mana_image.set_colorkey(bg_color, pygame.RLEACCEL)
        self.mana_image_size = self.mana_image.get_size()
        self.hint_grow_duration = 1.0
        self.hint_delay = 3.0
        self.hint_elapsed = 0.0
        self.hint_visible = False

    def on_enter(self):
        self.hint_elapsed = 0.0
        self.hint_visible = False

    def update(self, timestamp: float):
        self.hint_elapsed += timestamp
        if not self.hint_visible and self.hint_elapsed >= self.hint_delay:
            self.hint_visible = True

    def render(self, surface: pygame.Surface):
        surface.fill(self.background_color)
        surface_width = surface.get_width()
        surface_height = surface.get_height()
        text_rect = None
        if self.primary_text:
            text_surface = self.font.render(self.primary_text, True, self.text_color)
            text_rect = text_surface.get_rect(midtop=(surface_width // 2, 5))
            surface.blit(text_surface, text_rect)

        if self.hint_visible:
            base_hint = self.font.render(self.next_hint_text, True, self.next_hint_color)
            progress = min(1.0, max(0.0, (self.hint_elapsed - self.hint_delay) / max(1e-6, self.hint_grow_duration)))
            scale = 0.05 + 0.95 * progress
            hint_width = max(1, int(base_hint.get_width() * scale))
            hint_height = max(1, int(base_hint.get_height() * scale))
            hint_surface = pygame.transform.smoothscale(base_hint, (hint_width, hint_height))
            hint_rect = hint_surface.get_rect()
            top_offset = (text_rect.bottom + 5) if text_rect else 10
            hint_rect.topleft = (10, top_offset)
            surface.blit(hint_surface, hint_rect)

        if self.secondary_text:
            secondary_surface = self.font.render(self.secondary_text, True, self.text_color)
            secondary_rect = secondary_surface.get_rect(midbottom=(surface_width // 2, surface_height - 5))
            surface.blit(secondary_surface, secondary_rect)

        if self.tertiary_text:
            tertiary_surface = self.font.render(self.tertiary_text, True, self.text_color)
            tertiary_rect = tertiary_surface.get_rect(midbottom=(surface_width // 2, surface_height - 30))
            surface.blit(tertiary_surface, tertiary_rect)

        zone_height = surface.get_height() / 3.0
        desired_height = zone_height * 0.8
        orig_width, orig_height = self.mana_image_size
        scale = min(1.0, desired_height / orig_height)
        scaled_size = (max(1, int(orig_width * scale)), max(1, int(orig_height * scale)))
        scaled_image = pygame.transform.smoothscale(self.mana_image, scaled_size)
        image_rect = scaled_image.get_rect()
        image_rect.right = surface.get_width() - 10
        zone_top = surface.get_height() / 3.0
        image_rect.top = int(zone_top + max(0.0, (zone_height - image_rect.height) / 2))
        surface.blit(scaled_image, image_rect)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.switch("TutorialManaScreen2")


class TutorialManaScreen2(Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font
        self.primary_text = "Your orb will show a number. This is your current mana."
        self.tertiary_text = "Your number will decrease as you make actions..."
        self.secondary_text = "and increase as time passes."
        self.text_color = (235, 200, 110)
        self.background_color = pygame.Color("black")
        self.next_hint_text = "Press Return/Enter to continue."
        self.next_hint_color = (255, 255, 255)
        self.mana_image = pygame.image.load("Mana_10.png").convert_alpha()
        bg_color = self.mana_image.get_at((0, 0))
        self.mana_image.set_colorkey(bg_color, pygame.RLEACCEL)
        self.mana_image_size = self.mana_image.get_size()
        self.hint_delay = 6.0
        self.hint_grow_duration = 1.0
        self.hint_elapsed = 0.0
        self.hint_visible = False

    def on_enter(self):
        self.hint_elapsed = 0.0
        self.hint_visible = False

    def update(self, timestamp: float):
        self.hint_elapsed += timestamp
        if not self.hint_visible and self.hint_elapsed >= self.hint_delay:
            self.hint_visible = True

    def render(self, surface: pygame.Surface):
        surface.fill(self.background_color)
        surface_width = surface.get_width()
        surface_height = surface.get_height()
        text_rect = None
        if self.primary_text:
            text_surface = self.font.render(self.primary_text, True, self.text_color)
            text_rect = text_surface.get_rect(midtop=(surface_width // 2, 5))
            surface.blit(text_surface, text_rect)

        if self.hint_visible:
            base_hint = self.font.render(self.next_hint_text, True, self.next_hint_color)
            progress = min(1.0, max(0.0, (self.hint_elapsed - self.hint_delay) / max(1e-6, self.hint_grow_duration)))
            scale = 0.05 + 0.95 * progress
            hint_width = max(1, int(base_hint.get_width() * scale))
            hint_height = max(1, int(base_hint.get_height() * scale))
            hint_surface = pygame.transform.smoothscale(base_hint, (hint_width, hint_height))
            hint_rect = hint_surface.get_rect()
            top_offset = (text_rect.bottom + 5) if text_rect else 10
            hint_rect.topleft = (10, top_offset)
            surface.blit(hint_surface, hint_rect)

        if self.secondary_text:
            secondary_surface = self.font.render(self.secondary_text, True, self.text_color)
            secondary_rect = secondary_surface.get_rect(midbottom=(surface_width // 2, surface_height - 5))
            surface.blit(secondary_surface, secondary_rect)

        zone_height = surface.get_height() / 3.0
        desired_height = zone_height * 0.8
        orig_width, orig_height = self.mana_image_size
        scale = min(1.0, desired_height / orig_height)
        scaled_size = (max(1, int(orig_width * scale)), max(1, int(orig_height * scale)))
        scaled_image = pygame.transform.smoothscale(self.mana_image, scaled_size)
        image_rect = scaled_image.get_rect()
        image_rect.right = surface.get_width() - 10
        zone_top = surface.get_height() / 3.0
        image_rect.top = int(zone_top + max(0.0, (zone_height - image_rect.height) / 2))
        surface.blit(scaled_image, image_rect)

        if self.tertiary_text:
            tertiary_surface = self.font.render(self.tertiary_text, True, self.text_color)
            tertiary_rect = tertiary_surface.get_rect(midbottom=(surface_width // 2, surface_height - 30))
            surface.blit(tertiary_surface, tertiary_rect)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.switch("TutorialManaScreen3")


class TutorialManaScreen3(Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font
        self.primary_text = "Select Circular Storm to perform an action."
        self.tertiary_text = "Select 'Enact' to engage the action"
        self.secondary_text = "This will consume mana, and deal damage to your opponent."
        self.enact_text = "Enact"
        self.enact_color = (205, 205, 204)
        self.text_color = (235, 200, 110)
        self.background_color = pygame.Color("black")
        self.mana_image = pygame.image.load("Mana_10.png").convert_alpha()
        self.action_image = pygame.image.load("Circular_Storm.png").convert_alpha()
        bg_color = self.mana_image.get_at((0, 0))
        self.mana_image.set_colorkey(bg_color, pygame.RLEACCEL)
        self.mana_image_size = self.mana_image.get_size()
        self.action_image_size = self.action_image.get_size()
        self._storm_rect = pygame.Rect(0, 0, 0, 0)
        self.storm_hover_color = (255, 215, 0)
        self.storm_click_color = (0, 120, 255)
        self.storm_outline_width = 4
        self.storm_clicked = False
        self.hint_delay = 6.0
        self.hint_grow_duration = 1.0
        self.hint_elapsed = 0.0
        self.hint_visible = False

    def on_enter(self):
        self.hint_elapsed = 0.0
        self.hint_visible = False

    def update(self, timestamp: float):
        self.hint_elapsed += timestamp
        if not self.hint_visible and self.hint_elapsed >= self.hint_delay:
            self.hint_visible = True

    def render(self, surface: pygame.Surface):
        surface.fill(self.background_color)
        surface_width = surface.get_width()
        surface_height = surface.get_height()
        text_rect = None
        if self.primary_text:
            text_surface = self.font.render(self.primary_text, True, self.text_color)
            text_rect = text_surface.get_rect(midtop=(surface_width // 2, 5))
            surface.blit(text_surface, text_rect)

        if self.secondary_text:
            secondary_surface = self.font.render(self.secondary_text, True, self.text_color)
            secondary_rect = secondary_surface.get_rect(midbottom=(surface_width // 2, surface_height - 5))
            surface.blit(secondary_surface, secondary_rect)

        if self.tertiary_text:
            tertiary_surface = self.font.render(self.tertiary_text, True, self.text_color)
            tertiary_rect = tertiary_surface.get_rect(midbottom=(surface_width // 2, surface_height - 30))
            surface.blit(tertiary_surface, tertiary_rect)

        zone_height = surface.get_height() / 3.0
        desired_height = zone_height * 0.8
        orig_width, orig_height = self.mana_image_size
        scale = min(1.0, desired_height / orig_height)
        scaled_size = (max(1, int(orig_width * scale)), max(1, int(orig_height * scale)))
        scaled_image = pygame.transform.smoothscale(self.mana_image, scaled_size)
        image_rect = scaled_image.get_rect()
        image_rect.right = surface.get_width() - 10
        zone_top = surface.get_height() / 3.0
        image_rect.top = int(zone_top + max(0.0, (zone_height - image_rect.height) / 2))
        surface.blit(scaled_image, image_rect)

        storm_target_height = surface_height * 0.25
        storm_width, storm_height = self.action_image_size
        storm_scale = min(1.0, storm_target_height / storm_height)
        storm_scaled = pygame.transform.smoothscale(
            self.action_image,
            (
                max(1, int(storm_width * storm_scale)),
                max(1, int(storm_height * storm_scale)),
            ),
        )
        storm_rect = storm_scaled.get_rect(center=(surface_width // 2, surface_height // 2))
        surface.blit(storm_scaled, storm_rect)
        self._storm_rect = storm_rect
        hover = self._storm_rect.collidepoint(pygame.mouse.get_pos())
        if self.storm_clicked or hover:
            outline_color = self.storm_click_color if self.storm_clicked else self.storm_hover_color
            outline_rect = self._storm_rect.inflate(8, 8)
            pygame.draw.rect(surface, outline_color, outline_rect, self.storm_outline_width)
        if self.enact_text:
            enact_surface = self.font.render(self.enact_text, True, self.enact_color)
            enact_rect = enact_surface.get_rect()
            padding = 5
            enact_rect.centerx = image_rect.centerx
            enact_rect.top = image_rect.bottom + padding
            surface.blit(enact_surface, enact_rect)
            if self.storm_clicked:
                outline_rect = enact_rect.inflate(10, 6)
                pygame.draw.rect(surface, self.storm_click_color, outline_rect, 2)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._storm_rect.collidepoint(event.pos):
                self.storm_clicked = True
