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
        self.yellow_color = (255, 215, 64) # Golden yellow

        # timing/motion state
        self.wait_time = 5.0       # seconds to wait before moving
        self.move_duration = 3.0   # seconds to complete the move
        self._elapsed = 0.0
        self._move_elapsed = 0.0
        self._moving = False
        self._finished = False     # stop repeating after done

        # positions (initialized on_enter)
        self._start_x = None
        self._target_x = None
        self._current_x = None


    def on_enter(self):
        # compute positions once we have a display surface
        surf = pygame.display.get_surface()
        if surf:
            w, h = surf.get_size()
            self._start_x = w / 2.0
            min_center_x = float(self.radius)  # keep circle fully on-screen
            # target is halfway between center and leftmost allowed center
            self._target_x = (self._start_x + min_center_x) / 2.0
            self._current_x = self._start_x
        self._elapsed = 0.0
        self._move_elapsed = 0.0
        self._moving = False
        self._finished = False

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.switch("menu")

    def update(self, dt: float):
        # if finished, stand still
        if self._finished:
            return

        # lazy initialize if needed
        if self._start_x is None:
            surf = pygame.display.get_surface()
            if surf:
                w, h = surf.get_size()
                self._start_x = w / 2.0
                self._current_x = self._start_x
                self._target_x = (self._start_x + float(self.radius)) / 2.0

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
                # ensure exact final position and stop repeating
                self._current_x = self._target_x
                self._moving = False
                self._finished = True

    def render(self, surface: pygame.Surface):
        surface.fill((0, 0, 0))  # pure black backdrop
        w, h = surface.get_size()
        center_y = h // 2

        # yellow sits at the original center (start_x) so it will be revealed as red moves
        yellow_x = int(self._start_x) if self._start_x is not None else (w // 2)
        pygame.draw.circle(surface, self.yellow_color, (yellow_x, center_y), self.yellow_radius)

        # then draw the red (moving) circle on top
        cx = int(self._current_x) if self._current_x is not None else (w // 2)
        pygame.draw.circle(surface, self.color, (cx, center_y), self.radius)
# ...existing code...

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



