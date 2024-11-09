import pygame
import random
import time

# Inicialização do Pygame
pygame.init()

# Constantes da tela
W_WIDTH = 400
W_HEIGHT = 600
PIPE_WIDTH = 80
PIPE_GAP = 150
PIPE_SPACING = 250  # Distância entre as barreiras (antes era implicitamente 200)

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (255, 102, 102)
BUTTON_BORDER_COLOR = (200, 0, 0)
RED = (255, 0, 0)

# Velocidade inicial e incremento
BASE_SPEED = 2
SPEED_INCREMENT = 0.05
MAX_SPEED = 6
MIN_SCORE_FOR_SPEED = 10

class Bird:
    def __init__(self, x, y, images):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.images = images
        self.image = self.images["bird_up"]

    def jump(self):
        self.vel_y = -7

    def update(self):
        self.vel_y += 0.5
        self.y += self.vel_y
        if self.y < 0 or self.y > W_HEIGHT - self.image.get_height():
            return True
        return False

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

class Pipe:
    def __init__(self, x, height, images, speed):
        self.x = x
        self.height = height
        self.images = images
        self.speed = speed
        self.scored = False  # Flag para controlar se já foi pontuado

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        surface.blit(self.images["pipe_body"], (self.x, self.height - self.images["pipe_body"].get_height()))
        surface.blit(self.images["pipe_end"], (self.x, self.height + PIPE_GAP))

    def collide(self, bird_rect):
        upper_pipe_rect = pygame.Rect(self.x, self.height - self.images["pipe_body"].get_height(), PIPE_WIDTH, self.images["pipe_body"].get_height())
        lower_pipe_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, self.images["pipe_end"].get_height())
        return bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect)

def load_theme_images(theme):
    background_image = load_image(f'images/{theme}/background_{theme}.png')
    background_image = pygame.transform.scale(background_image, (W_WIDTH, W_HEIGHT))
    return {
        "background": background_image,
        "bird_up": load_image(f'images/{theme}/charlie_{theme}_1.png', (30, 30)),
        "bird_down": load_image(f'images/{theme}/charlie_{theme}_2.png', (30, 30)),
        "pipe_body": load_image(f'images/{theme}/barreira_corpo_{theme}.png'),
        "pipe_end": load_image(f'images/{theme}/barreira_fim_{theme}.png'),
    }

def load_image(file_name, size=None):
    img = pygame.image.load(file_name).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img

def countdown_screen(screen, background_image):
    font = pygame.font.Font(None, 100)
    for i in range(3, 0, -1):
        screen.blit(background_image, (0, 0))
        count_text = font.render(str(i), True, RED)
        text_rect = count_text.get_rect(center=(W_WIDTH//2, W_HEIGHT//2))
        screen.blit(count_text, text_rect)
        pygame.display.flip()
        time.sleep(1)

def theme_selection_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title = font.render("The Chosen", True, (128, 0, 0))
    screen.blit(title, (W_WIDTH // 2 - title.get_width() // 2, 50))

    button_font = pygame.font.Font(None, 50)
    buttons = [
        ("Castle", (W_WIDTH // 2, 200)),
        ("Florest", (W_WIDTH // 2, 300)),
        ("Twilight", (W_WIDTH // 2, 400))
    ]
    
    for text, pos in buttons:
        button = button_font.render(text, True, (0, 0, 0))
        rect = button.get_rect(center=pos)
        pygame.draw.rect(screen, BUTTON_COLOR, rect.inflate(20, 20))
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, rect.inflate(20, 20), 3)
        screen.blit(button, rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for text, pos in buttons:
                    button_rect = button.get_rect(center=pos)
                    if button_rect.collidepoint(event.pos):
                        return text

def game_over_screen(score):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title = font.render("Game Over", True, (128, 0, 0))
    screen.blit(title, (W_WIDTH // 2 - title.get_width() // 2, 50))

    score_font = pygame.font.Font(None, 48)
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(W_WIDTH // 2, 150))
    screen.blit(score_text, score_rect)

    button_font = pygame.font.Font(None, 50)
    restart_button = button_font.render("Reiniciar", True, (128, 0, 0))
    exit_button = button_font.render("Sair", True, (128, 0, 0))
    
    restart_rect = restart_button.get_rect(center=(W_WIDTH // 2, 250))
    exit_rect = exit_button.get_rect(center=(W_WIDTH // 2, 350))
    
    pygame.draw.rect(screen, BUTTON_COLOR, restart_rect.inflate(20, 20))
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, restart_rect.inflate(20, 20), 3)
    screen.blit(restart_button, restart_rect)

    pygame.draw.rect(screen, BUTTON_COLOR, exit_rect.inflate(20, 20))
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, exit_rect.inflate(20, 20), 3)
    screen.blit(exit_button, exit_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_rect.collidepoint(event.pos):
                    return True
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

def main():
    global screen
    screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
    pygame.display.set_caption("The Chosen")

    while True:
        theme = theme_selection_screen()
        images = load_theme_images(theme)
        
        countdown_screen(screen, images["background"])
        
        bird = Bird(50, W_HEIGHT // 2, images)
        pipes = []
        score = 0
        current_speed = BASE_SPEED

        # Criar as primeiras barreiras
        for i in range(3):  # Começa com 3 barreiras
            height = random.randint(150, 350)  # Ajustado para ter mais espaço vertical
            pipes.append(Pipe(W_WIDTH + (i * PIPE_SPACING), height, images, BASE_SPEED))

        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()

            if bird.update():
                running = False
                continue

            if score >= MIN_SCORE_FOR_SPEED:
                speed_increase = ((score - MIN_SCORE_FOR_SPEED) * SPEED_INCREMENT)
                current_speed = min(BASE_SPEED + speed_increase, MAX_SPEED)
            else:
                current_speed = BASE_SPEED

            # Atualizar as barreiras
            for pipe in pipes:
                pipe.speed = current_speed  # Atualiza a velocidade da barreira
                pipe.update()
                
                # Verifica se o pássaro passou pela barreira
                if not pipe.scored and pipe.x + PIPE_WIDTH < bird.x:
                    score += 1
                    pipe.scored = True

            # Remove barreiras que saíram da tela
            pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

            # Adiciona novas barreiras quando necessário
            if len(pipes) < 3:  # Mantém sempre 3 barreiras na tela
                last_pipe = max(pipes, key=lambda p: p.x)
                height = random.randint(150, 350)
                pipes.append(Pipe(last_pipe.x + PIPE_SPACING, height, images, current_speed))

            bird_rect = pygame.Rect(bird.x, bird.y, images["bird_up"].get_width(), images["bird_up"].get_height())
            for pipe in pipes:
                if pipe.collide(bird_rect):
                    running = False

            screen.blit(images["background"], (0, 0))
            for pipe in pipes:
                pipe.draw(screen)

            bird.draw(screen)

            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(W_WIDTH // 2, 30))
            screen.blit(score_text, score_rect)

            pygame.display.flip()
            clock.tick(60)

        if not game_over_screen(score):
            break

if __name__ == "__main__":
    main()
