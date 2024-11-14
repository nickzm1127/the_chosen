# Importa as bibliotecas necessárias
import pygame  # Biblioteca principal para criar jogos
import random  # Biblioteca para gerar números aleatórios
import time    # Biblioteca para controlar o tempo

# Inicializa todos os módulos do Pygame
pygame.init()

# Define as constantes do tamanho da janela do jogo
W_WIDTH = 400      # Largura da janela
W_HEIGHT = 600     # Altura da janela
PIPE_WIDTH = 80    # Largura dos canos/barreiras
PIPE_GAP = 150     # Espaço entre os canos superior e inferior
PIPE_SPACING = 250 # Distância horizontal entre os pares de canos

# Define as cores utilizadas no jogo usando tuplas RGB
WHITE = (255, 255, 255)               # Cor branca
BLACK = (0, 0, 0)                     # Cor preta
BUTTON_COLOR = (255, 102, 102)        # Cor rosa para botões
BUTTON_BORDER_COLOR = (200, 0, 0)     # Cor vermelha escura para borda dos botões
RED = (255, 0, 0)                     # Cor vermelha

# Define as constantes de velocidade do jogo
BASE_SPEED = 2         # Velocidade inicial do jogo
SPEED_INCREMENT = 0.05 # Quanto a velocidade aumenta por ponto
MAX_SPEED = 6         # Velocidade máxima permitida
MIN_SCORE_FOR_SPEED = 10  # Pontuação mínima para começar a aumentar a velocidade

# Classe que define o pássaro/personagem principal
class Bird:
    def __init__(self, x, y, images):
        self.x = x                      # Posição X inicial do pássaro
        self.y = y                      # Posição Y inicial do pássaro
        self.vel_y = 0                  # Velocidade vertical inicial
        self.images = images            # Dicionário com as imagens do pássaro
        self.image = self.images["bird_up"]  # Imagem atual do pássaro

    def jump(self):
        self.vel_y = -7  # Define a velocidade vertical para cima quando pula

    def update(self):
        self.vel_y += 0.5              # Aplica gravidade
        self.y += self.vel_y           # Atualiza posição vertical
        # Verifica se o pássaro saiu da tela
        if self.y < 0 or self.y > W_HEIGHT - self.image.get_height():
            return True
        return False

    def draw(self, surface):
        # Desenha o pássaro na tela
        surface.blit(self.image, (self.x, self.y))

# Classe que define os canos/obstáculos
class Pipe:
    def __init__(self, x, height, images, speed):
        self.x = x                  # Posição X inicial do cano
        self.height = height        # Altura do cano
        self.images = images        # Dicionário com as imagens dos canos
        self.speed = speed          # Velocidade de movimento do cano
        self.scored = False         # Controle se o jogador já pontuou neste cano

    def update(self):
        self.x -= self.speed  # Move o cano para a esquerda

    def draw(self, surface):
        # Desenha os canos superior e inferior
        surface.blit(self.images["pipe_body"], (self.x, self.height - self.images["pipe_body"].get_height()))
        surface.blit(self.images["pipe_end"], (self.x, self.height + PIPE_GAP))

    def collide(self, bird_rect):
        # Cria retângulos de colisão para os canos
        upper_pipe_rect = pygame.Rect(self.x, self.height - self.images["pipe_body"].get_height(), 
                                    PIPE_WIDTH, self.images["pipe_body"].get_height())
        lower_pipe_rect = pygame.Rect(self.x, self.height + PIPE_GAP, 
                                    PIPE_WIDTH, self.images["pipe_end"].get_height())
        # Verifica colisão com o pássaro
        return bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect)

# Função para carregar imagens do tema selecionado
def load_theme_images(theme):
    # Carrega e redimensiona a imagem de fundo
    background_image = load_image(f'images/{theme}/background_{theme}.png')
    background_image = pygame.transform.scale(background_image, (W_WIDTH, W_HEIGHT))
    # Retorna dicionário com todas as imagens do tema
    return {
        "background": background_image,
        "bird_up": load_image(f'images/{theme}/charlie_{theme}_1.png', (30, 30)),
        "bird_down": load_image(f'images/{theme}/charlie_{theme}_2.png', (30, 30)),
        "pipe_body": load_image(f'images/{theme}/barreira_corpo_{theme}.png'),
        "pipe_end": load_image(f'images/{theme}/barreira_fim_{theme}.png'),
    }

# Função auxiliar para carregar e redimensionar imagens
def load_image(file_name, size=None):
    img = pygame.image.load(file_name).convert_alpha()  # Carrega a imagem com transparência
    if size:
        img = pygame.transform.scale(img, size)         # Redimensiona se necessário
    return img

# Função que mostra a contagem regressiva antes do jogo começar
def countdown_screen(screen, background_image):
    font = pygame.font.Font(None, 100)
    for i in range(3, 0, -1):              # Conta de 3 até 1
        screen.blit(background_image, (0, 0))  # Desenha o fundo
        count_text = font.render(str(i), True, RED)  # Renderiza o número
        text_rect = count_text.get_rect(center=(W_WIDTH//2, W_HEIGHT//2))  # Centraliza o texto
        screen.blit(count_text, text_rect)  # Desenha o número
        pygame.display.flip()               # Atualiza a tela
        time.sleep(1)                      # Espera 1 segundo

# Função que mostra a tela de seleção de tema
def theme_selection_screen():
    screen.fill(BLACK)  # Preenche a tela com preto
    # Configura e desenha o título
    font = pygame.font.Font(None, 74)
    title = font.render("The Chosen", True, (128, 0, 0))
    screen.blit(title, (W_WIDTH // 2 - title.get_width() // 2, 50))

    # Configura e desenha os botões de tema
    button_font = pygame.font.Font(None, 50)
    buttons = [
        ("Castle", (W_WIDTH // 2, 200)),
        ("Florest", (W_WIDTH // 2, 300)),
        ("Twilight", (W_WIDTH // 2, 400))
    ]
    
    # Desenha cada botão de tema
    for text, pos in buttons:
        button = button_font.render(text, True, (0, 0, 0))
        rect = button.get_rect(center=pos)
        pygame.draw.rect(screen, BUTTON_COLOR, rect.inflate(20, 20))
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, rect.inflate(20, 20), 3)
        screen.blit(button, rect)

    pygame.display.flip()  # Atualiza a tela

    # Loop para detectar clique no botão de tema
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

# Função que mostra a tela de game over
def game_over_screen(score):
    screen.fill(BLACK)  # Preenche a tela com preto
    
    # Configura e desenha o título "Game Over"
    font = pygame.font.Font(None, 74)
    title = font.render("Game Over", True, (128, 0, 0))
    screen.blit(title, (W_WIDTH // 2 - title.get_width() // 2, 50))

    # Configura e desenha a pontuação
    score_font = pygame.font.Font(None, 48)
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(W_WIDTH // 2, 150))
    screen.blit(score_text, score_rect)

    # Configura e desenha os botões de reiniciar e sair
    button_font = pygame.font.Font(None, 50)
    restart_button = button_font.render("Reiniciar", True, (128, 0, 0))
    exit_button = button_font.render("Sair", True, (128, 0, 0))
    
    restart_rect = restart_button.get_rect(center=(W_WIDTH // 2, 250))
    exit_rect = exit_button.get_rect(center=(W_WIDTH // 2, 350))
    
    # Desenha os botões com suas bordas
    pygame.draw.rect(screen, BUTTON_COLOR, restart_rect.inflate(20, 20))
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, restart_rect.inflate(20, 20), 3)
    screen.blit(restart_button, restart_rect)

    pygame.draw.rect(screen, BUTTON_COLOR, exit_rect.inflate(20, 20))
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, exit_rect.inflate(20, 20), 3)
    screen.blit(exit_button, exit_rect)

    pygame.display.flip()  # Atualiza a tela

    # Loop para detectar clique nos botões
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

# Função principal do jogo
def main():
    global screen
    # Inicializa a janela do jogo
    screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
    pygame.display.set_caption("The Chosen")

    # Loop principal do jogo
    while True:
        theme = theme_selection_screen()      # Seleciona o tema
        images = load_theme_images(theme)     # Carrega as imagens do tema
        
        countdown_screen(screen, images["background"])  # Mostra contagem regressiva
        
        # Inicializa o pássaro e as variáveis do jogo
        bird = Bird(50, W_HEIGHT // 2, images)
        pipes = []
        score = 0
        current_speed = BASE_SPEED

        # Cria as primeiras barreiras
        for i in range(3):
            height = random.randint(150, 350)
            pipes.append(Pipe(W_WIDTH + (i * PIPE_SPACING), height, images, BASE_SPEED))

        clock = pygame.time.Clock()
        running = True

        # Loop do jogo em si
        while running:
            # Processa eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()

            # Atualiza o pássaro e verifica colisão com bordas
            if bird.update():
                running = False
                continue

            # Aumenta a velocidade baseado na pontuação
            if score >= MIN_SCORE_FOR_SPEED:
                speed_increase = ((score - MIN_SCORE_FOR_SPEED) * SPEED_INCREMENT)
                current_speed = min(BASE_SPEED + speed_increase, MAX_SPEED)
            else:
                current_speed = BASE_SPEED

            # Atualiza cada cano
            for pipe in pipes:
                pipe.speed = current_speed
                pipe.update()
                
                # Aumenta a pontuação quando passa por um cano
                if not pipe.scored and pipe.x + PIPE_WIDTH < bird.x:
                    score += 1
                    pipe.scored = True

            # Remove canos que saíram da tela
            pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

            # Adiciona novos canos quando necessário
            if len(pipes) < 3:
                last_pipe = max(pipes, key=lambda p: p.x)
                height = random.randint(150, 350)
                pipes.append(Pipe(last_pipe.x + PIPE_SPACING, height, current_speed))

            # Verifica colisões com os canos
            bird_rect = pygame.Rect(bird.x, bird.y, 
                                  images["bird_up"].get_width(), 
                                  images["bird_up"].get_height())
            for pipe in pipes:
                if pipe.collide(bird_rect):
                    running = False

            # Desenha todos os elementos na tela
            screen.blit(images["background"], (0, 0))
            for pipe in pipes:
                pipe.draw(screen)

            bird.draw(screen)

            # Desenha a pontuação
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"{score}", True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(W_WIDTH // 2, 30))
            screen.blit(score_text, score_rect)

            pygame.display.flip()  # Atualiza a tela
            clock.tick(60)        # Limita o fps a 60

        # Mostra tela de game over quando o jogo termina
        if not game_over_screen(score):
            break

# Inicia o jogo se este arquivo for executado diretamente
if __name__ == "__main__":
    main()
