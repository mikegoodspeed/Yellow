import random
import unittest

from snake_logic import SnakeGame


class SnakeLogicTests(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(0)
        self.game = SnakeGame.create(8, 6, self.rng)

    def test_moves_forward(self):
        head = self.game.snake[0]
        self.game.step()
        new_head = self.game.snake[0]
        self.assertEqual(new_head, (head[0] + 1, head[1]))
        self.assertEqual(len(self.game.snake), 3)

    def test_prevents_reverse(self):
        self.game.set_direction((-1, 0))
        self.game.step()
        self.assertEqual(self.game.snake[0][0], (8 // 2) + 1)

    def test_wall_collision(self):
        self.game.snake = [(7, 3), (6, 3), (5, 3)]
        self.game.direction = (1, 0)
        self.game.step()
        self.assertFalse(self.game.alive)

    def test_growth_on_food(self):
        head = self.game.snake[0]
        self.game.food = (head[0] + 1, head[1])
        self.game.step()
        self.assertEqual(self.game.score, 1)
        self.assertEqual(len(self.game.snake), 4)

    def test_food_not_on_snake(self):
        self.game.snake = [(x, 0) for x in range(8)]
        food = self.game._spawn_food()
        self.assertIsNotNone(food)
        self.assertNotIn(food, self.game.snake)

    def test_self_collision(self):
        self.game.snake = [(3, 3), (3, 4), (2, 4), (2, 3)]
        self.game.direction = (0, 1)
        self.game.step()
        self.assertFalse(self.game.alive)


if __name__ == "__main__":
    unittest.main()
