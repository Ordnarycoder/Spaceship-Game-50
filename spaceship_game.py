import pygame
import random

pygame.init()
pygame.font.init()

# Window setup
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Ship Game")

# Load spaceship image
SPACESHIP_IMG = pygame.image.load("spaceship.png")
SPACESHIP_IMG = pygame.transform.scale(SPACESHIP_IMG, (60, 60))  # Resize if needed

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Font for score
font = pygame.font.Font(None, 36)

# Classes
class SpaceShip:
    def __init__(self, x, y):
        self.image = SPACESHIP_IMG
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed = 7

    def move(self):
        self.rect.y -= self.speed

    def draw(self, window):
        pygame.draw.rect(window, WHITE, self.rect)

class Meteor:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 40)
        self.speed = random.randint(2, 5)

    def move(self):
        self.rect.y += self.speed

    def draw(self, window):
        pygame.draw.ellipse(window, RED, self.rect)

# Game setup
running = True
clock = pygame.time.Clock()
spaceship = SpaceShip(WIDTH // 2, HEIGHT - 70)
bullets = []
meteors = []
spawn_timer = 0
last_shot_time = 0
shot_cooldown = 200  # milliseconds
score = 0

# Game loop
while running:
    clock.tick(60)
    window.fill((0, 0, 0))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input            
    keys = pygame.key.get_pressed()
    spaceship.move(keys)
    current_time = pygame.time.get_ticks()

    if keys[pygame.K_SPACE]:
        if current_time - last_shot_time > shot_cooldown and len(bullets) < 3:
            bullet = Bullet(spaceship.rect.centerx, spaceship.rect.top)
            bullets.append(bullet)
            last_shot_time = current_time

    # Spawn meteors
    spawn_timer += 1
    if spawn_timer >= 40:
        meteors.append(Meteor())
        spawn_timer = 0

    # Update bullets
    for bullet in bullets[:]:
        bullet.move()
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    # Update meteors
    for meteor in meteors[:]:
        meteor.move()
        if meteor.rect.top > HEIGHT:
            meteors.remove(meteor)

    # Check collisions between meteors and bullets
    for meteor in meteors[:]:
        for bullet in bullets[:]:
            if meteor.rect.colliderect(bullet.rect):
                meteors.remove(meteor)
                bullets.remove(bullet)
                score += 1  # Increase score when a meteor is destroyed
                break

    # Check if meteor hits spaceship
    for meteor in meteors:
        if meteor.rect.colliderect(spaceship.rect):
            print("Game Over!")
            running = False

    # Draw spaceship, bullets, and meteors
    spaceship.draw(window)
    for bullet in bullets:
        bullet.draw(window)
    for meteor in meteors:
        meteor.draw(window)

    # Render and display score at top left corner
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
  