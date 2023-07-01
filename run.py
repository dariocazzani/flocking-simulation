import pygame
from boid import Boid


pygame.init()
width, height = 1000, 1000
screen_color = (0, 0, 0)
screen = pygame.display.set_mode((width, height))


def main():
    flock = [Boid() for _ in range(100)]
    boid = Boid()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Clear the screen (fill with black color)
        screen.fill(screen_color)
        
        for boid in flock:
            boid.edges()
            boid.flock(flock)
            boid.update()
            boid.show(screen)
        
        pygame.display.flip()
        pygame.time.delay(33)
    
    pygame.quit()
    pass

if __name__ == "__main__":
    main()