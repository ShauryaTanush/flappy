import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.5
FLAP_STRENGTH = -8
PIPE_WIDTH = 80
PIPE_GAP = 150
PIPE_DISTANCE = 300
BIRD_SIZE = 30

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Bird Settings
bird = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, BIRD_SIZE, BIRD_SIZE)
bird_y_momentum = 0

# Pipe Settings
pipes = []
pipe_timer = 0
score = 0
font = pygame.font.Font(None, 36)

# Game Loop Control
clock = pygame.time.Clock()
running = True

def create_pipe():
    height = random.randint(100, SCREEN_HEIGHT - 200)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - height - PIPE_GAP)
    return top_pipe, bottom_pipe

while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_y_momentum = FLAP_STRENGTH

    # Bird Gravity
    bird_y_momentum += GRAVITY
    bird.y += int(bird_y_momentum)

    # Generate Pipes
    pipe_timer += 1
    if pipe_timer >= PIPE_DISTANCE:
        pipes.extend(create_pipe())
        pipe_timer = 0

    # Move Pipes
    for pipe in pipes:
        pipe.x -= 3
    pipes = [pipe for pipe in pipes if pipe.right > 0]

    # Check for Collisions
    for pipe in pipes:
        if bird.colliderect(pipe):
            running = False
    if bird.y < 0 or bird.y > SCREEN_HEIGHT - BIRD_SIZE:
        running = False

    # Score Update
    for pipe in pipes:
        if pipe.right < bird.left and not hasattr(pipe, 'scored'):
            score += 0.5
            pipe.scored = True

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, bird)
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

    # Display Score
    score_text = font.render(f"Score: {int(score)}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update Display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
