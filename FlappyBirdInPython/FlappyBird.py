import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set screen resolution
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load images and scale them appropriately
background = pygame.image.load('background_with_ground.png').convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird_img = pygame.image.load('bird.png').convert_alpha()
bird_img = pygame.transform.scale(bird_img, (80, 80))

pipe_img = pygame.image.load('pipe.png').convert_alpha()
pipe_img = pygame.transform.scale(pipe_img, (100, 600))

# Game variables
bird_rect = bird_img.get_rect(center=(200, SCREEN_HEIGHT // 2))
bird_movement = 0
GRAVITY = 0.25
BIRD_JUMP = -6.5
PIPE_SPEED = -5  # Will vary based on difficulty
pipes = []
game_active = False  # Game starts in an inactive state
game_over = False
start_screen = True
score = 0
high_score = 0
difficulty = 'easy'  # Default difficulty
PIPE_GAP = 300  # Default gap for easy mode

# Font for text display
font = pygame.font.Font(None, 64)

# Function to create pipes
def create_pipe():
    random_height = random.randint(250, 600)
    pipe_top = pipe_img.get_rect(midbottom=(SCREEN_WIDTH, random_height - PIPE_GAP // 2))
    pipe_bottom = pipe_img.get_rect(midtop=(SCREEN_WIDTH, random_height + PIPE_GAP // 2))
    return pipe_top, pipe_bottom

# Function to move pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx += PIPE_SPEED
    return pipes

# Function to draw pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            screen.blit(pipe_img, pipe)
        else:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)

# Function to check for collisions with a smaller hitbox
def check_collision(pipes):
    # Create a smaller bird rectangle for collision detection (making it easier)
    smaller_bird_rect = bird_rect.inflate(-20, -20)  # Shrinks the hitbox

    # Check pipe collisions
    for pipe in pipes:
        if smaller_bird_rect.colliderect(pipe):
            return False

    # Check if bird hits the top or bottom of the screen
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return False

    return True

# Function to display the start screen
def display_start_screen():
    start_text = font.render("Press 1 for Easy Mode, 2 for Hard Mode", True, (255, 255, 255))
    difficulty_text = font.render(f"Difficulty: {difficulty.capitalize()}", True, (255, 255, 255))
    screen.blit(start_text, (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2))
    pygame.display.update()

# Function to display game over message
def display_game_over():
    global high_score
    game_over_text = font.render("Game Over!", True, (255, 0, 0))
    restart_text = font.render("Press SPACE to Restart", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    screen.blit(game_over_text, (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 3))
    screen.blit(restart_text, (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 3 + 100))
    screen.blit(score_text, (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 3 + 200))
    screen.blit(high_score_text, (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 3 + 300))
    pygame.display.update()

# Function to update score
def update_score(pipes):
    global score
    for pipe in pipes:
        if pipe.centerx == bird_rect.centerx:
            score += 1
    return score

# Main game loop
pipe_spawn = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn, 1200)

while True:
    screen.blit(background, (0, 0))

    # Start screen state
    if start_screen:
        display_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Select difficulty
                if event.key == pygame.K_1:
                    difficulty = 'easy'
                    PIPE_SPEED = -5  # Normal speed
                    PIPE_GAP = 300  # Normal gap
                    start_screen = False
                    game_active = True
                elif event.key == pygame.K_2:
                    difficulty = 'hard'
                    PIPE_SPEED = -7  # Faster pipes
                    PIPE_GAP = 250  # Smaller gap between pipes (harder)
                    start_screen = False
                    game_active = True
                bird_rect.center = (200, SCREEN_HEIGHT // 2)
                bird_movement = 0
                pipes.clear()
                score = 0

    # Game active state
    elif game_active:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_movement = BIRD_JUMP

            if event.type == pipe_spawn:
                pipes.extend(create_pipe())

        # Bird movement
        bird_movement += GRAVITY
        bird_rect.centery += bird_movement
        screen.blit(bird_img, bird_rect)

        # Move and draw pipes
        pipes = move_pipes(pipes)
        draw_pipes(pipes)

        # Check for collisions
        if not check_collision(pipes):
            game_active = False
            game_over = True
            high_score = max(score, high_score)

        # Update and display the score
        score = update_score(pipes)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, 50))

    # Game over state
    elif game_over:
        display_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Restart the game
                game_active = True
                game_over = False
                bird_rect.center = (200, SCREEN_HEIGHT // 2)
                bird_movement = 0
                pipes.clear()
                score = 0

    # Update display
    pygame.display.update()
    clock.tick(60)
