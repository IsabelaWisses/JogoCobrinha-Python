import pygame  # Importa a biblioteca Pygame para criar o jogo
import time  # Importa a biblioteca time para manipular o tempo (por exemplo, pausa de 2 segundos)
import random  # Importa a biblioteca random para gerar posições aleatórias para a comida

# Inicialização do Pygame
pygame.init()

# Definição de cores usando o modelo RGB (Red, Green, Blue)
branco = (255, 255, 255)  # Cor branca
preto = (0, 0, 0)  # Cor preta
vermelho = (255, 0, 0)  # Cor vermelha
verde = (0, 255, 0)  # Cor verde
azul = (50, 153, 213)  # Cor azul
roxo = (128, 0, 128)  # Cor roxa
amarela = (255, 255, 0)  # Cor amarela

# Configuração da tela do jogo
largura = 1200  # Largura da tela
altura = 800  # Altura da tela
tela = pygame.display.set_mode((largura, altura))  # Criação da tela com as dimensões especificadas
pygame.display.set_caption('Jogo da Cobrinha em Python')  # Título da janela do jogo
relogio = pygame.time.Clock()  # Relógio para controlar a velocidade do jogo

# Configurações adicionais
bloco = 20  # Tamanho de cada "bloco" da cobrinha e da comida
velocidade_jogo = 15  # Velocidade do jogo
recorde = 0  # Recorde inicial de pontuação

# Dicionário de cores para a cobrinha (apenas Azul, Roxa e Amarela)
cores_cobra = {
    "Azul": azul,
    "Roxa": roxo,
    "Amarela": amarela
}

# Carregar e ajustar a imagem da melancia (comida)
imagem_comida = pygame.image.load("melancia.png")  # Carrega a imagem da melancia
imagem_comida = pygame.transform.scale(imagem_comida, (bloco, bloco))  # Ajusta o tamanho da melancia para o bloco da cobrinha

# Função para gerar a posição aleatória da comida
def gerar_comida():
    comida_x = round(random.randrange(0, largura - bloco) / 20.0) * 20.0  # Posição aleatória em X
    comida_y = round(random.randrange(0, altura - bloco) / 20.0) * 20.0  # Posição aleatória em Y
    return comida_x, comida_y  # Retorna as coordenadas da comida

# Função para desenhar a comida na tela
def desenhar_comida(comida_x, comida_y):
    tela.blit(imagem_comida, (comida_x, comida_y))  # Desenha a melancia na posição da comida

# Função para desenhar a cobrinha
def desenhar_cobra(tamanho, pixels, cor):
    for pixel in pixels:
        pygame.draw.rect(tela, cor, [pixel[0], pixel[1], tamanho, tamanho])  # Desenha cada parte da cobrinha

# Função para desenhar a pontuação na tela
def desenhar_pontuacao(pontuacao, recorde):
    fonte = pygame.font.SysFont('Showcard Gothic', 35)  # Define a fonte do texto
    texto = fonte.render(f"PONTOS: {pontuacao}  |  RECORD: {recorde}", True, branco)  # Renderiza a pontuação
    tela.blit(texto, [10, 10])  # Desenha o texto na tela

# Função para mostrar uma mensagem (fim de jogo ou novo recorde)
def mostrar_mensagem(texto1, texto2):
    fonte = pygame.font.SysFont('Showcard Gothic', 40)  # Define a fonte do texto
    msg1 = fonte.render(texto1, True, vermelho)  # Primeira parte da mensagem
    msg2 = fonte.render(texto2, True, vermelho)  # Segunda parte da mensagem

    # Centraliza as mensagens na tela
    rect1 = msg1.get_rect(center=(largura // 2, altura // 2 - 30))
    rect2 = msg2.get_rect(center=(largura // 2, altura // 2 + 30))

    tela.blit(msg1, rect1)  # Desenha a primeira mensagem
    tela.blit(msg2, rect2)  # Desenha a segunda mensagem
    pygame.display.update()  # Atualiza a tela
    time.sleep(2)  # Pausa por 2 segundos

    # Espera o jogador pressionar qualquer tecla para reiniciar
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

# Função para selecionar a direção da cobrinha com base nas teclas pressionadas
def selecionar_velocidade(tecla, velocidade_atual):
    if tecla == pygame.K_DOWN and velocidade_atual != (0, -bloco):  # Para mover para baixo
        return 0, bloco
    elif tecla == pygame.K_UP and velocidade_atual != (0, bloco):  # Para mover para cima
        return 0, -bloco
    elif tecla == pygame.K_RIGHT and velocidade_atual != (-bloco, 0):  # Para mover para a direita
        return bloco, 0
    elif tecla == pygame.K_LEFT and velocidade_atual != (bloco, 0):  # Para mover para a esquerda
        return -bloco, 0
    return velocidade_atual  # Retorna a velocidade atual caso nenhuma tecla seja pressionada

# Função para escolher a cor da cobrinha
def escolher_cor():
    fonte = pygame.font.SysFont('Showcard Gothic', 29)  # Define a fonte para o texto
    tela.fill(preto)  # Preenche o fundo da tela com a cor preta
    
    # Centralizando o título
    titulo = fonte.render("Escolha a cor da cobrinha:", True, branco)
    tela.blit(titulo, (largura // 1.85 - titulo.get_width() // 2, 200))

    # Botoes para as cores Azul, Roxa e Amarela com espaçamento
    botoes = {
        "Azul": pygame.Rect(400, 400, 150, 80),
        "Roxa": pygame.Rect(600, 400, 150, 80),
        "Amarela": pygame.Rect(800, 400, 150, 80)
    }

    # Loop para esperar a escolha do jogador
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for nome, botao in botoes.items():
                    if botao.collidepoint(pos):  # Se o jogador clicar em um dos botões
                        return cores_cobra[nome]  # Retorna a cor escolhida

        # Desenha os botões com a cor correspondente
        for nome, botao in botoes.items():
            pygame.draw.rect(tela, cores_cobra[nome], botao)  # Desenha o botão com a cor
            texto = fonte.render(nome, True, preto)  # Desenha o nome do botão
            texto_rect = texto.get_rect(center=botao.center)  # Centraliza o texto no botão
            tela.blit(texto, texto_rect)

        pygame.display.update()  # Atualiza a tela

# Função principal do jogo
def rodar_jogo():
    global recorde  # Variável global para armazenar o recorde

    # Escolher a cor da cobrinha
    cor_cobra = escolher_cor()

    fim_jogo = False
    x = largura / 2  # Posição inicial da cobrinha em X
    y = altura / 2  # Posição inicial da cobrinha em Y
    velocidade_x = 0  # Velocidade inicial da cobrinha em X
    velocidade_y = 0  # Velocidade inicial da cobrinha em Y
    tamanho_cobra = 1  # Tamanho inicial da cobrinha
    pixels = []  # Lista para armazenar os segmentos da cobrinha

    comida_x, comida_y = gerar_comida()  # Gera a comida na tela

    while not fim_jogo:
        tela.fill(preto)  # Preenche o fundo com a cor preta

        for evento in pygame.event.get():  # Checa os eventos (como pressionamento de teclas)
            if evento.type == pygame.QUIT:  # Se o jogador fechar a janela
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:  # Se uma tecla for pressionada
                velocidade_x, velocidade_y = selecionar_velocidade(
                    evento.key, (velocidade_x, velocidade_y))  # Atualiza a direção

        # Atualiza a posição da cobrinha
        x += velocidade_x
        y += velocidade_y

        # Verifica se a cobrinha bateu nas bordas
        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True

        pixels.append([x, y])  # Adiciona a nova posição da cabeça da cobrinha
        if len(pixels) > tamanho_cobra:  # Se a cobrinha crescer, remove o último segmento
            del pixels[0]

        # Verifica se a cobrinha se bateu
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                fim_jogo = True

        desenhar_comida(comida_x, comida_y)  # Desenha a comida
        desenhar_cobra(bloco, pixels, cor_cobra)  # Desenha a cobrinha
        desenhar_pontuacao(tamanho_cobra - 1, recorde)  # Desenha a pontuação

        pygame.display.update()  # Atualiza a tela

        # Verifica se a cobrinha comeu a comida
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1  # Aumenta o tamanho da cobrinha
            comida_x, comida_y = gerar_comida()  # Gera uma nova comida

        relogio.tick(velocidade_jogo)  # Controla a velocidade do jogo

    # Fim de jogo
    pontuacao_final = tamanho_cobra - 1
    tela.fill(preto)  # Limpa a tela
    if pontuacao_final > recorde:
        recorde = pontuacao_final  # Atualiza o recorde se a pontuação for maior
        mostrar_mensagem("NOVO RECORD!", "Pressione qualquer tecla para jogar de novo.")
    else:
        mostrar_mensagem("GAME OVER!", "Pressione qualquer tecla para jogar de novo.")

    rodar_jogo()  # Reinicia o jogo

# Início do jogo
rodar_jogo()

#Cauã Davi, César Brum, Felipe Augusto, Gabriel Duarte, Gabriel Jardim, Isabela Wisses, João Victor, Yuri Duarte.
