# Autor: Gabriel Gatti da Silva

import pygame
from batalha import Batalha
from menu_inicial import Menu
from cores import Cores

# Inicializar o Pygame
pygame.init()
# Inicializar o mixer do Pygame
pygame.mixer.init()

# Carrega a música
pygame.mixer.music.load('media/musics/The Frozen Hobgoblin - Erlend Flatin.mp3')
pygame.mixer.music.play(-1)

# Configuração da janela do jogo
largura = 1024
altura = 768
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("IntroBattle")

# Carregar a imagem de fundo
img_fundo = pygame.image.load("media/imagens/background.png")
img_fundo = pygame.transform.scale(img_fundo, (largura, altura))

# Carregar os menus de ação
img_menu = pygame.image.load("media/imagens/ret_menu2.png")
img_menu_dir = pygame.transform.scale(img_menu, (470, 220))
img_menu_esq = pygame.transform.scale(img_menu, (670, 220))

# Carregar seta de seleção
img_seta = pygame.image.load("media/imagens/setinha.png")
img_seta_baixo = pygame.transform.scale(img_seta, (50, 35))
img_seta_lado = pygame.transform.rotate(img_seta_baixo, 90)

menu_inicial = Menu()
batalha = Batalha()

estado_jogo = 'menu_inicial'
estado_batalha = None
posicao_seta_menu_inicial = 0
posicao_seta_menu = 0

# Loop do jogo
executando = True
fps = 60
clock = pygame.time.Clock()

while executando:
    janela.blit(img_fundo, (0,0))
    clock.tick(fps)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        if estado_jogo == 'menu_inicial':
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    if posicao_seta_menu_inicial == 0:
                        posicao_seta_menu_inicial = 1
                    elif posicao_seta_menu_inicial == 1:
                        posicao_seta_menu_inicial = 2
                    elif posicao_seta_menu_inicial == 3:
                        posicao_seta_menu_inicial = 4
                elif evento.key == pygame.K_LEFT:
                    if posicao_seta_menu_inicial == 1:
                        posicao_seta_menu_inicial = 0
                    elif posicao_seta_menu_inicial == 2:
                        posicao_seta_menu_inicial = 1
                    elif posicao_seta_menu_inicial == 4:
                        posicao_seta_menu_inicial = 3
                elif evento.key == pygame.K_DOWN:
                    if posicao_seta_menu_inicial == 0:
                        posicao_seta_menu_inicial = 3
                    elif posicao_seta_menu_inicial == 1:
                        posicao_seta_menu_inicial = 3
                    elif posicao_seta_menu_inicial == 2:
                        posicao_seta_menu_inicial = 4
                elif evento.key == pygame.K_UP:
                    if posicao_seta_menu_inicial == 3:
                        posicao_seta_menu_inicial = 0
                    elif posicao_seta_menu_inicial == 4:
                        posicao_seta_menu_inicial = 1
                elif evento.key == pygame.K_z:
                    menu_inicial.seleciona_personagem(posicao_seta_menu_inicial)
                    if menu_inicial.selecionou_todos():
                        estado_jogo = 'jogando'
                        # Carrega a música da batalha
                        pygame.mixer.music.load('media/musics/Battle Music WAV.mp3')
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.1)
                        batalha.cria_personagens(menu_inicial.personagens_selecionados)
                        estado_batalha = 'selecionando_acao'
        elif estado_batalha == 'selecionando_acao':
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    if posicao_seta_menu == 0:
                        posicao_seta_menu = 1
                elif evento.key == pygame.K_LEFT:
                    if posicao_seta_menu == 1:
                        posicao_seta_menu = 0
                elif evento.key == pygame.K_z:
                    if posicao_seta_menu == 0:
                        estado_batalha = 'selecionando_alvo'
                        posicao_seta_menu = 0
                        if(batalha.esta_morto(0)):
                            posicao_seta_menu = 1
                    elif posicao_seta_menu == 1:
                        estado_batalha = 'defesa'
                        batalha.efetua_defesa()
                        estado_batalha = 'mostrando_defesa'
        elif estado_batalha == 'selecionando_alvo':
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    if posicao_seta_menu == 0 and not(batalha.esta_morto(1)):
                        posicao_seta_menu = 1
                elif evento.key == pygame.K_UP:
                    if posicao_seta_menu == 1 and not(batalha.esta_morto(0)):
                        posicao_seta_menu = 0
                elif evento.key == pygame.K_z:
                    estado_batalha = 'ataque'
                    batalha.efetua_ataque(posicao_seta_menu)
                    estado_batalha = 'mostrando_ataque'
                elif evento.key == pygame.K_x:
                    estado_batalha = 'selecionando_acao'
                    posicao_seta_menu = 0
        elif estado_batalha == 'mostrando_ataque' or estado_batalha == 'mostrando_defesa':
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_z:
                    if batalha.verifica_fim_batalha() == 'continua':
                        proximo = batalha.atualiza_ordem()
                        if proximo == 'inimigo':
                            acao_inimigo = batalha.realiza_acao_do_inimigo()
                            if acao_inimigo == 'ataque':
                                estado_batalha = 'mostrando_ataque'
                            elif acao_inimigo == 'defesa':
                                estado_batalha = 'mostrando_defesa'
                        else:
                            estado_batalha = 'selecionando_acao'
                            posicao_seta_menu = 0
                    # Acabou o jogo
                    else:
                        estado_jogo = batalha.verifica_fim_batalha()
                        if estado_jogo == 'derrota':
                            # Carrega a música da derrota
                            pygame.mixer.music.load('media/musics/hopeless-119866.mp3')
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(1)
                        else:
                            pygame.mixer.music.load('media/musics/The Frozen Hobgoblin - Erlend Flatin.mp3')
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(1)
        elif estado_jogo == 'vitoria' or estado_jogo == 'derrota':
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_z:
                    estado_jogo = 'menu_inicial'
                    pygame.mixer.music.load('media/musics/The Frozen Hobgoblin - Erlend Flatin.mp3')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(1)
                elif evento.key == pygame.K_ESCAPE:
                    executando = False
    
    if estado_jogo == 'menu_inicial':
        # Desenhar o menu
        menu_inicial.desenhar_menu(janela)

        # Atualiza a posição da seta
        if posicao_seta_menu_inicial == 0:
            janela.blit(img_seta_baixo, (170, 180))
        elif posicao_seta_menu_inicial == 1:
            janela.blit(img_seta_baixo, (490, 180))
        elif posicao_seta_menu_inicial == 2:
            janela.blit(img_seta_baixo, (800, 180))
        elif posicao_seta_menu_inicial == 3:
            janela.blit(img_seta_baixo, (325, 460))
        elif posicao_seta_menu_inicial == 4:
            janela.blit(img_seta_baixo, (638, 460))
    elif estado_jogo == 'jogando':
        # Desenhar os personagens da batalha
        batalha.desenha_bonecos(janela)

        # Desenhar menus de ação
        janela.blit(img_menu_dir, (600, 530))
        janela.blit(img_menu_esq, (10, 530))

        # Atualiza o menu de acordo com o estado da batalha
        batalha.atualiza_menu(janela, estado_batalha, posicao_seta_menu)

        if estado_batalha == 'selecionando_acao':
            # Atualiza a posição da seta
            if posicao_seta_menu == 0:
                janela.blit(img_seta_lado, (35, 610))
            else:
                janela.blit(img_seta_lado, (365, 610))
        elif estado_batalha == 'selecionando_alvo':
            # Atualiza a posição da seta
            if posicao_seta_menu == 0:
                janela.blit(img_seta_baixo, (805, 125))
            else:
                janela.blit(img_seta_baixo, (725, 295))
    elif estado_jogo == 'vitoria' or estado_jogo == 'derrota':
        # Reseta jogo
        menu_inicial = Menu()
        batalha = Batalha()
        posicao_seta_menu_inicial = 0
        posicao_seta_menu = 0
        estado_batalha = None

        # Desenhar a tela de vitoria/derrota
        largura_retangulo = 400
        altura_retangulo = 100
        cor_retangulo = (0, 0, 0)  # Preto
        cor_borda = (255, 255, 255)  # Branco

        # Posição do retângulo (centralizado horizontalmente)
        posicao_retangulo = ((1024 - largura_retangulo) // 2, 290)

        fonte = pygame.font.Font('media/font/EightBitDragon-anqx.ttf', 40)
        if estado_jogo == 'vitoria':
            texto_resultado = fonte.render('Victory!', True, Cores.TEXTO_PADRAO.value)
        else:
            texto_resultado = fonte.render('Game Over', True, Cores.TEXTO_PADRAO.value)
        posicao_texto_resultado = texto_resultado.get_rect(center=(posicao_retangulo[0] + largura_retangulo // 2, posicao_retangulo[1] + altura_retangulo // 2))

        fonte = pygame.font.Font('media/font/EightBitDragon-anqx.ttf', 30)
        texto_fim_z = fonte.render('Press Z to return to the main menu', True, Cores.TEXTO_PADRAO.value)
        posicao_texto_fim_z = texto_fim_z.get_rect(center=(posicao_retangulo[0] + largura_retangulo // 2, posicao_retangulo[1] + altura_retangulo // 2 + 100))
        texto_fim_quit = fonte.render('Press ESC to quit', True, Cores.TEXTO_PADRAO.value)
        posicao_texto_fim_quit = texto_fim_quit.get_rect(center=(posicao_retangulo[0] + largura_retangulo // 2, posicao_retangulo[1] + altura_retangulo // 2 + 150))

        pygame.draw.rect(janela, cor_borda, (posicao_retangulo, (largura_retangulo, altura_retangulo)), 10)  # Borda de 4 pixels
        pygame.draw.rect(janela, cor_retangulo, ((posicao_retangulo[0]+10,posicao_retangulo[1]+10), (largura_retangulo-20, altura_retangulo-20)))

        janela.blit(texto_resultado, posicao_texto_resultado)
        janela.blit(texto_fim_z, posicao_texto_fim_z)
        janela.blit(texto_fim_quit, posicao_texto_fim_quit)


    pygame.display.flip()


# Encerrar o jogo
pygame.quit()