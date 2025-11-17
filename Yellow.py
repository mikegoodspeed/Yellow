import sys

import pygame

from cutscene import CutScene1, ScreenManager
from menu import MenuScreen, TitleScreen
from tutorials import (
    TutorialManaScreen1,
    TutorialManaScreen2,
    TutorialManaScreen3,
    TutorialTextScreen1,
    TutorialTextScreen2,
)



def main():
    pygame.init()
    size = (800, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Yellow Tutorial Flow")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    manager = ScreenManager()
    manager.add("TitleScreen", TitleScreen(manager, font))
    manager.add("MenuScreen", MenuScreen(manager, font))
    manager.add("CutScene1", CutScene1(manager, font))
    manager.add("TutorialTextScreen1", TutorialTextScreen1(manager, font))
    manager.add("TutorialTextScreen2", TutorialTextScreen2(manager, font))
    manager.add("TutorialManaScreen1", TutorialManaScreen1(manager, font))
    manager.add("TutorialManaScreen2", TutorialManaScreen2(manager, font))
    manager.add("TutorialManaScreen3", TutorialManaScreen3(manager, font))
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
