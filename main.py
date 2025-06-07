import pygame
import asyncio

from gameobject import GameObject
from board import Board
from yochan import YoChan
from tsuki import Tsuki
from trainer import Trainer
from timer import Timer
from scorecard import ScoreCard

from background import Background

from menu import Menu

pygame.init()

WIDTH = 1024
HEIGHT = 768
ASPECT = WIDTH/HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
render_surface = pygame.Surface((WIDTH, HEIGHT))

# Initialize game object constants
GameObject.WIDTH = WIDTH
GameObject.HEIGHT = HEIGHT
GameObject.SCREEN_WIDTH = WIDTH


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


# Background
background = Background()

# UI elements
timer = Timer()
scorecard = ScoreCard()

# Game Elements
gameboard = Board(scorecard)
yochan = YoChan(gameboard)
tsuki = Tsuki()
trainer = Trainer()

menu = Menu()

clock = pygame.time.Clock()
delta_time = 0.1


async def main():
    global delta_time, clock, menu, trainer, tsuki, yochan, gameboard, \
            scorecard, timer, background, WIDTH, HEIGHT, ASPECT, screen, \
            render_surface

    running = True

    playing = False
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
                GameObject.SCREEN_WIDTH = width  # Set the universal tracker
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    playing = not playing
            if playing:
                yochan.handle_input(event)
            else:
                menu.handle_input(event)

        background.update(delta_time)
        background.draw(render_surface)

        if playing:
            # Logical updates here
            timer.update(delta_time)
            gameboard.update(delta_time)
            tsuki.update(delta_time, gameboard)  # She can see the board
            yochan.update(delta_time, gameboard)  # Her too
            trainer.update(delta_time, gameboard)

            # Draw graphics

            gameboard.draw(render_surface)
            tsuki.draw(render_surface)
            yochan.draw(render_surface)

            # Draw UI
            scorecard.draw(render_surface)
            timer.draw(render_surface)

        else:
            menu.update(delta_time)
            menu.draw(render_surface)

        # Scale and draw render_surface properly
        screen.fill((0, 0, 0))
        rect = get_scaled_rect(screen.get_size())
        scaled_surface = pygame.transform.scale(render_surface,
                                                (rect.width, rect.height))
        screen.blit(scaled_surface, rect.topleft)

        pygame.display.flip()
        delta_time = clock.tick(60) / 1000  # Milliseconds
        delta_time = max(0.001, min(0.1, delta_time))
        await asyncio.sleep(0)

    # pygame.quit()

asyncio.run(main())
