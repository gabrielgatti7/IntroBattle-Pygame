import pygame
from cores import Cores

class Menu:
    def __init__(self):
        self.personagens = ['Paladin', 'Rogue', 'Wizard', 'Hunter', 'Priest']
        self.fonte = pygame.font.Font('font/EightBitDragon-anqx.ttf', 30)
        self.opcoes = []
        self.opcoes_saltadas = []
        img_menu = pygame.image.load("imagens/ret_menu2.png")
        for nome in self.personagens:
            personagem_img = pygame.image.load(f"imagens/{nome}.png".lower())
            personagem_img = pygame.transform.scale(personagem_img, (150, 150))
            if nome == 'Wizard':
                personagem_img = pygame.transform.flip(personagem_img, True, False)
            texto_nome = self.fonte.render(f"{nome}", True, Cores.TEXTO_PADRAO.value)
            img_menu_scaled = pygame.transform.scale(img_menu, (200, 200))
            self.opcoes.append([personagem_img, img_menu_scaled, texto_nome, 0])
            self.opcoes_saltadas.append([pygame.transform.scale(personagem_img, (180, 180)), pygame.transform.scale(img_menu_scaled, (220, 220)), texto_nome])
        self.personagens_selecionados = []

    def desenhar_menu(self, janela):
        largura_retangulo = 400
        altura_retangulo = 100
        cor_retangulo = (0, 0, 0)  # Preto
        cor_borda = (255, 255, 255)  # Branco

        # Posição do retângulo (centralizado horizontalmente)
        posicao_retangulo = ((1024 - largura_retangulo) // 2, 50)

        fonte_titulo = pygame.font.Font('font/EightBitDragon-anqx.ttf', 40)
        titulo = fonte_titulo.render('IntroBattle!', True, Cores.TEXTO_PADRAO.value)
        posicao_titulo = titulo.get_rect(center=(posicao_retangulo[0] + largura_retangulo // 2, posicao_retangulo[1] + altura_retangulo // 2))

        pygame.draw.rect(janela, cor_borda, (posicao_retangulo, (largura_retangulo, altura_retangulo)), 10)  # Borda de 4 pixels
        pygame.draw.rect(janela, cor_retangulo, ((posicao_retangulo[0]+10,posicao_retangulo[1]+10), (largura_retangulo-20, altura_retangulo-20)))

        janela.blit(titulo, posicao_titulo)

        # Paladin
        if(self.opcoes[0][3] == 1):
            janela.blit(self.opcoes_saltadas[0][2], (130, 430+10))
            janela.blit(self.opcoes_saltadas[0][1], (105-10, 220-10))
            janela.blit(self.opcoes_saltadas[0][0], (115-10, 240-10))
        else:
            janela.blit(self.opcoes[0][2], (130, 430))
            janela.blit(self.opcoes[0][1], (105, 220))
            janela.blit(self.opcoes[0][0], (115, 240))
        # Rogue
        if(self.opcoes[1][3] == 1):
            janela.blit(self.opcoes_saltadas[1][2], (2*125+210, 430+10))
            janela.blit(self.opcoes_saltadas[1][1], (2*105+210-10, 220-10))
            janela.blit(self.opcoes_saltadas[1][0], (2*115+210-10, 240-10))
        else:
            janela.blit(self.opcoes[1][2], (2*125+210, 430))
            janela.blit(self.opcoes[1][1], (2*105+210, 220))
            janela.blit(self.opcoes[1][0], (2*115+210, 240))
        # Wizard
        if(self.opcoes[2][3] == 1):
            janela.blit(self.opcoes_saltadas[2][2], (3*125+2*210, 430+10))
            janela.blit(self.opcoes_saltadas[2][1], (3*105+2*210-10, 220-10))
            janela.blit(self.opcoes_saltadas[2][0], (3*115+2*210-32, 240-10))
        else:
            janela.blit(self.opcoes[2][2], (3*115+2*210, 430))
            janela.blit(self.opcoes[2][1], (3*105+2*210, 220))
            janela.blit(self.opcoes[2][0], (3*115+2*203, 240))
        # Hunter
        if(self.opcoes[3][3] == 1):
            janela.blit(self.opcoes_saltadas[3][2], (285, 710+10))
            janela.blit(self.opcoes_saltadas[3][1], (260-10, 500-10))
            janela.blit(self.opcoes_saltadas[3][0], (270-10, 520-10))
        else:
            janela.blit(self.opcoes[3][2], (285, 710))
            janela.blit(self.opcoes[3][1], (260, 500))
            janela.blit(self.opcoes[3][0], (270, 520))
        # Priest
        if(self.opcoes[4][3] == 1):
            janela.blit(self.opcoes_saltadas[4][2], (285+320, 710+10))
            janela.blit(self.opcoes_saltadas[4][1], (260+310-10, 500-10))
            janela.blit(self.opcoes_saltadas[4][0], (270+320-10, 520-10))
        else:
            janela.blit(self.opcoes[4][2], (285+320, 710))
            janela.blit(self.opcoes[4][1], (260+310, 500))
            janela.blit(self.opcoes[4][0], (270+320, 520))
    
    def seleciona_personagem(self, posicao):
        nome = self.personagens[posicao]
        if nome in self.personagens_selecionados:
            self.personagens_selecionados.remove(nome)
            self.opcoes[self.personagens.index(nome)][3] = 0
        else:
            self.personagens_selecionados.append(nome)
            self.opcoes[self.personagens.index(nome)][3] = 1

    def selecionou_todos(self):
        return len(self.personagens_selecionados) == 3