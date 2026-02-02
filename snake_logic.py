from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable


Direction = tuple[int, int]


def _is_opposite(a: Direction, b: Direction) -> bool:
    return a[0] == -b[0] and a[1] == -b[1]


@dataclass
class SnakeGame:
    grid_width: int
    grid_height: int
    rng: random.Random
    snake: list[tuple[int, int]]
    direction: Direction
    food: tuple[int, int] | None
    score: int
    alive: bool
    grow_pending: int

    @classmethod
    def create(cls, grid_width: int, grid_height: int, rng: random.Random | None = None) -> "SnakeGame":
        if rng is None:
            rng = random.Random()
        start_x = grid_width // 2
        start_y = grid_height // 2
        snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        game = cls(
            grid_width=grid_width,
            grid_height=grid_height,
            rng=rng,
            snake=snake,
            direction=(1, 0),
            food=None,
            score=0,
            alive=True,
            grow_pending=0,
        )
        game.food = game._spawn_food()
        return game

    def reset(self) -> None:
        new = SnakeGame.create(self.grid_width, self.grid_height, self.rng)
        self.snake = new.snake
        self.direction = new.direction
        self.food = new.food
        self.score = 0
        self.alive = True
        self.grow_pending = 0

    def set_direction(self, direction: Direction) -> None:
        if not _is_opposite(direction, self.direction):
            self.direction = direction

    def step(self) -> None:
        if not self.alive:
            return
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        if not (0 <= new_head[0] < self.grid_width and 0 <= new_head[1] < self.grid_height):
            self.alive = False
            return

        tail = self.snake[-1]
        body = set(self.snake)
        if new_head in body and not (self.grow_pending == 0 and new_head == tail):
            self.alive = False
            return

        self.snake.insert(0, new_head)

        if self.food is not None and new_head == self.food:
            self.score += 1
            self.grow_pending += 1
            self.food = self._spawn_food()

        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.snake.pop()

    def _spawn_food(self) -> tuple[int, int] | None:
        empty = self._empty_cells()
        if not empty:
            return None
        return self.rng.choice(empty)

    def _empty_cells(self) -> list[tuple[int, int]]:
        body = set(self.snake)
        return [
            (x, y)
            for y in range(self.grid_height)
            for x in range(self.grid_width)
            if (x, y) not in body
        ]

    def snapshot(self) -> dict:
        return {
            "snake": list(self.snake),
            "direction": self.direction,
            "food": self.food,
            "score": self.score,
            "alive": self.alive,
            "grow_pending": self.grow_pending,
        }

    def load(self, snapshot: dict) -> None:
        self.snake = list(snapshot["snake"])
        self.direction = tuple(snapshot["direction"])
        self.food = snapshot["food"]
        self.score = int(snapshot["score"])
        self.alive = bool(snapshot["alive"])
        self.grow_pending = int(snapshot["grow_pending"])


__all__ = ["SnakeGame"]
