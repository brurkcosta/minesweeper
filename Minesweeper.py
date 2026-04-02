import pygame
import sys
import random

pygame.init()

# ================= CONFIG =================
LARGURA = 600
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Campo Minado")

FONTE = pygame.font.SysFont(None, 30)
FONTE_GRANDE = pygame.font.SysFont(None, 50)

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
VERDE = (100, 200, 100)
VERMELHO = (200, 50, 50)

# ================= MENU =================
def desenhar_texto(texto, x, y, fonte=FONTE):
    img = fonte.render(texto, 1, PRETO)
    TELA.blit(img, (x, y))

def menu():
    while 1:
        TELA.fill(BRANCO)

        desenhar_texto("CAMPO MINADO", 170, 100, FONTE_GRANDE)

        b1 = pygame.Rect(200, 220, 200, 50)
        b2 = pygame.Rect(200, 300, 200, 50)
        b3 = pygame.Rect(200, 380, 200, 200)

        pygame.draw.rect(TELA, VERDE, b1)
        pygame.draw.rect(TELA, VERDE, b2)
        pygame.draw.rect(TELA, VERDE, b3)

        desenhar_texto("Fácil", 260, 235)
        desenhar_texto("Médio", 260, 315)
        desenhar_texto("Difícil", 250, 395)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(evento.pos):
                    return 1
                if b2.collidepoint(evento.pos):
                    return 2
                if b3.collidepoint(evento.pos):
                    return 3

        pygame.display.update()

# ================= SUA LÓGICA =================
def criar_campo(n):
    if n == 1:
        return [[0 for _ in range(10)] for _ in range(10)]
    if n == 2:
        return [[0 for _ in range(15)] for _ in range(15)]
    if n == 3:
        return [[0 for _ in range(20)] for _ in range(20)]

def criar_jogador(n):
    if n == 1:
        return [["x" for _ in range(10)] for _ in range(10)]
    if n == 2:
        return [["x" for _ in range(15)] for _ in range(15)]
    if n == 3:
        return [["x" for _ in range(20)] for _ in range(20)]

def criar_bombas(matriz, quantidade, pi, pj):
    tamanho = len(matriz)
    bombas = 0

    while bombas < quantidade:
        i = random.randint(0, tamanho - 1)
        j = random.randint(0, tamanho - 1)

        if i == pi and j == pj:
            continue

        if matriz[i][j] != "B":
            matriz[i][j] = "B"
            bombas += 1

    return matriz

def dicas(matriz):
    tamanho = len(matriz)

    for i in range(tamanho):
        for j in range(tamanho):
            if matriz[i][j] == "B":
                continue

            dica = 0

            if i + 1 < tamanho and matriz[i + 1][j] == "B":
                dica += 1
            if j + 1 < tamanho and matriz[i][j + 1] == "B":
                dica += 1
            if i + 1 < tamanho and j + 1 < tamanho and matriz[i + 1][j + 1] == "B":
                dica += 1
            if i - 1 >= 0 and matriz[i - 1][j] == "B":
                dica += 1
            if i - 1 >= 0 and j + 1 < tamanho and matriz[i - 1][j + 1] == "B":
                dica += 1
            if j - 1 >= 0 and matriz[i][j - 1] == "B":
                dica += 1
            if i + 1 < tamanho and j - 1 >= 0 and matriz[i + 1][j - 1] == "B":
                dica += 1
            if i - 1 >= 0 and j - 1 >= 0 and matriz[i - 1][j - 1] == "B":
                dica += 1

            matriz[i][j] = dica

    return matriz

def abrir_casas(campo_real, campo_jogador, i, j):
    tamanho = len(campo_real)

    if i < 0 or i >= tamanho or j < 0 or j >= tamanho:
        return

    if campo_jogador[i][j] != "x":
        return

    campo_jogador[i][j] = campo_real[i][j]

    if campo_real[i][j] != 0:
        return

    abrir_casas(campo_real, campo_jogador, i+1, j)
    abrir_casas(campo_real, campo_jogador, i-1, j)
    abrir_casas(campo_real, campo_jogador, i, j+1)
    abrir_casas(campo_real, campo_jogador, i, j-1)
    abrir_casas(campo_real, campo_jogador, i+1, j+1)
    abrir_casas(campo_real, campo_jogador, i-1, j-1)
    abrir_casas(campo_real, campo_jogador, i+1, j-1)
    abrir_casas(campo_real, campo_jogador, i-1, j+1)

# ================= VITÓRIA =================
def tela_vitoria():
    while 1:
        TELA.fill(BRANCO)

        desenhar_texto("VOCÊ VENCEU!", 140, 150, FONTE_GRANDE)

        b_menu = pygame.Rect(200, 300, 200, 50)
        b_sair = pygame.Rect(200, 380, 200, 50)

        pygame.draw.rect(TELA, VERDE, b_menu)
        pygame.draw.rect(TELA, VERMELHO, b_sair)

        desenhar_texto("Menu", 260, 315)
        desenhar_texto("Sair", 270, 395)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if b_menu.collidepoint(evento.pos):
                    return
                if b_sair.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# ================= JOGO =================
def jogo(n):
    campo_real = criar_campo(n)
    campo_jogador = criar_jogador(n)

    if n == 1:
        bombas = 18
    if n == 2:
        bombas = 27
    if n == 3:
        bombas = 41

    tamanho = len(campo_real)
    total_casas = tamanho * tamanho - bombas

    primeira = 1
    rodando = 1
    TAM = LARGURA // tamanho

    while rodando:
        TELA.fill(BRANCO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                i = my // TAM
                j = mx // TAM

                # clique esquerdo
                if evento.button == 1:
                    if campo_jogador[i][j] == "F":
                        continue

                    if primeira == 1:
                        campo_real = criar_bombas(campo_real, bombas, i, j)
                        campo_real = dicas(campo_real)
                        primeira = 0

                    if campo_real[i][j] == "B":
                        print("Perdeu!")
                        rodando = 0
                    else:
                        abrir_casas(campo_real, campo_jogador, i, j)

                # clique direito (bandeira)
                if evento.button == 3:
                    if campo_jogador[i][j] == "x":
                        campo_jogador[i][j] = "F"
                    elif campo_jogador[i][j] == "F":
                        campo_jogador[i][j] = "x"

        # vitória
        fechadas = sum(linha.count("x") for linha in campo_jogador)
        abertas = tamanho * tamanho - fechadas

        if abertas == total_casas:
            tela_vitoria()
            return

        # desenhar grid
        for i in range(tamanho):
            for j in range(tamanho):
                rect = pygame.Rect(j*TAM, i*TAM, TAM, TAM)
                pygame.draw.rect(TELA, CINZA, rect, 1)

                valor = campo_jogador[i][j]

                if valor == "F":
                    desenhar_texto("B", j*TAM+10, i*TAM+5)
                elif valor != "x":
                    desenhar_texto(str(valor), j*TAM+10, i*TAM+5)

        pygame.display.update()

# ================= MAIN =================
while 1:
    dificuldade = menu()
    jogo(dificuldade)