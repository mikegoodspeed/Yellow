import pygame

from cutscene import Screen, ScreenManager


TEXT_COLOR = (235, 200, 110)
BG_COLOR = pygame.Color("black")
HINT_TEXT = "Press Return/Enter to continue."
HINT_COLOR = (255, 255, 255)


def _blit_text(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: tuple[int, int, int],
    **rect_kwargs,
) -> pygame.Rect | None:
    if not text:
        return None
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(**rect_kwargs)
    surface.blit(text_surface, rect)
    return rect


def _render_growing_hint(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: tuple[int, int, int],
    elapsed: float,
    delay: float,
    grow_duration: float,
    top_offset: int,
):
    if elapsed < delay:
        return
    base_hint = font.render(text, True, color)
    progress = min(1.0, max(0.0, (elapsed - delay) / max(1e-6, grow_duration)))
    scale = 0.05 + 0.95 * progress
    hint_width = max(1, int(base_hint.get_width() * scale))
    hint_height = max(1, int(base_hint.get_height() * scale))
    hint_surface = pygame.transform.smoothscale(base_hint, (hint_width, hint_height))
    hint_rect = hint_surface.get_rect()
    hint_rect.topleft = (10, top_offset)
    surface.blit(hint_surface, hint_rect)


def _scale_image_to_zone(
    image: pygame.Surface,
    image_size: tuple[int, int],
    surface: pygame.Surface,
    zone_top_ratio: float = 1.0 / 3.0,
    zone_height_ratio: float = 1.0 / 3.0,
    height_ratio: float = 0.8,
    right_margin: int = 10,
) -> tuple[pygame.Surface, pygame.Rect]:
    zone_height = surface.get_height() * zone_height_ratio
    desired_height = zone_height * height_ratio
    orig_width, orig_height = image_size
    scale = min(1.0, desired_height / orig_height)
    scaled_size = (max(1, int(orig_width * scale)), max(1, int(orig_height * scale)))
    scaled_image = pygame.transform.smoothscale(image, scaled_size)
    image_rect = scaled_image.get_rect()
    image_rect.right = surface.get_width() - right_margin
    zone_top = surface.get_height() * zone_top_ratio
    image_rect.top = int(zone_top + max(0.0, (zone_height - image_rect.height) / 2))
    return scaled_image, image_rect


class ManaInfoScreen(Screen):
    def __init__(
        self,
        manager: ScreenManager,
        font: pygame.font.Font,
        primary_text: str,
        secondary_text: str,
        tertiary_text: str,
        mana_image_path: str,
        hint_delay: float,
        next_screen: str,
    ):
        super().__init__(manager)
        self.font = font
        self.primary_text = primary_text
        self.tertiary_text = tertiary_text
        self.secondary_text = secondary_text
        self.text_color = TEXT_COLOR
        self.background_color = BG_COLOR
        self.next_hint_text = HINT_TEXT
        self.next_hint_color = HINT_COLOR
        self.mana_image = pygame.image.load(mana_image_path).convert_alpha()
        bg_color = self.mana_image.get_at((0, 0))
        self.mana_image.set_colorkey(bg_color, pygame.RLEACCEL)
        self.mana_image_size = self.mana_image.get_size()
        self.hint_grow_duration = 1.0
        self.hint_delay = hint_delay
        self.hint_elapsed = 0.0
        self.next_screen = next_screen

    def on_enter(self):
        self.hint_elapsed = 0.0

    def update(self, timestamp: float):
        self.hint_elapsed += timestamp

    def render(self, surface: pygame.Surface):
        surface.fill(self.background_color)
        surface_width = surface.get_width()
        surface_height = surface.get_height()

        text_rect = _blit_text(
            surface,
            self.font,
            self.primary_text,
            self.text_color,
            midtop=(surface_width // 2, 5),
        )

        if self.next_hint_text:
            top_offset = (text_rect.bottom + 5) if text_rect else 10
            _render_growing_hint(
                surface,
                self.font,
                self.next_hint_text,
                self.next_hint_color,
                self.hint_elapsed,
                self.hint_delay,
                self.hint_grow_duration,
                top_offset,
            )

        _blit_text(
            surface,
            self.font,
            self.secondary_text,
            self.text_color,
            midbottom=(surface_width // 2, surface_height - 5),
        )
        _blit_text(
            surface,
            self.font,
            self.tertiary_text,
            self.text_color,
            midbottom=(surface_width // 2, surface_height - 30),
        )

        scaled_image, image_rect = _scale_image_to_zone(
            self.mana_image, self.mana_image_size, surface
        )
        surface.blit(scaled_image, image_rect)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.switch(self.next_screen)


class TutorialManaScreen1(ManaInfoScreen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(
            manager,
            font,
            "This mana orb represents your energy.",
            "Mana will auto-regenerate over time.",
            "Making any action will consume mana.",
            "Mana_Original.png",
            hint_delay=3.0,
            next_screen="TutorialManaScreen2",
        )


class TutorialManaScreen2(ManaInfoScreen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(
            manager,
            font,
            "Your orb will show a number. This is your current mana.",
            "and increase as time passes.",
            "Your number will decrease as you make actions...",
            "Mana_10.png",
            hint_delay=6.0,
            next_screen="TutorialManaScreen3",
        )


class ActionTutorialScreen(Screen):
    def __init__(
        self,
        manager: ScreenManager,
        font: pygame.font.Font,
        primary_text: str,
        secondary_text: str,
        tertiary_text: str,
        mana_image_path: str,
        next_screen: str,
    ):
        super().__init__(manager)
        self.font = font
        self.primary_text = primary_text
        self.tertiary_text = tertiary_text
        self.secondary_text = secondary_text
        self.enact_text = "Enact"
        self.text_color = TEXT_COLOR
        self.background_color = BG_COLOR
        self.mana_image = pygame.image.load(mana_image_path).convert_alpha()
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
        self.enact_delay = 2.0
        self.enact_flame_duration = 3.0
        self.enact_timer = 0.0
        self.enact_state = "idle"
        self.show_storm = True
        self.flame_colors = [(255, 180, 40), (255, 100, 20), (200, 40, 0)]
        self.enact_base_color = (205, 205, 204)
        self.enact_active_color = self.storm_click_color
        self.enact_unlocked = False
        self._enact_rect: pygame.Rect | None = None
        self.post_enact_delay = 1.0
        self.post_enact_timer = 0.0
        self.post_enact_started = False
        self.next_screen = next_screen

    def on_enter(self):
        self.enact_state = "idle"
        self.enact_timer = 0.0
        self.show_storm = True
        self.storm_clicked = False
        self.enact_unlocked = False
        self.post_enact_started = False
        self.post_enact_timer = 0.0

    def update(self, timestamp: float):
        if self.enact_state == "waiting":
            self.enact_timer += timestamp
            if self.enact_timer >= self.enact_delay:
                self.enact_state = "flames"
                self.enact_timer = 0.0
        elif self.enact_state == "flames":
            self.enact_timer += timestamp
            if self.enact_timer >= self.enact_flame_duration:
                self.enact_state = "done"
                self.enact_timer = 0.0
                self.show_storm = False
                self.storm_clicked = False
                self.post_enact_started = True
                self.post_enact_timer = 0.0

        if self.post_enact_started and not self.show_storm:
            self.post_enact_timer += timestamp
            if self.post_enact_timer >= self.post_enact_delay:
                self.manager.switch(self.next_screen)

    def render(self, surface: pygame.Surface):
        surface.fill(self.background_color)
        surface_width = surface.get_width()
        surface_height = surface.get_height()

        _blit_text(
            surface,
            self.font,
            self.primary_text,
            self.text_color,
            midtop=(surface_width // 2, 5),
        )
        _blit_text(
            surface,
            self.font,
            self.secondary_text,
            self.text_color,
            midbottom=(surface_width // 2, surface_height - 5),
        )
        _blit_text(
            surface,
            self.font,
            self.tertiary_text,
            self.text_color,
            midbottom=(surface_width // 2, surface_height - 30),
        )

        scaled_image, image_rect = _scale_image_to_zone(
            self.mana_image, self.mana_image_size, surface
        )
        surface.blit(scaled_image, image_rect)

        if self.show_storm:
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
            if self.enact_state == "flames":
                self._render_flames(surface, storm_rect)
        else:
            self._storm_rect = pygame.Rect(0, 0, 0, 0)

        if self.enact_text and self.show_storm:
            enact_color = self.enact_active_color if self.enact_unlocked else self.enact_base_color
            enact_surface = self.font.render(self.enact_text, True, enact_color)
            enact_rect = enact_surface.get_rect()
            enact_rect.centerx = image_rect.centerx
            enact_rect.top = image_rect.bottom + 5
            surface.blit(enact_surface, enact_rect)
            self._enact_rect = pygame.Rect(enact_rect)
            if self.storm_clicked:
                outline_rect = enact_rect.inflate(10, 6)
                pygame.draw.rect(surface, self.storm_click_color, outline_rect, 2)
        else:
            self._enact_rect = None

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.show_storm and self._storm_rect.collidepoint(event.pos):
                self.storm_clicked = True
                self.enact_unlocked = True
            if self._enact_rect and self._enact_rect.collidepoint(event.pos) and self.enact_unlocked:
                if self.enact_state == "idle":
                    self.enact_state = "waiting"
                    self.enact_timer = 0.0

    def _render_flames(self, surface: pygame.Surface, storm_rect: pygame.Rect):
        center = storm_rect.center
        base_radius = max(storm_rect.width, storm_rect.height) / 2
        flame_progress = min(1.0, self.enact_timer / max(1e-6, self.enact_flame_duration))
        for idx, color in enumerate(self.flame_colors):
            radius = (
                base_radius
                + 12
                + idx * 8
                + int(20 * flame_progress)
                + (idx % 2) * 4
            )
            width = 6 - idx
            pygame.draw.circle(surface, color, center, int(radius), max(1, width))


class TutorialManaScreen3(ActionTutorialScreen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(
            manager,
            font,
            "Select Circular Storm to perform an action.",
            "This will consume mana, and deal damage to your opponent.",
            "Select 'Enact' to engage the action",
            "Mana_10.png",
            next_screen="TutorialManaScreen4",
        )


class TutorialManaScreen4(Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font
        self.primary_text = "You are the Blue Circling."
        self.secondary_text = "Your opponent is the Grey Circling."
        self.tertiary_text = "They have just taken 15 damage!"
        self.text_color = (235, 200, 110)
        self.background_color = pygame.Color("black")
        self.grey_color = (110, 110, 110)
        self.blue_color = (50, 100, 255)
        self.text_delay = 0.5
        self.text_elapsed = 0.0
        self.text_visible = False
        self.dmg_color = (0, 0, 0)
        self.dmg_font = pygame.font.Font(None, max(32, int(self.font.get_height() * 1.5)))
        self.text_duration = 3.0
        self._text_shown_elapsed = 0.0
        self._text_finished = False
        self._post_text_delay = 1.0
        self._post_text_elapsed = 0.0
        self._post_text_started = False

    def on_enter(self):
        self.text_elapsed = 0.0
        self.text_visible = False
        self._text_finished = False
        self._post_text_started = False

    def update(self, timestamp: float):
        if not self.text_visible and not self._text_finished:
            self.text_elapsed += timestamp
            if self.text_elapsed >= self.text_delay:
                self.text_visible = True
                self._text_shown_elapsed = 0.0
        elif self.text_visible:
            self._text_shown_elapsed += timestamp
            if self._text_shown_elapsed >= self.text_duration:
                self.text_visible = False
                self._text_finished = True
        elif self._text_finished and not self._post_text_started:
            self._post_text_started = True
            self._post_text_elapsed = 0.0
        elif self._post_text_started:
            self._post_text_elapsed += timestamp
            if self._post_text_elapsed >= self._post_text_delay:
                self.manager.switch("TutorialManaScreen5")

    def render(self, surface: pygame.Surface):
        surface.fill(self.background_color)
        surface_width = surface.get_width()
        surface_height = surface.get_height()
        if self.primary_text:
            text_surface = self.font.render(self.primary_text, True, self.text_color)
            text_rect = text_surface.get_rect(midtop=(surface_width // 2, 5))
            surface.blit(text_surface, text_rect)

        if self.secondary_text:
            secondary_surface = self.font.render(self.secondary_text, True, self.text_color)
            secondary_rect = secondary_surface.get_rect(midbottom=(surface_width // 2, surface_height - 45))
            surface.blit(secondary_surface, secondary_rect)

        if self.tertiary_text:
            tertiary_surface = self.font.render(self.tertiary_text, True, self.text_color)
            tertiary_rect = tertiary_surface.get_rect(midbottom=(surface_width // 2, surface_height - 20))
            surface.blit(tertiary_surface, tertiary_rect)

        circle_radius = max(20, min(surface_width, surface_height) // 8)
        left_center = (int(surface_width * 0.25), surface_height // 2)
        right_center = (int(surface_width * 0.75), surface_height // 2)
        pygame.draw.circle(surface, self.grey_color, left_center, circle_radius)
        pygame.draw.circle(surface, self.blue_color, right_center, circle_radius)

        if self.text_visible:
            text_surface = self.dmg_font.render("- 15", True, self.dmg_color)
            text_rect = text_surface.get_rect(center=left_center)
            surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.switch("TitleScreen")


class TutorialManaScreen5(ActionTutorialScreen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(
            manager,
            font,
            "",
            "",
            "",
            "Mana_5.png",
            next_screen="TutorialManaScreen4",
        )
