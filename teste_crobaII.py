import pygame
import sys
import random
import time

# Inicializar pygame e fontes
pygame.init()
pygame.font.init()
minha_fonte = pygame.font.SysFont('Comic Sans MS', 20)

# Definições iniciais
TAM_TELA = (1000, 650)
tela = pygame.display.set_mode(TAM_TELA)
tempo = pygame.time.Clock()
pontuacao = 0

# Carregar e ajustar imagens
imagem_maca = pygame.image.load('pngwing.com.png')
imagem_cabeca_cobra = pygame.image.load('soralinda.png')

# Ajustar tamanho das imagens para 50x50 pixels (já que a cobra e a comida são 50x50)
imagem_maca = pygame.transform.scale(imagem_maca, (50, 50))
imagem_cabeca_cobra = pygame.transform.scale(imagem_cabeca_cobra, (50, 50))

# Funções relacionadas à comida
def inicializa_comida(tam_tela):
    return [random.randrange(0, tam_tela[0] - 50, 50), random.randrange(0, tam_tela[1] - 50, 50)]

def gera_nova_comida(tam_tela):
    return inicializa_comida(tam_tela)

# Funções relacionadas à cobra
def inicializa_cobra():
    return [300, 300], [[300, 300], [250, 300], [200, 300]], 'DIREITA'

def muda_direcao(direcao_atual, nova_direcao):
    direcoes_opostas = {'DIREITA': 'ESQUERDA', 'ESQUERDA': 'DIREITA', 'CIMA': 'BAIXO', 'BAIXO': 'CIMA'}
    if direcoes_opostas[nova_direcao] != direcao_atual:
        return nova_direcao
    return direcao_atual

def move_cobra(posicao, corpo, direcao, posicao_comida):
    if direcao == 'DIREITA':
        posicao[0] += 50
    elif direcao == 'ESQUERDA':
        posicao[0] -= 50
    elif direcao == 'CIMA':
        posicao[1] -= 50
    elif direcao == 'BAIXO':
        posicao[1] += 50

    corpo.insert(0, list(posicao))

    if posicao == posicao_comida:
        return posicao, corpo, True
    else:
        corpo.pop()
        return posicao, corpo, False

def verifica_colisao(posicao, corpo, tam_tela):
    if posicao[0] >= tam_tela[0] or posicao[0] < 0 or posicao[1] >= tam_tela[1] or posicao[1] < 0:
        return True
    for parte_do_corpo in corpo[1:]:
        if posicao == parte_do_corpo:
            return True
    return False

# Inicializa cobra e comida
posicao_cobra, corpo_cobra, direcao_cobra = inicializa_cobra()
posicao_comida = inicializa_comida(TAM_TELA)

# Loop principal do jogo
while True:
    tela.fill((177, 156, 217))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direcao_cobra = muda_direcao(direcao_cobra, 'DIREITA')
            elif event.key == pygame.K_UP:
                direcao_cobra = muda_direcao(direcao_cobra, 'CIMA')
            elif event.key == pygame.K_DOWN:
                direcao_cobra = muda_direcao(direcao_cobra, 'BAIXO')
            elif event.key == pygame.K_LEFT:
                direcao_cobra = muda_direcao(direcao_cobra, 'ESQUERDA')

    posicao_cobra, corpo_cobra, comida_devorada = move_cobra(posicao_cobra, corpo_cobra, direcao_cobra, posicao_comida)

    if verifica_colisao(posicao_cobra, corpo_cobra, TAM_TELA):
        tela.fill((177, 156, 217))
        pontos = minha_fonte.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
        tela.blit(pontos, (10, 10))
        voce_perdeu = minha_fonte.render('VOCÊ PERDEU!', True, (255, 255, 255))
        tela.blit(voce_perdeu, (210, 180))
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    if comida_devorada:
        pontuacao += 1
        posicao_comida = gera_nova_comida(TAM_TELA)

    pontos = minha_fonte.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
    tela.blit(pontos, (10, 10))

    # Desenhar a cabeça da cobra
    tela.blit(imagem_cabeca_cobra, pygame.Rect(corpo_cobra[0][0], corpo_cobra[0][1], 50, 50))

    # Desenhar o corpo da cobra
    for pos in corpo_cobra[1:]:
        pygame.draw.rect(tela, pygame.Color(70, 41, 90), pygame.Rect(pos[0], pos[1], 50, 50))

    # Desenhar a comida
    tela.blit(imagem_maca, pygame.Rect(posicao_comida[0], posicao_comida[1], 50, 50))

    pygame.display.update()
    tempo.tick(5)  # Ajuste o valor para mudar a velocidade do jogo
