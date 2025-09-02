import pygame as pg
import pygame_gui

def show_config_menu() -> tuple[int, int, int, bool]:
    """
    Show the configuration menu for the game.

    Returns:
        tuple[int, int, int, bool]: A tuple containing the cell size, snake speed, and wether to run the game.
    """
    WINDOW_SIZE = (800, 600)
    config_screen = pg.display.set_mode(WINDOW_SIZE)
    manager = pygame_gui.UIManager(WINDOW_SIZE)

    start_btn = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((350, 100), (100, 50)),
        text='Start',
        manager=manager
    )

    cells_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pg.Rect((300, 200), (200, 50)),
        start_value=30,
        value_range=(5, 40),
        manager=manager
    )

    cells_label = pygame_gui.elements.UILabel(
        relative_rect=pg.Rect((500, 200), (120, 50)),
        text=f'Cell Size: {int(cells_slider.get_current_value())}',
        manager=manager
    )

    snake_speed_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pg.Rect((300, 300), (200, 50)),
        start_value=150,
        value_range=(50, 350),
        manager=manager
    )

    snake_speed_label = pygame_gui.elements.UILabel(
        relative_rect=pg.Rect((500, 300), (120, 50)),
        text=f'Snake Speed: {int(snake_speed_slider.get_current_value())}',
        manager=manager
    )

    board_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pg.Rect((300, 400), (200, 50)),
        start_value=15,
        value_range=(5, 25),
        manager=manager
    )

    board_label = pygame_gui.elements.UILabel(
        relative_rect=pg.Rect((500, 400), (120, 50)),
        text=f'Board: {int(board_slider.get_current_value())}x{int(board_slider.get_current_value())}',
        manager=manager
    )

    quit_btn = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((350, 500), (100, 50)),
        text='Quit',
        manager=manager
    )

    running = True
    board_size = int(board_slider.get_current_value())
    cell_size = int(cells_slider.get_current_value())
    snake_speed = int(snake_speed_slider.get_current_value())

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return board_size, cell_size, snake_speed, False

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == board_slider:
                    board_label.set_text(f'Board: {int(board_slider.get_current_value())}x{int(board_slider.get_current_value())}')
                if event.ui_element == cells_slider:
                    cells_label.set_text(f'Cell Size: {int(cells_slider.get_current_value())}')
                if event.ui_element == snake_speed_slider:
                    snake_speed_label.set_text(f'Snake Speed: {int(snake_speed_slider.get_current_value())}')

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_btn:
                    board_size = int(board_slider.get_current_value())
                    cell_size = int(cells_slider.get_current_value())
                    snake_speed = int(snake_speed_slider.get_current_value())
                    min_value = snake_speed_slider.value_range[0]
                    max_value = snake_speed_slider.value_range[1]
                    snake_speed = abs(snake_speed - (max_value - min_value))

                    running = False
                    return board_size, cell_size, snake_speed, True
                
                if event.ui_element == quit_btn:
                    board_size = int(board_slider.get_current_value())
                    cell_size = int(cells_slider.get_current_value())
                    snake_speed = int(snake_speed_slider.get_current_value())
                    running = False
                    return board_size, cell_size, snake_speed, False
            manager.process_events(event)

        manager.update(60)
        config_screen.fill((40, 40, 40))
        manager.draw_ui(config_screen)
        pg.display.update()
