import pygame

pygame.init()

screen = pygame.display.set_mode((640, 640))

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Logical updates here

    # graphics here
    screen.fill("purple")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
