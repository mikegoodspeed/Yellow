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

    def update(self, dt: float):
        if self.active:
            self.active.update(dt)

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

    def update(self, dt: float):
        pass

    def render(self, surface: pygame.Surface):
        pass


class TitleScreen(Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            # any key moves to menu
            self.manager.switch("menu")

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
                    self.manager.switch("game")
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


class CutScene1 (Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font
        self.radius = 50
        self.color = (255, 0, 0)  # pure red

        # small yellow reveal circle (drawn first, so red covers it until moved)
        self.yellow_radius = 18
        self.yellow_color_rgb = (255, 215, 64)  # Golden yellow

        # timing/motion state for red movement
        self.wait_time = 5.0       # seconds to wait before moving
        self.move_duration = 3.0   # seconds to complete the move
        self._elapsed = 0.0
        self._move_elapsed = 0.0
        self._moving = False
        self._finished = False     # stop repeating after done

        self._start_x = None
        self._target_x = None
        self._current_x = None

        # blue (same size as red)
        self.blue_radius = self.radius
        self.blue_color_rgb = (50, 100, 255)
        self.blue_wait_after_red = 3.0
        self.blue_fade_duration = 2.0
        self.blue_move_duration = 3.0
        self._blue_wait_elapsed = 0.0
        self._blue_fade_elapsed = 0.0
        self._blue_started = False
        self._blue_fully_visible = False
        self._blue_x = None
        self._blue_moving = False
        self._blue_move_elapsed = 0.0
        self._blue_start_x = None
        self._blue_target_x = None
        self._blue_finished = False

        # green sequence (appears after blue finishes + wait)
        self.green_radius = self.radius
        self.green_color_rgb = (40, 200, 80)   # green color
        self.green_wait_after_all = 10.0       # wait after blue finished
        self.green_move_duration = 1.0         # move time to yellow
        self.green_fade_duration = 1.0         # fade-out duration once in place
        self._green_wait_elapsed = 0.0
        self._green_started = False
        self._green_moving = False
        self._green_move_elapsed = 0.0
        self._green_x = None
        self._green_y = None
        self._green_start_x = None
        self._green_start_y = None
        self._green_target_x = None
        self._green_target_y = None
        self._green_in_place = False
        self._green_fade_elapsed = 0.0
        self._green_fading = False

        # yellow fade state (fades out when green fades out)
        self._yellow_fading = False
        self._yellow_fade_elapsed = 0.0
        self._yellow_fade_duration = self.green_fade_duration

    def on_enter(self):
        surf = pygame.display.get_surface()
        if surf:
            w, h = surf.get_size()
            self._start_x = w / 2.0
            min_center_x = float(self.radius)
            self._target_x = (self._start_x + min_center_x) / 2.0
            self._current_x = self._start_x
            self._blue_x = self._start_x
        self._elapsed = 0.0
        self._move_elapsed = 0.0
        self._moving = False
        self._finished = False

        self._blue_wait_elapsed = 0.0
        self._blue_fade_elapsed = 0.0
        self._blue_started = False
        self._blue_fully_visible = False
        self._blue_moving = False
        self._blue_move_elapsed = 0.0
        self._blue_start_x = None
        self._blue_target_x = None
        self._blue_finished = False

        # green reset
        self._green_wait_elapsed = 0.0
        self._green_started = False
        self._green_moving = False
        self._green_move_elapsed = 0.0
        self._green_x = None
        self._green_y = None
        self._green_start_x = None
        self._green_start_y = None
        self._green_target_x = None
        self._green_target_y = None
        self._green_in_place = False
        self._green_fade_elapsed = 0.0
        self._green_fading = False

        self._yellow_fading = False
        self._yellow_fade_elapsed = 0.0

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.switch("menu")

    def update(self, dt: float):
        # advance blue fade after red finished
        if self._finished and not self._blue_fully_visible:
            if not self._blue_started:
                self._blue_wait_elapsed += dt
                if self._blue_wait_elapsed >= self.blue_wait_after_red:
                    self._blue_started = True
                    self._blue_fade_elapsed = 0.0
            else:
                self._blue_fade_elapsed += dt
                if self._blue_fade_elapsed >= self.blue_fade_duration:
                    self._blue_fade_elapsed = self.blue_fade_duration
                    self._blue_fully_visible = True

        # start blue movement when fade complete
        if self._blue_fully_visible and not self._blue_finished and not self._blue_moving:
            surf = pygame.display.get_surface()
            if surf:
                w, h = surf.get_size()
                max_center_x = float(w - self.radius)
            else:
                max_center_x = (self._blue_x or 0)
            self._blue_start_x = float(self._blue_x if self._blue_x is not None else self._start_x or 0)
            self._blue_target_x = (self._blue_start_x + max_center_x) / 2.0
            self._blue_moving = True
            self._blue_move_elapsed = 0.0

        # advance blue movement
        if self._blue_moving:
            self._blue_move_elapsed += dt
            t = min(1.0, self._blue_move_elapsed / max(1e-6, self.blue_move_duration))
            if self._blue_start_x is not None and self._blue_target_x is not None:
                self._blue_x = self._blue_start_x + (self._blue_target_x - self._blue_start_x) * t
            if t >= 1.0:
                self._blue_x = self._blue_target_x
                self._blue_moving = False
                self._blue_finished = True

        # after blue finished, start counting towards green
        if self._blue_finished and not self._green_started:
            self._green_wait_elapsed += dt
            if self._green_wait_elapsed >= self.green_wait_after_all:
                self._green_started = True
                # initialize green start above-left of yellow
                yellow_x = float(self._start_x if self._start_x is not None else 0.0)
                surf = pygame.display.get_surface()
                if surf:
                    _, h = surf.get_size()
                    center_y = h / 2.0
                else:
                    center_y = 0.0
                # slightly left and above
                offset_x = -30.0
                offset_y = -20.0
                self._green_start_x = yellow_x + offset_x
                self._green_start_y = center_y + offset_y
                self._green_x = self._green_start_x
                self._green_y = self._green_start_y

        # start green movement once started and not yet moving
        if self._green_started and not self._green_moving and not self._green_in_place:
            # set target to yellow's exact standing place (center_y and yellow_x)
            yellow_x = float(self._start_x if self._start_x is not None else 0.0)
            surf = pygame.display.get_surface()
            if surf:
                _, h = surf.get_size()
                center_y = h / 2.0
            else:
                center_y = 0.0
            self._green_target_x = yellow_x
            self._green_target_y = center_y
            self._green_moving = True
            self._green_move_elapsed = 0.0

        # advance green movement
        if self._green_moving:
            self._green_move_elapsed += dt
            t = min(1.0, self._green_move_elapsed / max(1e-6, self.green_move_duration))
            if self._green_start_x is not None and self._green_target_x is not None:
                self._green_x = self._green_start_x + (self._green_target_x - self._green_start_x) * t
            if self._green_start_y is not None and self._green_target_y is not None:
                self._green_y = self._green_start_y + (self._green_target_y - self._green_start_y) * t
            if t >= 1.0:
                self._green_x = self._green_target_x
                self._green_y = self._green_target_y
                self._green_moving = False
                self._green_in_place = True
                # start fade-out of green and yellow immediately
                self._green_fading = True
                self._green_fade_elapsed = 0.0
                self._yellow_fading = True
                self._yellow_fade_elapsed = 0.0

        # advance fades if active
        if self._green_fading:
            self._green_fade_elapsed += dt
            if self._green_fade_elapsed >= self.green_fade_duration:
                self._green_fade_elapsed = self.green_fade_duration
                self._green_fading = False  # green finished fading (now invisible)

        if self._yellow_fading:
            self._yellow_fade_elapsed += dt
            if self._yellow_fade_elapsed >= self._yellow_fade_duration:
                self._yellow_fade_elapsed = self._yellow_fade_duration
                self._yellow_fading = False

        # existing red movement logic (only if not finished)
        if not self._finished:
            # lazy initialize if needed
            if self._start_x is None:
                surf = pygame.display.get_surface()
                if surf:
                    w, h = surf.get_size()
                    self._start_x = w / 2.0
                    self._current_x = self._start_x
                    self._target_x = (self._start_x + float(self.radius)) / 2.0
                    if self._blue_x is None:
                        self._blue_x = self._start_x

            if not self._moving:
                self._elapsed += dt
                if self._elapsed >= self.wait_time:
                    self._moving = True
                    self._move_elapsed = 0.0
            else:
                self._move_elapsed += dt
                t = min(1.0, self._move_elapsed / max(1e-6, self.move_duration))
                if self._start_x is not None and self._target_x is not None:
                    self._current_x = self._start_x + (self._target_x - self._start_x) * t
                if t >= 1.0:
                    self._current_x = self._target_x
                    self._moving = False
                    self._finished = True
                    self._blue_wait_elapsed = 0.0

    def render(self, surface: pygame.Surface):
        surface.fill((0, 0, 0))  # pure black backdrop
        w, h = surface.get_size()
        center_y = h // 2

        yellow_x = int(self._start_x) if self._start_x is not None else (w // 2)

        # draw yellow via alpha surface so it can fade out when green fades
        if self._yellow_fading:
            y_alpha = int(255 * max(0.0, 1.0 - (self._yellow_fade_elapsed / max(1e-6, self._yellow_fade_duration))))
        else:
            # if green has finished fading and yellow not explicitly fading, keep visible
            y_alpha = 255
        y_alpha = max(0, min(255, y_alpha))
        dy = self.yellow_radius * 2
        yellow_surf = pygame.Surface((dy, dy), pygame.SRCALPHA)
        pygame.draw.circle(yellow_surf, (*self.yellow_color_rgb, y_alpha), (self.yellow_radius, self.yellow_radius), self.yellow_radius)
        surface.blit(yellow_surf, (yellow_x - self.yellow_radius, center_y - self.yellow_radius))

        # draw blue (with its fade) over yellow if active
        if self._blue_x is None:
            self._blue_x = yellow_x
        if self._blue_started or self._blue_fully_visible:
            if self._blue_fully_visible:
                b_alpha = 255
            else:
                b_alpha = int(255 * (self._blue_fade_elapsed / max(1e-6, self.blue_fade_duration)))
            b_alpha = max(0, min(255, b_alpha))
            d = self.blue_radius * 2
            blue_surf = pygame.Surface((d, d), pygame.SRCALPHA)
            blue_color = (*self.blue_color_rgb, b_alpha)
            pygame.draw.circle(blue_surf, blue_color, (self.blue_radius, self.blue_radius), self.blue_radius)
            bx = int(self._blue_x) - self.blue_radius
            by = center_y - self.blue_radius
            surface.blit(blue_surf, (bx, by))

        # draw green on top of yellow when started (with movement + fade)
        if self._green_started:
            # compute current alpha for green (if fading, alpha goes down)
            if self._green_fading:
                g_alpha = int(255 * max(0.0, 1.0 - (self._green_fade_elapsed / max(1e-6, self.green_fade_duration))))
            else:
                g_alpha = 255
            g_alpha = max(0, min(255, g_alpha))
            gd = self.green_radius * 2
            green_surf = pygame.Surface((gd, gd), pygame.SRCALPHA)
            pygame.draw.circle(green_surf, (*self.green_color_rgb, g_alpha), (self.green_radius, self.green_radius), self.green_radius)
            gx = int(self._green_x if self._green_x is not None else yellow_x) - self.green_radius
            gy = int(self._green_y if self._green_y is not None else center_y) - self.green_radius
            surface.blit(green_surf, (gx, gy))

        # then draw the red (moving) circle on top
        cx = int(self._current_x) if self._current_x is not None else (w // 2)
        pygame.draw.circle(surface, self.color, (cx, center_y), self.radius)

    def render(self, surface: pygame.Surface):
        surface.fill((0, 0, 0))  # pure black backdrop
        w, h = surface.get_size()
        center_y = h // 2

        yellow_x = int(self._start_x) if self._start_x is not None else (w // 2)

        # draw yellow via alpha surface so it can fade out when green fades
        if self._yellow_fading:
            y_alpha = int(255 * max(0.0, 1.0 - (self._yellow_fade_elapsed / max(1e-6, self._yellow_fade_duration))))
        else:
            # if green has finished fading and yellow not explicitly fading, keep visible
            y_alpha = 255
        y_alpha = max(0, min(255, y_alpha))
        dy = self.yellow_radius * 2
        yellow_surf = pygame.Surface((dy, dy), pygame.SRCALPHA)
        pygame.draw.circle(yellow_surf, (*self.or_rgb, y_alpha), (self.yellow_radius, self.yellow_radius), self.yellow_radius)
        surface.blit(yellow_surf, (yellow_x - self.yellow_radius, center_y - self.yellow_radius))

        # draw blue (with its fade) over yellow if active
        if self._blue_x is None:
            self._blue_x = yellow_x
        if self._blue_started or self._blue_fully_visible:
            if self._blue_fully_visible:
                b_alpha = 255
            else:
                b_alpha = int(255 * (self._blue_fade_elapsed / max(1e-6, self.blue_fade_duration)))
            b_alpha = max(0, min(255, b_alpha))
            d = self.blue_radius * 2
            blue_surf = pygame.Surface((d, d), pygame.SRCALPHA)
            blue_color = (*self.blue_color_rgb, b_alpha)
            pygame.draw.circle(blue_surf, blue_color, (self.blue_radius, self.blue_radius), self.blue_radius)
            bx = int(self._blue_x) - self.blue_radius
            by = center_y - self.blue_radius
            surface.blit(blue_surf, (bx, by))

        # draw green on top of yellow when started (with movement + fade)
        if self._green_started:
            # compute current alpha for green (if fading, alpha goes down)
            if self._green_fading:
                g_alpha = int(255 * max(0.0, 1.0 - (self._green_fade_elapsed / max(1e-6, self.green_fade_duration))))
            else:
                g_alpha = 255
            g_alpha = max(0, min(255, g_alpha))
            gd = self.green_radius * 2
            green_surf = pygame.Surface((gd, gd), pygame.SRCALPHA)
            pygame.draw.circle(green_surf, (*self.green_color_rgb, g_alpha), (self.green_radius, self.green_radius), self.green_radius)
            gx = int(self._green_x if self._green_x is not None else yellow_x) - self.green_radius
            gy = int(self._green_y if self._green_y is not None else center_y) - self.green_radius
            surface.blit(green_surf, (gx, gy))

        # then draw the red (moving) circle on top
        cx = int(self._current_x) if self._current_x is not None else (w // 2)
        pygame.draw.circle(surface, self.color, (cx, center_y), self.radius)

    def render(self, surface: pygame.Surface):  # noqa: F
        surface.fill((0, 0, 0))  # pure black backdrop
        w, h = surface.get_size()
        center_y = h // 2

        # yellow sits at the original center (start_x) so it will be revealed as red moves
        yellow_x = int(self._start_x) if self._start_x is not None else (w // 2)
        pygame.draw.circle(surface, self.yellow_color_rgb, (yellow_x, center_y), self.yellow_radius)

        # draw blue over yellow (use current blue position and current alpha)
        if self._blue_x is None:
            self._blue_x = yellow_x
        if self._blue_started or self._blue_fully_visible:
            if self._blue_fully_visible:
                alpha = 255
            else:
                alpha = int(255 * (self._blue_fade_elapsed / max(1e-6, self.blue_fade_duration)))
            alpha = max(0, min(255, alpha))

            d = self.blue_radius * 2
            blue_surf = pygame.Surface((d, d), pygame.SRCALPHA)
            blue_color = (*self.blue_color_rgb, alpha)
            pygame.draw.circle(blue_surf, blue_color, (self.blue_radius, self.blue_radius), self.blue_radius)
            bx = int(self._blue_x) - self.blue_radius
            by = center_y - self.blue_radius
            surface.blit(blue_surf, (bx, by))

        # then draw the red (moving) circle on top
        cx = int(self._current_x) if self._current_x is not None else (w // 2)
        pygame.draw.circle(surface, self.color, (cx, center_y), self.radius)

def main():
    pygame.init()
    size = (800, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pygame Window")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    manager = ScreenManager()
    manager.add("title", TitleScreen(manager, font))
    manager.add("menu", MenuScreen(manager, font))
    manager.add("game", CutScene1(manager, font))
    manager.switch("title")

    while manager.running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                manager.quit()
            else:
                manager.handle_event(event)

        manager.update(dt)
        manager.render(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()



