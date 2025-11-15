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


class GameScreen(Screen):
    def __init__(self, manager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font
        self.pos = [400, 300]
        self.velocity = [120, 80]  # px/sec

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.switch("menu")

    def update(self, dt: float):
        # simple movement bouncing the circle
        for i in (0, 1):
            self.pos[i] += self.velocity[i] * dt
        w, h = 800, 600
        if self.pos[0] < 50 or self.pos[0] > w - 50:
            self.velocity[0] *= -1
        if self.pos[1] < 50 or self.pos[1] > h - 50:
            self.velocity[1] *= -1

    def render(self, surface):
        background_color = (18, 40, 18)
        surface.fill(background_color)
        circle_color = (235, 200, 110)
        circle_center = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(surface, circle_color, circle_center, 50)
        hint_color = (180, 180, 180)
        hint = self.font.render("Esc: Back to menu", True, hint_color)
        hint_position = (10, 10)
        surface.blit(hint, hint_position)


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
    manager.add("game", GameScreen(manager, font))
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



