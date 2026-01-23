import sys

import pygame

from cutscene import Screen, ScreenManager


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
        self.blue_radius = 40
        self.mellow_radius = 40
        self.screen_size = (800, 600)
        self.blue_speed = 240
        self.mellow_speed = 150
        self.blue_input = {"up": False, "down": False, "left": False, "right": False}
        self.mellow_pos = [self.screen_size[0] * 0.25, self.screen_size[1] * 0.5]
        self.mellow_velocity = [self.mellow_speed, self.mellow_speed * 0.6]
        self.current_blue = self._spawn_blue()
        self.converted_blues: list[dict] = []
        self.pending_spawn_timer = 0.0
        self.red_center = [self.screen_size[0] * 5 / 6, self.screen_size[1] / 2]
        self.red_radius = 55
        self.ai_radius = 35
        self.ai_speed = 180
        self.ai_pos = [self.screen_size[0] * 0.5, self.screen_size[1] * 0.25]
        self.ai_velocity = [0.0, self.ai_speed]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.switch("menu")
            elif event.key == pygame.K_UP:
                self.blue_input["up"] = True
            elif event.key == pygame.K_DOWN:
                self.blue_input["down"] = True
            elif event.key == pygame.K_LEFT:
                self.blue_input["left"] = True
            elif event.key == pygame.K_RIGHT:
                self.blue_input["right"] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.blue_input["up"] = False
            elif event.key == pygame.K_DOWN:
                self.blue_input["down"] = False
            elif event.key == pygame.K_LEFT:
                self.blue_input["left"] = False
            elif event.key == pygame.K_RIGHT:
                self.blue_input["right"] = False

    def update(self, dt: float):
        if self.current_blue:
            dx = self.blue_input["right"] - self.blue_input["left"]
            dy = self.blue_input["down"] - self.blue_input["up"]
            if dx != 0 or dy != 0:
                length = (dx * dx + dy * dy) ** 0.5
                vel_x = (dx / length) * self.blue_speed
                vel_y = (dy / length) * self.blue_speed
            else:
                vel_x = vel_y = 0
            self.current_blue["pos"][0] += vel_x * dt
            self.current_blue["pos"][1] += vel_y * dt
            min_x = self.blue_radius
            max_x = self.screen_size[0] - self.blue_radius
            min_y = self.blue_radius
            max_y = self.screen_size[1] - self.blue_radius
            self.current_blue["pos"][0] = max(min_x, min(max_x, self.current_blue["pos"][0]))
            self.current_blue["pos"][1] = max(min_y, min(max_y, self.current_blue["pos"][1]))
        else:
            self.pending_spawn_timer -= dt
            if self.pending_spawn_timer <= 0:
                self.current_blue = self._spawn_blue()
        for i in (0, 1):
            self.mellow_pos[i] += self.mellow_velocity[i] * dt
        if self.mellow_pos[0] - self.mellow_radius < 0 or self.mellow_pos[0] + self.mellow_radius > self.screen_size[0]:
            self.mellow_velocity[0] *= -1
            self.mellow_pos[0] = max(self.mellow_radius, min(self.screen_size[0] - self.mellow_radius, self.mellow_pos[0]))
        if self.mellow_pos[1] - self.mellow_radius < 0 or self.mellow_pos[1] + self.mellow_radius > self.screen_size[1]:
            self.mellow_velocity[1] *= -1
            self.mellow_pos[1] = max(self.mellow_radius, min(self.screen_size[1] - self.mellow_radius, self.mellow_pos[1]))
        for converted in self.converted_blues:
            converted["pos"][0] += converted["velocity"][0] * dt
            converted["pos"][1] += converted["velocity"][1] * dt
            if converted["pos"][0] - self.blue_radius < 0 or converted["pos"][0] + self.blue_radius > self.screen_size[0]:
                converted["velocity"][0] *= -1
                converted["pos"][0] = max(self.blue_radius, min(self.screen_size[0] - self.blue_radius, converted["pos"][0]))
            if converted["pos"][1] - self.blue_radius < 0 or converted["pos"][1] + self.blue_radius > self.screen_size[1]:
                converted["velocity"][1] *= -1
                converted["pos"][1] = max(self.blue_radius, min(self.screen_size[1] - self.blue_radius, converted["pos"][1]))
        if self.current_blue and self.current_blue["state"] == "active":
            self._handle_blue_contact(dt)
        self._update_ai(dt)
        self._check_ai_collision()
        if self._check_red_collision():
            self.manager.switch("end")

    def render(self, surface):
        background_color = (18, 40, 18)
        surface.fill(background_color)
        pygame.draw.circle(surface, (200, 30, 30), (int(self.red_center[0]), int(self.red_center[1])), self.red_radius)
        mellow_color = (200, 200, 250)
        pygame.draw.circle(surface, mellow_color, (int(self.mellow_pos[0]), int(self.mellow_pos[1])), self.mellow_radius)
        converted_color = (160, 160, 180)
        for converted in self.converted_blues:
            pygame.draw.circle(surface, converted_color, (int(converted["pos"][0]), int(converted["pos"][1])), self.blue_radius)
        if self.current_blue:
            blue_color = (50, 120, 255)
            pygame.draw.circle(surface, blue_color, (int(self.current_blue["pos"][0]), int(self.current_blue["pos"][1])), self.blue_radius)
        ai_color = (100, 250, 120)
        pygame.draw.circle(surface, ai_color, (int(self.ai_pos[0]), int(self.ai_pos[1])), self.ai_radius)
        hint_color = (180, 180, 180)
        hint = self.font.render("Use arrows to move Blue. Esc: Back to menu", True, hint_color)
        surface.blit(hint, (10, 10))

    def _update_ai(self, dt: float):
        dx = self.mellow_pos[0] - self.ai_pos[0]
        dy = self.mellow_pos[1] - self.ai_pos[1]
        dist = max(1e-6, (dx * dx + dy * dy) ** 0.5)
        self.ai_velocity = [dx / dist * self.ai_speed, dy / dist * self.ai_speed]
        self.ai_pos[0] += self.ai_velocity[0] * dt
        self.ai_pos[1] += self.ai_velocity[1] * dt
        if self.ai_pos[0] - self.ai_radius < 0 or self.ai_pos[0] + self.ai_radius > self.screen_size[0]:
            self.ai_velocity[0] *= -1
            self.ai_pos[0] = max(self.ai_radius, min(self.screen_size[0] - self.ai_radius, self.ai_pos[0]))
        if self.ai_pos[1] - self.ai_radius < 0 or self.ai_pos[1] + self.ai_radius > self.screen_size[1]:
            self.ai_velocity[1] *= -1
            self.ai_pos[1] = max(self.ai_radius, min(self.screen_size[1] - self.ai_radius, self.ai_pos[1]))

    def _check_ai_collision(self):
        dx = self.mellow_pos[0] - self.ai_pos[0]
        dy = self.mellow_pos[1] - self.ai_pos[1]
        dist_sq = dx * dx + dy * dy
        min_dist = self.ai_radius + self.mellow_radius
        if 0 < dist_sq <= min_dist * min_dist:
            dist = dist_sq ** 0.5
            nx = dx / dist
            ny = dy / dist
            self.mellow_velocity[0] = nx * self.mellow_speed
            self.mellow_velocity[1] = ny * self.mellow_speed
            self.mellow_pos[0] = self.ai_pos[0] + nx * min_dist
            self.mellow_pos[1] = self.ai_pos[1] + ny * min_dist
    def _handle_blue_contact(self, dt: float):
        dx = self.mellow_pos[0] - self.current_blue["pos"][0]
        dy = self.mellow_pos[1] - self.current_blue["pos"][1]
        dist_sq = dx * dx + dy * dy
        min_dist = self.blue_radius + self.mellow_radius
        if dist_sq > 0 and dist_sq <= min_dist * min_dist:
            if not self.current_blue["contact_started"]:
                self.current_blue["contact_started"] = True
                self.current_blue["contact_timer"] = 0.0
            self.current_blue["contact_timer"] += dt
            dist = dist_sq**0.5
            nx = dx / dist
            ny = dy / dist
            self.mellow_velocity[0] = nx * self.mellow_speed
            self.mellow_velocity[1] = ny * self.mellow_speed
            self.mellow_pos[0] = self.current_blue["pos"][0] + nx * min_dist
            self.mellow_pos[1] = self.current_blue["pos"][1] + ny * min_dist
            if self.current_blue["contact_timer"] >= 10.0:
                self._convert_current_blue(nx, ny)
        elif self.current_blue["contact_started"]:
            self.current_blue["contact_timer"] += dt

    def _convert_current_blue(self, nx: float, ny: float):
        converted = self.current_blue.copy()
        converted["state"] = "converted"
        converted["velocity"] = [nx * self.mellow_speed, ny * self.mellow_speed]
        self.converted_blues.append(converted)
        self.current_blue = None
        self.pending_spawn_timer = 1.0

    def _spawn_blue(self):
        return {
            "pos": [
                self.screen_size[0] - self.blue_radius - 10,
                self.blue_radius + 10,
            ],
            "state": "active",
            "contact_started": False,
            "contact_timer": 0.0,
        }

    def _check_red_collision(self):
        def hits_red(position, radius):
            dx = position[0] - self.red_center[0]
            dy = position[1] - self.red_center[1]
            return dx * dx + dy * dy <= (radius + self.red_radius) ** 2

        if hits_red(self.mellow_pos, self.mellow_radius):
            return True
        for converted in self.converted_blues:
            if hits_red(converted["pos"], self.blue_radius):
                return True
        return False


class EndScreen(Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font
        self.elapsed = 0.0
       

   

    def render(self, surface):
        surface.fill(pygame.Color("black"))
        text = self.font.render("Game Over", True, (255, 0, 0))
        rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        surface.blit(text, rect)
        

    def _show_button(self):
        display = pygame.display.get_surface()
        if not display:
            return
        width, height = display.get_size()
        button_surface = self.font.render(self.button_text, True, (255, 255, 255))
        inner_rect = button_surface.get_rect()
        inner_rect.centerx = width // 2
        inner_rect.top = height // 2 + 300

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.switch("game")

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
    manager.add("end", EndScreen(manager, font))
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
