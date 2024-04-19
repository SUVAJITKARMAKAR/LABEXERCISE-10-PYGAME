import pygame
import sys
import random

pygame.init()

# Set up the screen
screen_width = 1500
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rocket Bomb Example")

# Load background image
background_img = pygame.image.load('images/background.png')
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load images and resize
rocket_img = pygame.image.load('images/shuttle.png')
rocket_img = pygame.transform.scale(rocket_img, (100, 100))
bomb_img = pygame.image.load('images/nuclear-bomb.png')
bomb_img = pygame.transform.scale(bomb_img, (40, 40))
house_img = pygame.image.load('images/mansion.png')
house_img = pygame.transform.scale(house_img, (150,150))
explosion_img = pygame.image.load('images/blasting.png')
explosion_img = pygame.transform.scale(explosion_img, (100, 100))

# Objects attributes
rocket_rect = rocket_img.get_rect()
rocket_rect.centerx = screen_width // 2
rocket_rect.top = 0  

house_rect = house_img.get_rect()
house_rect.centerx = screen_width // 2
house_rect.bottom = screen_height  

# Define movement speed
rocket_speed = 10  # Increased rocket speed
bomb_speed = 1
gravity = 0.5

# Game variables
score = 0
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

# List to store bomb rectangles
bombs = []

# List to store explosion animations
explosions = []

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a new bomb rectangle and add it to the list
                bomb_rect = bomb_img.get_rect()
                bomb_rect.centerx = rocket_rect.centerx
                bomb_rect.top = rocket_rect.bottom
                bombs.append(bomb_rect)

    # Move the rocket
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rocket_rect.x -= rocket_speed
    if keys[pygame.K_RIGHT]:
        rocket_rect.x += rocket_speed

    # Ensure rocket stays within the screen boundaries
    rocket_rect.x = max(0, min(rocket_rect.x, screen_width - rocket_rect.width))

    # Move and draw each bomb
    for bomb_rect in bombs[:]:  # Iterate over a copy to avoid modifying the list while iterating
        bomb_rect.y += bomb_speed
        bomb_speed += gravity

        # Check collision with the house
        if bomb_rect.colliderect(house_rect):
            # Create explosion animation
            explosion_rect = explosion_img.get_rect()
            explosion_rect.center = bomb_rect.center
            explosions.append((explosion_rect, pygame.time.get_ticks()))  # Add explosion and current time

            # Remove the bomb from the list
            bombs.remove(bomb_rect)
            score += 1

            # Reset house position with delay
            house_rect.centerx = random.randint(0, screen_width - house_rect.width)
            house_rect.bottom = screen_height
            pygame.time.delay(100)  # Delay before spawning the house again
        elif bomb_rect.y > screen_height:  # If bomb misses the house
            game_over_text = game_over_font.render("Game Over", True, RED)
            score_text = font.render("Score: " + str(score), True, RED)
            screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 50))
            screen.blit(score_text, (screen_width // 2 - 50, screen_height // 2 + 50))
            pygame.display.flip()
            pygame.time.delay(2000)  # Delay for 2 seconds before exiting
            pygame.quit()
            sys.exit()

    # Draw background
    screen.blit(background_img, (0, 0))

    # Draw everything onto the screen
    screen.blit(rocket_img, rocket_rect)
    screen.blit(house_img, house_rect)  # Draw the house

    for bomb_rect in bombs:
        screen.blit(bomb_img, bomb_rect)

    # Draw and manage explosion animations
    for explosion, start_time in explosions[:]:
        current_time = pygame.time.get_ticks()
        if current_time - start_time < 200:  # Display explosion for 200 milliseconds
            screen.blit(explosion_img, explosion)
        else:
            explosions.remove((explosion, start_time))  # Remove explosion after 200 milliseconds

    # Display score
    score_text = font.render("Score: " + str(score), True, RED)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
