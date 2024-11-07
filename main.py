import pygame  # Importa a biblioteca Pygame para desenvolvimento de jogos
import random  # Importa a biblioteca random para gerar números aleatórios

# Inicialização do Pygame
pygame.init()  # Inicializa todos os módulos do Pygame

# Constantes da tela
W_WIDTH = 400  # Largura da tela do jogo
W_HEIGHT = 600  # Altura da tela do jogo
PIPE_WIDTH = 80  # Largura das barreiras (tubos)
PIPE_GAP = 150  # Espaço entre as barreiras

# Cores
WHITE = (255, 255, 255)  # Cor branca
BLACK = (0, 0, 0)  # Cor preta
BUTTON_COLOR = (255, 102, 102)  # Cor dos botões
BUTTON_BORDER_COLOR = (200, 0, 0)  # Cor da borda dos botões

# Classe do pássaro
class Bird:
    def __init__(self, x, y, images):
        self.x = x  # Posição horizontal do pássaro
        self.y = y  # Posição vertical do pássaro
        self.vel_y = 0  # Velocidade vertical do pássaro
        self.images = images  # Imagens do pássaro
        self.image = self.images["bird_up"]  # Imagem inicial do pássaro

    def jump(self):
        self.vel_y = -7  # Aumenta a velocidade para cima quando o pássaro pula

    def update(self):
        self.vel_y += 0.5  # Acelera o pássaro para baixo devido à gravidade
        self.y += self.vel_y  # Atualiza a posição vertical do pássaro
        if self.y < 0:  # Se o pássaro ultrapassar o topo da tela
            self.y = 0  # Reseta a posição para 0
        elif self.y > W_HEIGHT - self.image.get_height():  # Se ultrapassar o fundo da tela
            self.y = W_HEIGHT - self.image.get_height()  # Reseta para a altura da tela

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))  # Desenha o pássaro na tela

# Classe das barreiras
class Pipe:
    def __init__(self, x, height, images):
        self.x = x  # Posição horizontal da barreira
        self.height = height  # Altura da barreira
        self.images = images  # Imagens da barreira

    def update(self):
        self.x -= 2  # Move a barreira para a esquerda

    def draw(self, surface):
        # Desenha a parte superior e inferior da barreira
        surface.blit(self.images["pipe_body"], (self.x, self.height - self.images["pipe_body"].get_height()))
        surface.blit(self.images["pipe_end"], (self.x, self.height + PIPE_GAP))

    def collide(self, bird_rect):
        # Verifica colisão com as barreiras
        upper_pipe_rect = pygame.Rect(self.x, self.height - self.images["pipe_body"].get_height(), PIPE_WIDTH, self.images["pipe_body"].get_height())
        lower_pipe_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, self.images["pipe_end"].get_height())
        return bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect)

# Função para carregar as imagens do tema
def load_theme_images(theme):
    background_image = load_image(f'images/{theme}/background_{theme}.png')  # Carrega a imagem de fundo
    background_image = pygame.transform.scale(background_image, (W_WIDTH, W_HEIGHT))  # Redimensiona o fundo para caber na tela
    return {
        "background": background_image,
        "bird_up": load_image(f'images/{theme}/charlie_{theme}_1.png', (30, 30)),  # Carrega a imagem do pássaro (em cima)
        "bird_down": load_image(f'images/{theme}/charlie_{theme}_2.png', (30, 30)),  # Carrega a imagem do pássaro (em baixo)
        "pipe_body": load_image(f'images/{theme}/barreira_corpo_{theme}.png'),  # Carrega a imagem da parte superior da barreira
        "pipe_end": load_image(f'images/{theme}/barreira_fim_{theme}.png'),  # Carrega a imagem da parte inferior da barreira
    }

# Função para carregar uma imagem
def load_image(file_name, size=None):
    img = pygame.image.load(file_name).convert_alpha()  # Carrega a imagem e converte para formato apropriado
    if size:
        img = pygame.transform.scale(img, size)  # Redimensiona a imagem se um tamanho for especificado
    return img

# Tela de seleção de tema
def theme_selection_screen():
    screen.fill(BLACK)  # Preenche a tela com a cor branca
    font = pygame.font.Font(None, 74)  # Cria uma fonte para o título
    title = font.render("The Chosen", True, (128, 0, 0))  # Renderiza o título em preto
    screen.blit(title, (W_WIDTH // 2 - title.get_width() // 2, 50))  # Desenha o título na tela

    button_font = pygame.font.Font(None, 50)  # Cria uma fonte para os botões
    buttons = [
        ("Castle", (W_WIDTH // 2, 200)),  # Botão para o tema Castle
        ("Florest", (W_WIDTH // 2, 300)),  # Botão para o tema Florest
        ("Twilight", (W_WIDTH // 2, 400))  # Botão para o tema Twilight
    ]
    
    for text, pos in buttons:
        button = button_font.render(text, True, (0, 0, 0))  # Renderiza o texto do botão
        rect = button.get_rect(center=pos)  # Cria um retângulo para o botão
        # Desenha o botão
        pygame.draw.rect(screen, BUTTON_COLOR, rect.inflate(20, 20))  # Botão com cor
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, rect.inflate(20, 20), 3)  # Borda do botão
        screen.blit(button, rect)  # Desenha o texto do botão

    pygame.display.flip()  # Atualiza a tela

    while True:
        for event in pygame.event.get():  # Loop para capturar eventos
            if event.type == pygame.QUIT:  # Se o usuário fechar a janela
                pygame.quit()
                quit()  # Encerra o jogo
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Se o botão do mouse for pressionado
                for text, pos in buttons:  # Verifica cada botão
                    button_rect = button.get_rect(center=pos)  # Cria um retângulo para o botão
                    if button_rect.collidepoint(event.pos):  # Se o mouse estiver sobre o botão
                        return text  # Retorna o nome do tema selecionado

# Tela de game over
def game_over_screen():
    screen.fill(BLACK)  # Preenche a tela com a cor preta
    font = pygame.font.Font(None, 74)  # Cria uma fonte para o título
    title = font.render("Game Over", True, (128, 0, 0))  # Renderiza o título em maroon
    screen.blit(title, (W_WIDTH // 2 - title.get_width() // 2, 50))  # Desenha o título na tela

    button_font = pygame.font.Font(None, 50)  # Cria uma fonte para os botões
    restart_button = button_font.render("Reiniciar", True, (128, 0, 0))  # Renderiza o botão de reiniciar
    exit_button = button_font.render("Sair", True, (128, 0, 0))  # Renderiza o botão de sair
    
    # Cria os retângulos para os botões
    restart_rect = restart_button.get_rect(center=(W_WIDTH // 2, 200))  
    exit_rect = exit_button.get_rect(center=(W_WIDTH // 2, 300))
    
    # Desenha os botões
    pygame.draw.rect(screen, BUTTON_COLOR, restart_rect.inflate(20, 20))  # Desenha o botão de reiniciar
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, restart_rect.inflate(20, 20), 3)  # Borda do botão de reiniciar
    screen.blit(restart_button, restart_rect)  # Desenha o texto do botão de reiniciar

    pygame.draw.rect(screen, BUTTON_COLOR, exit_rect.inflate(20, 20))  # Desenha o botão de sair
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, exit_rect.inflate(20, 20), 3)  # Borda do botão de sair
    screen.blit(exit_button, exit_rect)  # Desenha o texto do botão de sair

    pygame.display.flip()  # Atualiza a tela

    while True:
        for event in pygame.event.get():  # Loop para capturar eventos
            if event.type == pygame.QUIT:  # Se o usuário fechar a janela
                pygame.quit()
                quit()  # Encerra o jogo
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Se o botão do mouse for pressionado
                if restart_rect.collidepoint(event.pos):  # Se o mouse estiver sobre o botão de reiniciar
                    return True  # Retorna True para reiniciar o jogo
                elif exit_rect.collidepoint(event.pos):  # Se o mouse estiver sobre o botão de sair
                    pygame.quit()  # Encerra o Pygame
                    quit()  # Encerra o jogo

# Função principal do jogo
def main():
    global screen  # Declara a variável screen como global
    screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))  # Cria a tela do jogo
    pygame.display.set_caption("The Chosen")  # Define o título da janela

    theme = theme_selection_screen()  # Chama a tela de seleção de tema
    images = load_theme_images(theme)  # Carrega as imagens do tema selecionado
    bird = Bird(50, W_HEIGHT // 2, images)  # Cria uma instância do pássaro
    pipes = []  # Inicializa uma lista de barreiras
    score = 0  # Inicializa o score do jogador

    clock = pygame.time.Clock()  # Cria um relógio para controlar a taxa de quadros
    running = True  # Define a variável de controle do jogo

    while running:
        for event in pygame.event.get():  # Loop para capturar eventos
            if event.type == pygame.QUIT:  # Se o usuário fechar a janela
                pygame.quit()
                quit()  # Encerra o jogo
            if event.type == pygame.KEYDOWN:  # Se uma tecla for pressionada
                if event.key == pygame.K_SPACE:  # Se a tecla for a barra de espaço
                    bird.jump()  # Faz o pássaro pular

        bird.update()  # Atualiza a posição do pássaro

        if len(pipes) == 0 or pipes[-1].x < W_WIDTH - 200:  # Se não houver barreiras ou a última barreira estiver longe
            height = random.randint(100, 400)  # Gera uma altura aleatória para a nova barreira
            pipes.append(Pipe(W_WIDTH, height, images))  # Adiciona a nova barreira à lista

        for pipe in pipes:  # Atualiza a posição de todas as barreiras
            pipe.update()
            if pipe.x < 0:  # Se a barreira sair da tela
                pipes.remove(pipe)  # Remove a barreira da lista
                score += 1  # Aumenta o score

        # Verifica colisões
        bird_rect = pygame.Rect(bird.x, bird.y, images["bird_up"].get_width(), images["bird_up"].get_height())  # Cria um retângulo para o pássaro
        for pipe in pipes:  # Checa cada barreira
            if pipe.collide(bird_rect):  # Se houver colisão
                running = False  # Encerra o loop do jogo

        screen.blit(images["background"], (0, 0))  # Desenha o fundo na tela
        for pipe in pipes:  # Desenha todas as barreiras
            pipe.draw(screen)

        bird.draw(screen)  # Desenha o pássaro na tela

        font = pygame.font.Font(None, 36)  # Cria uma fonte para o score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))  # Renderiza o texto do score
        screen.blit(score_text, (10, 10))  # Desenha o score na tela

        pygame.display.flip()  # Atualiza a tela
        clock.tick(60)  # Limita a taxa de quadros a 60 FPS

    game_over_screen()  # Chama a tela de game over

# Executa a função principal
if __name__ == "__main__":
    main()  # Inicia o jogo