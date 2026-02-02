from __future__ import annotations

import random

import pygame

from cutscene import Screen, ScreenManager
from snake_logic import SnakeGame


class SnakeScreen(Screen):
    def __init__(self, manager: ScreenManager, font: pygame.font.Font):
        super().__init__(manager)
        self.font = font
        self.cell_size = 24
        self.top_padding = 60
        self.tick_interval = 0.12
        self.accumulator = 0.0
        self.game: SnakeGame | None = None
        self.queued_direction: tuple[int, int] | None = None
        self.paused = False
        self.rng = random.Random(7)
        self.last_surface_size: tuple[int, int] | None = None

    def on_enter(self):
        self._reset_game()

    def handle_event(self, event: pygame.event.Event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.manager.switch("menu")
            return
        if event.key in (pygame.K_r, pygame.K_RETURN):
            if self.game and not self.game.alive:
                self._reset_game()
            return
        if event.key in (pygame.K_SPACE, pygame.K_p):
            if self.game and self.game.alive:
                self.paused = not self.paused
            return

        direction = None
        if event.key in (pygame.K_UP, pygame.K_w):
            direction = (0, -1)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            direction = (0, 1)
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            direction = (-1, 0)
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            direction = (1, 0)
        if direction is not None:
            self.queued_direction = direction

    def update(self, dt: float):
        if not self.game or self.paused or not self.game.alive:
            return
        self.accumulator += dt
        while self.accumulator >= self.tick_interval:
            if self.queued_direction is not None:
                self.game.set_direction(self.queued_direction)
                self.queued_direction = None
            self.game.step()
            self.accumulator -= self.tick_interval

    def render(self, surface: pygame.Surface):
        self._ensure_game(surface)
        if not self.game:
            return

        background = (12, 16, 18)
        surface.fill(background)

        board_rect = self._board_rect(surface)
        pygame.draw.rect(surface, (30, 34, 38), board_rect)
        pygame.draw.rect(surface, (70, 70, 70), board_rect, 2)

        self._draw_cells(surface, board_rect)
        self._draw_hud(surface)

        if self.paused and self.game.alive:
            self._draw_center_message(surface, "Paused", "Space to resume")
        elif not self.game.alive:
            self._draw_center_message(surface, "Game Over", "Press R or Enter to restart")

    def _reset_game(self):
        self.accumulator = 0.0
        self.queued_direction = None
        self.paused = False
        self.game = None
        self.last_surface_size = None

    def _ensure_game(self, surface: pygame.Surface):
        size = surface.get_size()
        if self.game and self.last_surface_size == size:
            return
        grid_width = max(10, size[0] // self.cell_size)
        grid_height = max(10, (size[1] - self.top_padding) // self.cell_size)
        self.game = SnakeGame.create(grid_width, grid_height, self.rng)
        self.last_surface_size = size

    def _board_rect(self, surface: pygame.Surface) -> pygame.Rect:
        grid_width = self.game.grid_width if self.game else 0
        grid_height = self.game.grid_height if self.game else 0
        width = grid_width * self.cell_size
        height = grid_height * self.cell_size
        x = (surface.get_width() - width) // 2
        y = self.top_padding
        return pygame.Rect(x, y, width, height)

    def _draw_cells(self, surface: pygame.Surface, board_rect: pygame.Rect):
        if not self.game:
            return
        padding = 3
        body_color = (90, 200, 120)
        head_color = (130, 240, 160)
        food_color = (220, 80, 60)

        for i, (x, y) in enumerate(self.game.snake):
            cell_rect = pygame.Rect(
                board_rect.left + x * self.cell_size + padding,
                board_rect.top + y * self.cell_size + padding,
                self.cell_size - padding * 2,
                self.cell_size - padding * 2,
            )
            color = head_color if i == 0 else body_color
            pygame.draw.rect(surface, color, cell_rect)

        if self.game.food is not None:
            fx, fy = self.game.food
            food_rect = pygame.Rect(
                board_rect.left + fx * self.cell_size + padding,
                board_rect.top + fy * self.cell_size + padding,
                self.cell_size - padding * 2,
                self.cell_size - padding * 2,
            )
            pygame.draw.rect(surface, food_color, food_rect)

    def _draw_hud(self, surface: pygame.Surface):
        if not self.game:
            return
        label_color = (220, 220, 220)
        score_text = self.font.render(f"Score: {self.game.score}", True, label_color)
        hint_text = self.font.render("Arrows/WASD to move. Esc: Menu", True, (160, 160, 160))
        surface.blit(score_text, (16, 12))
        surface.blit(hint_text, (16, 34))

    def _draw_center_message(self, surface: pygame.Surface, title: str, subtitle: str):
        title_text = self.font.render(title, True, (240, 240, 240))
        subtitle_text = self.font.render(subtitle, True, (190, 190, 190))
        rect = title_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 10))
        sub_rect = subtitle_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 24))
        surface.blit(title_text, rect)
        surface.blit(subtitle_text, sub_rect)


__all__ = ["SnakeScreen"]
