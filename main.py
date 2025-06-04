import pygame

from gameobject import GameObject
from board import Board
from yochan import YoChan

pygame.init()

WIDTH = 1024
HEIGHT = 768
ASPECT = WIDTH/HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
render_surface = pygame.Surface((WIDTH, HEIGHT))

# Initialize game object constants
GameObject.WIDTH = WIDTH
GameObject.HEIGHT = HEIGHT


def get_scaled_rect(window_size):
    """Returns a rect where the internal surface should be drawn"""
    win_width, win_height = window_size
    win_ratio = win_width/win_height
    if win_ratio > ASPECT:
        # If the window is too high
        scale = win_height / HEIGHT
        scaled_width = int(WIDTH * scale)
        x_offset = (win_width - scaled_width) // 2
        return pygame.Rect(x_offset, 0, scaled_width, win_height)
    else:
        # If it's too wide
        scale = win_width / WIDTH
        scaled_height = int(HEIGHT * scale)
        y_offset = (win_height - scaled_height) // 2
        return pygame.Rect(0, y_offset, win_width, scaled_height)


# Create the gameboard
gameboard = Board()
gameboard.add_fishcube(1, 1)
gameboard.add_fishcube(1, 2)
gameboard.add_fishcube(1, 3)
gameboard.add_fishcube(1, 4)

gameboard.add_fishcube(3, 1)
gameboard.add_fishcube(3, 2)
gameboard.add_fishcube(3, 3)
gameboard.add_fishcube(3, 4)

# Create yochan
yochan = YoChan(gameboard)

clock = pygame.time.Clock()
delta_time = 0.1

running = True

print(gameboard.grid)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Make window resiable
            width, height = event.size
            if width < WIDTH:
                width = WIDTH
            if height < HEIGHT:
                height = HEIGHT
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            pass
        yochan.handle_input(event)

    # Logical updates here
    gameboard.update(delta_time)
    yochan.update(delta_time, gameboard)  # She can "see" the board

    # Draw graphics
    render_surface.fill((0, 0, 64))
    gameboard.draw(render_surface)
    yochan.draw(render_surface)

    # Scale and draw render_surface properly
    screen.fill((0, 0, 0))
    rect = get_scaled_rect(screen.get_size())
    scaled_surface = pygame.transform.smoothscale(render_surface,
                                                  (rect.width, rect.height))
    screen.blit(scaled_surface, rect.topleft)

    pygame.display.flip()
    delta_time = clock.tick(60) / 1000  # Milliseconds
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()
