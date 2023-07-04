import pygame
import pygame_gui
from boid import Boid


class Settings:
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
    SCREEN_COLOR = (0, 0, 0)
    CLOCK_TICK = 60


def create_gui_elements(manager):
    gui_elements = {}
    gui_elements["align_slider"] = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((120, 20), (200, 20)),
        start_value=1.1,
        value_range=(0.0, 5.0),
        manager=manager
    )
    gui_elements["align_label"] = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((20, 20), (100, 20)),
        text="Alignment:",
        manager=manager
    )
    gui_elements["cohesion_slider"] = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((120, 50), (200, 20)),
        start_value=0.25,
        value_range=(0.0, 0.5),
        manager=manager
    )
    gui_elements["cohesion_label"] = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((20, 50), (100, 20)),
        text="Cohesion:",
        manager=manager
    )
    gui_elements["separation_slider"] = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((120, 80), (200, 20)),
        start_value=0.25,
        value_range=(0.0, 0.5),
        manager=manager
    )
    gui_elements["separation_label"] = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((20, 80), (100, 20)),
        text="Separation:",
        manager=manager
    )
    gui_elements["restart_button"] = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((120, 120), (100, 20)),
        text="Restart",
        manager=manager
    )
    return gui_elements


def handle_events(event, manager, gui_elements):
    global flock
    manager.process_events(event)
    if event.type == pygame.USEREVENT:
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == gui_elements["restart_button"]:
                flock = [Boid(screen_height=Settings.SCREEN_HEIGHT, screen_width=Settings.SCREEN_WIDTH) for _ in range(100)]


def main():
    pygame.init()
    screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))

    manager = pygame_gui.UIManager((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
    gui_elements = create_gui_elements(manager)

    global flock
    flock = [Boid(screen_height=Settings.SCREEN_HEIGHT, screen_width=Settings.SCREEN_WIDTH) for _ in range(100)]

    running = True
    clock = pygame.time.Clock()

    while running:
        time_delta = clock.tick(Settings.CLOCK_TICK) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_events(event, manager, gui_elements)

        manager.update(time_delta)

        gui_elements["align_label"].set_text(f'A: {gui_elements["align_slider"].get_current_value():.2f}')
        gui_elements["cohesion_label"].set_text(f'C: {gui_elements["cohesion_slider"].get_current_value():.2f}')
        gui_elements["separation_label"].set_text(f'S: {gui_elements["separation_slider"].get_current_value():.2f}')

        align_mult = gui_elements["align_slider"].get_current_value()
        cohesion_mult = gui_elements["cohesion_slider"].get_current_value()
        sep_mult = gui_elements["separation_slider"].get_current_value()

        screen.fill(Settings.SCREEN_COLOR)

        for boid in flock:
            boid.flock(flock, align_mult, cohesion_mult, sep_mult)
            boid.edges()
            boid.update()
            boid.show(screen)

        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
