import sys
import pygame


class ScreenManager:
    def __init__(self):
        self.screens: dict[str, "Screen"] = {}
        self.active: "Screen" | None = None
        self.running: bool = True

    def add(self, name: str, screen: "Screen"):
        self.screens[name] = screen

    def switch(self, name: str):
        if self.active:
            self.active.on_exit()
        self.active = self.screens.get(name)
        if self.active:
            self.active.on_enter()

    def handle_event(self, event: pygame.event.Event):
        if self.active:
            self.active.handle_event(event)

    def update(self, timestamp: float):
        if self.active:
            self.active.update(timestamp)

    def render(self, surface: pygame.Surface):
        if self.active:
            self.active.render(surface)

    def quit(self):
        self.running = False


class Screen:
    def __init__(self, manager: ScreenManager):
        self.manager = manager

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self, timestamp: float):
        pass

    def render(self, surface: pygame.Surface):
        pass

class TutorialTextScreen1(Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font
        self.elapsed = 0.0
        self.secondary_delay = 3.0
        self.secondary_shown = False
        self.post_secondary_elapsed = 0.0
        self.post_secondary_delay = 3.0

    # def handle_event(self, event: pygame.event.Event):
    #     if event.type == pygame.KEYDOWN:
    #         # any key moves to MenuScreen
    #         self.manager.switch("MenuScreen")

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
        background_color = pygame.Color('black')
        surface.fill(background_color)
        primary_text = "Oh no! Yellow has been abducted!"
        secondary_text = "Your goal is to find, rescue, and return Yellow safely home."
        antialias = True
        text_color = (235, 200, 110)
        text = self.font.render(primary_text, antialias, text_color)
        center_coordinates = (surface.get_width()//2, surface.get_height()//2)
        rect = text.get_rect(center=center_coordinates)
        surface.blit(text, rect)
        if self.secondary_shown:
            text = self.font.render(secondary_text, antialias, text_color)
            center_coordinates = (surface.get_width()//2, surface.get_height()//2 + 50)
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

    # def handle_event(self, event: pygame.event.Event):
    #     if event.type == pygame.KEYDOWN:
    #         # any key moves to MenuScreen
    #         self.manager.switch("MenuScreen")

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
                self.manager.switch("TutorialManaScreen")

    def render(self, surface: pygame.Surface):
        background_color = pygame.Color('black')
        surface.fill(background_color)
        primary_text = "To do so, you'll need to battle several other circlings"
        secondary_text = "I'm going to teach you the basics now."
        antialias = True
        text_color = (235, 200, 110)
        text = self.font.render(primary_text, antialias, text_color)
        center_coordinates = (surface.get_width()//2, surface.get_height()//2)
        rect = text.get_rect(center=center_coordinates)
        surface.blit(text, rect)
        if self.secondary_shown:
            text = self.font.render(secondary_text, antialias, text_color)
            center_coordinates = (surface.get_width()//2, surface.get_height()//2 + 50)
            rect = text.get_rect(center=center_coordinates)
            surface.blit(text, rect)


class TutorialManaScreen(Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font
        self.primary_text = "Mana Primer"
        self.text_color = (235, 200, 110)
        self.background_color = pygame.Color('black')
        self.mana_image = pygame.image.load("Mana_Original.png").convert_alpha()

    def render(self, surface: pygame.Surface):
        surface.fill(self.background_color)
        text_surface = self.font.render(self.primary_text, True, self.text_color)
        text_rect = text_surface.get_rect(midtop=(surface.get_width() // 2, 10))
        surface.blit(text_surface, text_rect)

        image_rect = self.mana_image.get_rect()
        image_rect.left = 0
        image_rect.centery = surface.get_height() // 2
        surface.blit(self.mana_image, image_rect)




class TitleScreen(Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            # any key moves to menu
            self.manager.switch("MenuScreen")

    def render(self, surface: pygame.Surface):
        background_color = pygame.Color('black')
        surface.fill(background_color)
        title_text = "Yellow - Press any key"
        antialias = True
        text_color = (235, 200, 110)
        text = self.font.render(title_text, antialias, text_color)
        center_coordinates = (surface.get_width()//2, surface.get_height()//2)
        rect = text.get_rect(center=center_coordinates)
        surface.blit(text, rect)


class MenuScreen(Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
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
        background_color = (30, 30, 30)
        selected_option_color = (255, 255, 100)
        default_option_color = (200, 200, 200)

        surface.fill(background_color)
        surface_width, surface_height = surface.get_size()
        for i, option in enumerate(self.options):
            color = selected_option_color if i == self.selected else default_option_color
            text = self.font.render(option, True, color)
            spacing = i * 80
            center_position = (surface_width//2, surface_height//2 + spacing)
            rect = text.get_rect(center=center_position)
            surface.blit(text, rect)


class CircleEffect:
    def __init__(self, radius: int, color: tuple[int, int, int]):
        self.radius = radius
        self.color = color

    def _draw_alpha_circle(self, surface: pygame.Surface, center: tuple[float, float], alpha: int):
        diameter = self.radius * 2
        circle_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, (*self.color, alpha), (self.radius, self.radius), self.radius)
        surface.blit(circle_surface, (int(center[0]) - self.radius, int(center[1]) - self.radius))


class YellowCircle(CircleEffect):
    def __init__(self, radius: int, color: tuple[int, int, int], fade_duration: float):
        super().__init__(radius, color)
        self.fade_duration = fade_duration
        self.center_x = 0.0
        self.fading = False
        self.fade_elapsed = 0.0
        self.visible = True

    def reset(self, center_x: float):
        self.center_x = center_x
        self.fading = False
        self.fade_elapsed = 0.0
        self.visible = True

    def start_fade(self):
        if not self.fading:
            self.fading = True
            self.fade_elapsed = 0.0

    def update(self, timestamp: float):
        if self.fading:
            self.fade_elapsed += timestamp
            if self.fade_elapsed >= self.fade_duration:
                self.fade_elapsed = self.fade_duration
                self.fading = False
                self.visible = False

    def render(self, surface: pygame.Surface, center_y: float):
        if not self.visible and not self.fading:
            return
        if self.fading and self.fade_duration > 0:
            ratio = max(0.0, 1.0 - (self.fade_elapsed / max(1e-6, self.fade_duration)))
            alpha = int(255 * ratio)
        else:
            alpha = 255
        self._draw_alpha_circle(surface, (self.center_x, center_y), alpha)


class RedCircle(CircleEffect):
    def __init__(self, radius: int, color: tuple[int, int, int], wait_time: float, move_duration: float, fade_in_delay: float = 1.0, fade_in_duration: float = 1.0):
        super().__init__(radius, color)
        self.wait_time = wait_time
        self.move_duration = move_duration
        self.fade_in_delay = fade_in_delay
        self.fade_in_duration = fade_in_duration
        self.start_x: float | None = None
        self.target_x: float | None = None
        self.current_x: float | None = None
        self.wait_elapsed = 0.0  # movement wait
        self.move_elapsed = 0.0
        self.moving = False
        self.finished = False
        self.fade_wait_elapsed = 0.0
        self.fade_in_elapsed = 0.0
        self.fading_in = False
        self.visible = False

    def reset(self, start_x: float, target_x: float):
        self.start_x = start_x
        self.target_x = target_x
        self.current_x = start_x
        self.wait_elapsed = 0.0
        self.move_elapsed = 0.0
        self.moving = False
        self.finished = False
        self.fade_wait_elapsed = 0.0
        self.fade_in_elapsed = 0.0
        self.fading_in = False
        self.visible = False

    def update(self, timestamp: float):
        if self.finished:
            return
        if not self.visible:
            if not self.fading_in:
                self.fade_wait_elapsed += timestamp
                if self.fade_wait_elapsed >= self.fade_in_delay:
                    self.fading_in = True
                    self.fade_in_elapsed = 0.0
            else:
                self.fade_in_elapsed += timestamp
                if self.fade_in_elapsed >= self.fade_in_duration:
                    self.fade_in_elapsed = self.fade_in_duration
                    self.fading_in = False
                    self.visible = True
            return

        if not self.moving:
            self.wait_elapsed += timestamp
            if self.wait_elapsed >= self.wait_time:
                self.moving = True
                self.move_elapsed = 0.0
        else:
            self.move_elapsed += timestamp
            t = min(1.0, self.move_elapsed / max(1e-6, self.move_duration))
            if self.start_x is not None and self.target_x is not None:
                self.current_x = self.start_x + (self.target_x - self.start_x) * t
            if t >= 1.0:
                self.current_x = self.target_x
                self.moving = False
                self.finished = True

    def render(self, surface: pygame.Surface, center_y: float):
        if self.current_x is None:
            return
        if not self.visible and not self.fading_in:
            return
        if self.fading_in and self.fade_in_duration > 0:
            alpha = int(255 * min(1.0, self.fade_in_elapsed / max(1e-6, self.fade_in_duration)))
        else:
            alpha = 255
        self._draw_alpha_circle(surface, (self.current_x, center_y), alpha)


class BlueCircle(CircleEffect):
    def __init__(self, radius: int, color: tuple[int, int, int], wait_after_red: float, fade_duration: float, move_duration: float):
        super().__init__(radius, color)
        self.wait_after_red = wait_after_red
        self.fade_duration = fade_duration
        self.move_duration = move_duration
        self.center_x: float | None = None
        self.screen_width = 0
        self.wait_elapsed = 0.0
        self.fade_elapsed = 0.0
        self.move_elapsed = 0.0
        self.fading_in = False
        self.fully_visible = False
        self.moving = False
        self.ready_for_sequence = False
        self.finished = False
        self.start_x = 0.0
        self.target_x = 0.0

    def reset(self, start_x: float, screen_width: int):
        self.center_x = start_x
        self.screen_width = screen_width
        self.wait_elapsed = 0.0
        self.fade_elapsed = 0.0
        self.move_elapsed = 0.0
        self.fading_in = False
        self.fully_visible = False
        self.moving = False
        self.ready_for_sequence = False
        self.finished = False
        self.start_x = start_x
        self.target_x = start_x

    def notify_red_finished(self):
        self.ready_for_sequence = True

    def update(self, timestamp: float):
        if not self.ready_for_sequence or self.center_x is None:
            return
        if not self.fading_in:
            self.wait_elapsed += timestamp
            if self.wait_elapsed >= self.wait_after_red:
                self.fading_in = True
                self.fade_elapsed = 0.0
        elif not self.fully_visible:
            self.fade_elapsed += timestamp
            if self.fade_elapsed >= self.fade_duration:
                self.fade_elapsed = self.fade_duration
                self.fully_visible = True
        elif not self.moving and not self.finished:
            max_center_x = float(self.screen_width - self.radius) if self.screen_width else self.center_x
            self.start_x = self.center_x
            self.target_x = (self.start_x + max_center_x) / 2.0
            self.move_elapsed = 0.0
            self.moving = True
        elif self.moving:
            self.move_elapsed += timestamp
            t = min(1.0, self.move_elapsed / max(1e-6, self.move_duration))
            self.center_x = self.start_x + (self.target_x - self.start_x) * t
            if t >= 1.0:
                self.center_x = self.target_x
                self.moving = False
                self.finished = True

    def render(self, surface: pygame.Surface, center_y: float):
        if not self.ready_for_sequence or self.center_x is None:
            return
        if not self.fading_in and not self.fully_visible and not self.finished and not self.moving:
            return
        if self.fully_visible or self.finished or self.move_duration == 0:
            alpha = 255
        else:
            alpha = int(255 * (self.fade_elapsed / max(1e-6, self.fade_duration)))
        alpha = max(0, min(255, alpha))
        self._draw_alpha_circle(surface, (self.center_x, center_y), alpha)


class GreenCircle(CircleEffect):
    def __init__(
        self,
        radius: int,
        color: tuple[int, int, int],
        wait_after_blue: float,
        move_duration: float,
        fade_duration: float,
        corner_inset: tuple[float, float] = (30.0, 30.0),
        fade_in_duration: float = 0.5,
    ):
        super().__init__(radius, color)
        self.wait_after_blue = wait_after_blue
        self.move_duration = move_duration
        self.fade_duration = fade_duration
        self.corner_inset = corner_inset
        self.fade_in_duration = fade_in_duration

        self.wait_elapsed = 0.0
        self.move_elapsed = 0.0
        self.fade_in_elapsed = 0.0
        self.fade_out_elapsed = 0.0
        self.started = False
        self.fading_in = False
        self.moving = False
        self.in_place = False
        self.fading_out = False
        self.finished = False
        self.can_start_sequence = False
        self.position: tuple[float, float] | None = None
        self.start_pos: tuple[float, float] | None = None
        self.target_pos: tuple[float, float] | None = None
        self.corner_position: tuple[float, float] | None = None
        self._trigger_fade_event = False
        self.visible = False

    def reset(self, yellow_x: float, center_y: float):
        inset_x, inset_y = self.corner_inset
        corner_x = self.radius + inset_x
        corner_y = self.radius + inset_y

        self.wait_elapsed = 0.0
        self.move_elapsed = 0.0
        self.fade_in_elapsed = 0.0
        self.fade_out_elapsed = 0.0
        self.started = False
        self.fading_in = False
        self.moving = False
        self.in_place = False
        self.fading_out = False
        self.finished = False
        self.can_start_sequence = False
        self.position = None
        self.start_pos = None
        self.corner_position = (corner_x, corner_y)
        self.target_pos = (yellow_x, center_y)
        self._trigger_fade_event = False
        self.visible = False

    def notify_blue_finished(self):
        self.can_start_sequence = True

    def update(self, dt: float, yellow_x: float, center_y: float):
        if self.finished or not self.can_start_sequence:
            return

        self.target_pos = (yellow_x, center_y)

        if not self.started:
            self.wait_elapsed += dt
            if self.wait_elapsed >= self.wait_after_blue:
                self.started = True
                self.position = self.corner_position
                self.start_pos = self.corner_position
                self.fading_in = True
                self.visible = True
                self.fade_in_elapsed = 0.0
        elif self.fading_in:
            if self.fade_in_duration <= 0:
                self.fading_in = False
                self.moving = True
                self.move_elapsed = 0.0
            else:
                self.fade_in_elapsed += dt
                if self.fade_in_elapsed >= self.fade_in_duration:
                    self.fade_in_elapsed = self.fade_in_duration
                    self.fading_in = False
                    self.moving = True
                    self.move_elapsed = 0.0
        elif self.moving:
            self.move_elapsed += dt
            t = min(1.0, self.move_elapsed / max(1e-6, self.move_duration))
            if self.start_pos and self.target_pos:
                sx, sy = self.start_pos
                tx, ty = self.target_pos
                self.position = (sx + (tx - sx) * t, sy + (ty - sy) * t)
            if t >= 1.0:
                self.position = self.target_pos
                self.moving = False
                self.in_place = True
                self.fading_out = True
                self.fade_out_elapsed = 0.0
                self._trigger_fade_event = True
        elif self.fading_out:
            self.fade_out_elapsed += dt
            if self.fade_out_elapsed >= self.fade_duration:
                self.fade_out_elapsed = self.fade_duration
                self.fading_out = False
                self.finished = True
                self.visible = False

    def consume_fade_trigger(self) -> bool:
        if self._trigger_fade_event:
            self._trigger_fade_event = False
            return True
        return False

    def render(self, surface: pygame.Surface):
        if not self.started or self.position is None:
            return
        if not self.visible and not self.fading_in and not self.fading_out:
            return
        if self.fading_in and self.fade_in_duration > 0:
            alpha = int(255 * min(1.0, self.fade_in_elapsed / max(1e-6, self.fade_in_duration)))
        elif self.fading_out and self.fade_duration > 0:
            alpha = int(255 * max(0.0, 1.0 - (self.fade_out_elapsed / max(1e-6, self.fade_duration))))
        else:
            alpha = 255
        self._draw_alpha_circle(surface, self.position, alpha)


class CutScene1(Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font
        self.surface_width = 800
        self.surface_height = 600
        self.center_x = self.surface_width / 2.0
        self.center_y = self.surface_height / 2.0

        red_radius = 50
        yellow_radius = 18

        self.red_circle = RedCircle(red_radius, (255, 0, 0), wait_time=2.0, move_duration=3.0)
        self.blue_circle = BlueCircle(red_radius, (50, 100, 255), wait_after_red=3.0, fade_duration=2.0, move_duration=3.0)
        self.green_circle = GreenCircle(red_radius, (40, 200, 80), wait_after_blue=5.0, move_duration=1.0, fade_duration=1.0)
        self.yellow_circle = YellowCircle(yellow_radius, (255, 215, 64), fade_duration=1.0)

        self._blue_triggered = False
        self._green_triggered = False
        self._yellow_fade_complete = False
        self._post_yellow_wait = 2.0
        self._post_yellow_timer = 0.0

    def _refresh_surface_metrics(self):
        surf = pygame.display.get_surface()
        if surf:
            self.surface_width, self.surface_height = surf.get_size()
            self.center_x = self.surface_width / 2.0
            self.center_y = self.surface_height / 2.0

    def on_enter(self):
        self._refresh_surface_metrics()
        start_x = self.center_x
        min_center_x = float(self.red_circle.radius)
        target_x = (start_x + min_center_x) / 2.0

        self.red_circle.reset(start_x, target_x)
        self.blue_circle.reset(start_x, self.surface_width)
        self.green_circle.reset(start_x, self.center_y)
        self.yellow_circle.reset(start_x)

        self._blue_triggered = False
        self._green_triggered = False
        self._yellow_fade_complete = False
        self._post_yellow_timer = 0.0

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.switch("MenuScreen")

    def update(self, timestamp: float):
        self._refresh_surface_metrics()
        self.red_circle.update(timestamp)
        self.blue_circle.update(timestamp)
        self.green_circle.update(timestamp, self.yellow_circle.center_x, self.center_y)
        self.yellow_circle.update(timestamp)

        if self.red_circle.finished and not self._blue_triggered:
            self.blue_circle.notify_red_finished()
            self._blue_triggered = True

        if self.blue_circle.finished and not self._green_triggered:
            self.green_circle.notify_blue_finished()
            self._green_triggered = True

        if self.green_circle.consume_fade_trigger():
            self.yellow_circle.start_fade()

        if not self._yellow_fade_complete and not self.yellow_circle.visible and not self.yellow_circle.fading:
            self._yellow_fade_complete = True
            self._post_yellow_timer = 0.0
        if self._yellow_fade_complete:
            self._post_yellow_timer += timestamp
            if self._post_yellow_timer >= self._post_yellow_wait:
                self.manager.switch("TutorialTextScreen1")

    def render(self, surface: pygame.Surface):
        surface.fill((0, 0, 0))
        center_y = self.center_y

        self.yellow_circle.render(surface, center_y)
        self.blue_circle.render(surface, center_y)
        self.green_circle.render(surface)
        self.red_circle.render(surface, center_y)

def main():
    pygame.init()
    size = (800, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pygame Window")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    manager = ScreenManager()
    manager.add("TitleScreen", TitleScreen(manager, font))
    manager.add("MenuScreen", MenuScreen(manager, font))
    manager.add("CutScene1", CutScene1(manager, font))
    manager.add("TutorialTextScreen1", TutorialTextScreen1(manager, font))
    manager.add("TutorialTextScreen2", TutorialTextScreen2(manager, font))
    manager.add("TutorialManaScreen", TutorialManaScreen(manager, font))
    manager.switch("TitleScreen")

    while manager.running:
        timestamp = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                manager.quit()
            else:
                manager.handle_event(event)

        manager.update(timestamp)
        manager.render(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
