import pygame  # Importa a biblioteca Pygame para criação do jogo
import random  # Importa a biblioteca random para gerar números aleatórios
import time  # Importa a biblioteca time para funções de tempo

# Inicialização do Pygame
pygame.init()  # Inicia todos os módulos do Pygame

# Constantes da tela
W_WIDTH = 400  # Largura da janela
W_HEIGHT = 600  # Altura da janela
PIPE_WIDTH = 80  # Largura do cano
PIPE_GAP = 150  # Distância entre o cano superior e o inferior
PIPE_SPACING = 250  # Distância entre as barreiras (ajustada para maior espaçamento)

# Cores
WHITE = (255, 255, 255)  # Cor branca em RGB
BLACK = (0, 0, 0)  # Cor preta em RGB
BUTTON_COLOR = (255, 102, 102)  # Cor do botão em RGB
BUTTON_BORDER_COLOR = (200, 0, 0)  # Cor da borda do botão em RGB
RED = (255, 0, 0)  # Cor vermelha em RGB

# Velocidade inicial e incremento
BASE_SPEED = 2  # Velocidade inicial do movimento dos canos
SPEED_INCREMENT = 0.05  # Incremento de velocidade conforme a pontuação aumenta
MAX_SPEED = 6  # Velocidade máxima permitida
MIN_SCORE_FOR_SPEED = 10  # Pontuação mínima para que a velocidade comece a aumentar

class Bird:
    def __init__(self, x, y, images):
        """ Inicializa o pássaro com sua posição inicial e imagens correspondentes ao tema """
        self.x = x  # Posição horizontal do pássaro
        self.y = y  # Posição vertical do pássaro
        self.vel_y = 0  # Velocidade vertical do pássaro (gravidade)
        self.images = images  # Dicionário de imagens do pássaro
        self.image = self.images["bird_up"]  # Define a imagem inicial do pássaro

    def jump(self):
        """ Faz o pássaro "pular" alterando sua velocidade vertical """
        self.vel_y = -7  # Muda a velocidade para negativa (subir)

    def update(self):
        """ Atualiza a posição do pássaro considerando a gravidade """
        self.vel_y += 0.5  # Aplica a gravidade (aumenta a velocidade vertical)
        self.y += self.vel_y  # Atualiza a posição vertical do pássaro com base na velocidade
        if self.y < 0 or self.y > W_HEIGHT - self.image.get_height():  # Verifica se o pássaro saiu da tela
            return True  # Retorna True se o pássaro colidir com o topo ou o chão
        return False  # Continua o jogo se não houver colisão

    def draw(self, surface):
        """ Desenha o pássaro na tela """
        surface.blit(self.image, (self.x, self.y))  # Desenha o pássaro na posição atual

class Pipe:
    def __init__(self, x, height, images, speed):
        """ Inicializa o cano com sua posição, altura e velocidade """
        self.x = x  # Posição horizontal do cano
        self.height = height  # Altura do cano
        self.images = images  # Imagens do cano (corpo e extremidade)
        self.speed = speed  # Velocidade do movimento do cano
        self.scored = False  # Flag para indicar se o jogador já pontuou ao passar pelo cano

    def update(self):
        """ Atualiza a posição do cano, movendo-o para a esquerda """
        self.x -= self.speed  # Movimenta o cano para a esquerda

    def draw(self, surface):
        """ Desenha o cano na tela (parte superior e inferior) """
        # Desenha o corpo do cano superior
        surface.blit(self.images["pipe_body"], (self.x, self.height - self.images["pipe_body"].get_height()))
        # Desenha o corpo do cano inferior
        surface.blit(self.images["pipe_end"], (self.x, self.height + PIPE_GAP))

    def collide(self, bird_rect):
        """ Verifica colisão entre o pássaro e o cano """
        # Define o retângulo do cano superior
        upper_pipe_rect = pygame.Rect(self.x, self.height - self.images["pipe_body"].get_height(), PIPE_WIDTH, self.images["pipe_body"].get_height())
        # Define o retângulo do cano inferior
        lower_pipe_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, self.images["pipe_end"].get_height())
        # Verifica se o pássaro colidiu com qualquer parte do cano
        return bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect)

def load_theme_images(theme):
    """ Carrega as imagens correspondentes ao tema selecionado """
    background_image = load_image(f'images/{theme}/background_{theme}.png')  # Carrega a imagem de fundo
    background_image = pygame.transform.scale(background_image, (W_WIDTH, W_HEIGHT))  # Redimensiona a imagem de fundo
    return {
        "background": background_image,
        "bird_up": load_image(f'images/{theme}/charlie_{theme}_1.png', (30, 30)),  # Carrega a imagem do pássaro com asa para cima
        "bird_down": load_image(f'images/{theme}/charlie_{theme}_2.png', (30, 30)),  # Carrega a imagem do pássaro com asa para baixo
        "pipe_body": load_image(f'images/{theme}/barreira_corpo_{theme}.png'),  # Carrega a imagem do corpo do cano
        "pipe_end": load_image(f'images/{theme}/barreira_fim_{theme}.png'),  # Carrega a imagem da extremidade do cano
    }

def load_image(file_name, size=None):
    """ Carrega uma imagem de arquivo e opcionalmente redimensiona """
    img = pygame.image.load(file_name).convert_alpha()  # Carrega a imagem com transparência
    if size:
        img = pygame.transform.scale(img, size)  # Redimensiona a imagem se necessário
    return img  # Retorna a imagem carregada

def countdown_screen(screen, background_image):
    """ Exibe uma contagem regressiva antes de iniciar o jogo """
    font = pygame.font.Font(None, 100)  # Define a fonte da contagem
    for i in range(3, 0, -1):  # Laço de contagem regressiva de 3 até 1
        screen.blit(background_image, (0, 0))  # Desenha o fundo
        count_text = font.render(str(i), True, RED)  # Renderiza o número da contagem
        text_rect = count_text.get_rect(center=(W_WIDTH//2, W_HEIGHT//2))  # Centraliza o texto
        screen.blit(count_text, text_rect)  # Desenha o número na tela
        pygame.display.flip()  # Atualiza a tela
        time.sleep(1)  # Pausa por 1 segundo

def theme_selection_screen():
    """ Tela para o jogador selecionar o tema do jogo """
    screen.fill(BLACK)  # Preenche a tela com cor preta
    font = pygame.font.Font(None, 74)  # Define a fonte do título
    title = font.render("The Chosen", True, (128, 0, 0))  # Renderiza o título
    screen.blit(title, (W_WIDTH // 2 - title.get_width() // 2, 50))  # Centraliza o título na tela

    button_font = pygame.font.Font(None, 50)  # Fonte dos botões de seleção de tema
    buttons = [  # Definição dos botões com os nomes dos temas
        ("Castle", (W_WIDTH // 2, 200)),
        ("Florest", (W_WIDTH // 2, 300)),
        ("Twilight", (W_WIDTH // 2, 400))
    ]
    
    for text, pos in buttons:  # Laço que desenha os botões
        button = button_font.render(text, True, (0, 0, 0))  # Renderiza o texto do botão
        rect = button.get_rect(center=pos)  # Centraliza o texto do botão
        pygame.draw.rect(screen, BUTTON_COLOR, rect.inflate(20, 20))  # Desenha o botão
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, rect.inflate(20, 20), 3)  # Desenha a borda do botão
        screen.blit(button, rect)  # Desenha o texto sobre o botão

    pygame.display.flip()  # Atualiza a tela

    while True:  # Laço para capturar eventos do mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Se o jogador fechar o jogo
                pygame.quit()  # Fecha o Pygame
                quit()  # Sai do programa
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Se o jogador clicar com o botão esquerdo
                mouse_pos = pygame.mouse.get_pos()  # Captura a posição do mouse
                for text, pos in buttons:  # Verifica qual botão foi clicado
                    rect = pygame.Rect(pos[0] - 100, pos[1] - 25, 200, 50)  # Define a área clicável de cada botão
                    if rect.collidepoint(mouse_pos):  # Verifica se o clique foi dentro da área do botão
                        return text.lower()  # Retorna o tema selecionado (em minúsculas)

def game_over_screen(score):
    """ Exibe a tela de fim de jogo com a pontuação final """
    screen.fill(WHITE)  # Preenche a tela com cor branca
    font = pygame.font.Font(None, 74)  # Define a fonte do texto de fim de jogo
    text = font.render("Game Over", True, RED)  # Renderiza o texto "Game Over"
    score_text = font.render(f"Score: {score}", True, RED)  # Renderiza o texto da pontuação
    screen.blit(text, (W_WIDTH // 2 - text.get_width() // 2, W_HEIGHT // 2 - 100))  # Centraliza o texto "Game Over"
    screen.blit(score_text, (W_WIDTH // 2 - score_text.get_width() // 2, W_HEIGHT // 2))  # Centraliza o texto da pontuação
    pygame.display.flip()  # Atualiza a tela
    time.sleep(3)  # Pausa por 3 segundos

def main():
    # Tela de seleção de tema
    theme = theme_selection_screen()  # Chama a função para selecionar o tema
    images = load_theme_images(theme)  # Carrega as imagens correspondentes ao tema selecionado
    background_image = images["background"]  # Define a imagem de fundo do jogo

    bird = Bird(100, W_HEIGHT // 2, images)  # Cria uma instância do pássaro no centro da tela
    pipes = []  # Lista que vai armazenar os canos
    score = 0  # Pontuação inicial
    game_speed = BASE_SPEED  # Velocidade inicial do jogo
    pipe_timer = 0  # Controlador para adicionar novos canos

    countdown_screen(screen, background_image)  # Exibe a contagem regressiva antes de começar o jogo

    # Loop principal do jogo
    running = True  # Variável de controle do loop do jogo
    while running:
        screen.blit(background_image, (0, 0))  # Desenha o fundo na tela

        # Eventos do jogo (como teclado e mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Se o jogador fechar o jogo
                running = False  # Encerra o loop do jogo
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Se o jogador apertar a barra de espaço
                bird.jump()  # Faz o pássaro "pular"

        # Atualiza o pássaro
        if bird.update():  # Se o pássaro sair da tela, o jogo acaba
            game_over_screen(score)  # Exibe a tela de fim de jogo
            break  # Sai do loop principal

        # Atualiza os canos
        pipe_timer += 1  # Incrementa o contador para controle da criação de canos
        if pipe_timer > PIPE_SPACING / game_speed:  # Se o tempo para criar um novo cano for atingido
            pipe_height = random.randint(150, 400)  # Define uma altura aleatória para o cano
            pipes.append(Pipe(W_WIDTH, pipe_height, images, game_speed))  # Adiciona um novo cano à lista
            pipe_timer = 0  # Reinicia o timer de canos

        for pipe in pipes[:]:  # Itera sobre a lista de canos
            pipe.update()  # Atualiza a posição dos canos
            pipe.draw(screen)  # Desenha os canos na tela
            if pipe.x + PIPE_WIDTH < 0:  # Se o cano sair completamente da tela
                pipes.remove(pipe)  # Remove o cano da lista

            # Verifica se o pássaro passou por um cano e contabiliza a pontuação
            if not pipe.scored and pipe.x < bird.x:
                score += 1  # Aumenta a pontuação
                pipe.scored = True  # Marca que o jogador já pontuou neste cano

            # Verifica colisão entre o pássaro e os canos
            if pipe.collide(pygame.Rect(bird.x, bird.y, bird.image.get_width(), bird.image.get_height())):
                game_over_screen(score)  # Exibe a tela de fim de jogo
                running = False  # Encerra o jogo

        # Aumenta a velocidade do jogo conforme a pontuação
        if score >= MIN_SCORE_FOR_SPEED:
            game_speed = min(BASE_SPEED + score * SPEED_INCREMENT, MAX_SPEED)  # Aumenta a velocidade do jogo, mas limita à velocidade máxima

        bird.draw(screen)  # Desenha o pássaro na tela

        # Exibe a pontuação na tela
        font = pygame.font.Font(None, 36)  # Define a fonte para o texto da pontuação
        score_text = font.render(f"Score: {score}", True, WHITE)  # Renderiza o texto da pontuação
        screen.blit(score_text, (10, 10))  # Desenha o texto da pontuação no canto superior esquerdo

        pygame.display.flip()  # Atualiza a tela
        pygame.time.Clock().tick(60)  # Define o FPS (quadros por segundo) do jogo

    pygame.quit()  # Encerra o pygame quando o loop do jogo termina

if __name__ == "__main__":
    screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))  # Cria a janela do jogo
    pygame.display.set_caption("The Chosen")  # Define o título da janela
    main()  # Executa a função principal do jogo
