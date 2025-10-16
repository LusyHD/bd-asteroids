import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import score


# ----- LIST OF POTENTIAL IMPROVEMENTS -----
# Add a scoring system ✅
# Implement multiple lives and respawning 
# Add an explosion effect for the asteroids
# Add acceleration to the player movement
# Make the objects wrap around the screen instead of disappearing
# Add a background image
# Create different weapon types
# Make the asteroids lumpy instead of perfectly round
# Make the ship have a triangular hit box instead of a circular one
# Add a shield power-up
# Add a speed power-up
# Add bombs that can be dropped
# ------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting Asteroids!")
    print("Screen width:", SCREEN_WIDTH)
    print("Screen height:", SCREEN_HEIGHT)

    clock = pygame.time.Clock()
    dt = 0
    font = pygame.font.SysFont(None, 24)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)


    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    Asteroid_Field = AsteroidField()

    score.load()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        updatable.update(dt)

        if not player.alive and player.lives <= 0:
            print("Game over!")
            if score.get_prev_high() is not None:
                if score.get() > score.get_prev_high():
                    print("NEW HIGH SCORE!")
                    print(f"Your Score: {score.get()}")
                    print(f"Previous High Score: {score.get_prev_high()}")
            else:
                print(f"Your Score: {score.get()}")
                print(f"High Score: {score.get_high()}")
            score.reset()
            sys.exit()

        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)

        text_surface = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        if player.alive and not player.invulnerability:
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    player.player_death()
                    break  # avoid multiple hits this frame
                for shot in shots:
                    if asteroid.collides_with(shot):
                        shot.kill()
                        asteroid.split()
                        score.add()

        pygame.display.flip()

        dt = clock.tick(60) / 1000 #60 FPS


if __name__ == "__main__":
    main()
