import pygame
from personagem import Personagem
import random
from cores import Cores

class Batalha:
    def __init__(self):
        self.aliados = []
        self.aliados_imgs = []
        self.inimigos = []
        self.inimigos_imgs = []
        self.posicoes_aliados = [(180, 180), (50, 280), (180, 360)]
        self.posicoes_inimigos = [(750, 160), (680, 330)]
        self.ordem_personagens = []
        self.personagem_atual = 0
        self.aliados_mortos = 0
        self.inimigos_mortos = 0
        self.ultimo_aliado_atacado = 0

    def cria_personagens(self, selecao):
        if 'Paladin' in selecao:
            self.aliados.append(Personagem('Paladin', 100, 10, 10, 7))
        if 'Rogue' in selecao:
            self.aliados.append(Personagem('Rogue', 80, 15, 5, 20))
        if 'Wizard' in selecao:
            self.aliados.append(Personagem('Wizard', 60, 20, 10, 10))
        if 'Hunter' in selecao:
            self.aliados.append(Personagem('Hunter', 70, 12, 8, 15))
        if 'Priest' in selecao:
            self.aliados.append(Personagem('Priest', 50, 5, 15, 8))
        
        self.inimigos.append(Personagem('Necromancer', 80, 30, 15, 4))
        self.inimigos.append(Personagem('Skeleton', 40, 5, 1, 5))

        for aliado in self.aliados:
            aliado_img = pygame.image.load(f"imagens/{aliado.nome}.png".lower())
            aliado_img = pygame.transform.scale(aliado_img, (150, 150))
            if aliado.nome == 'Wizard':
                aliado_img = pygame.transform.flip(aliado_img, True, False)
            self.aliados_imgs.append(aliado_img)

        for inimigos in self.inimigos:
            inimigo_img = pygame.image.load(f"imagens/{inimigos.nome}.png".lower())
            inimigo_img = pygame.transform.scale(inimigo_img, (150, 150))
            inimigo_img = pygame.transform.flip(inimigo_img, True, False)
            self.inimigos_imgs.append(inimigo_img)

        self.ordem_personagens = self.aliados + self.inimigos
        self.ordem_personagens = sorted(self.ordem_personagens, key=lambda x: x.velocidade, reverse=True)

    def desenha_bonecos(self, janela):
        i = 0
        for aliado_img in self.aliados_imgs:
            if not(self.aliados[i].morreu()):
                janela.blit(aliado_img, self.posicoes_aliados[i])
            i += 1
        i = 0
        for inimigo_img in self.inimigos_imgs:
            if not(self.inimigos[i].morreu()):
                janela.blit(inimigo_img, self.posicoes_inimigos[i])
            i += 1
    
    def atualiza_ordem(self):
        self.personagem_atual += 1
        if self.personagem_atual >= len(self.ordem_personagens):
            self.personagem_atual = 0
        while(self.ordem_personagens[self.personagem_atual].morreu()):
            self.personagem_atual += 1
            if self.personagem_atual >= len(self.ordem_personagens):
                self.personagem_atual = 0
        
        self.ordem_personagens[self.personagem_atual].reseta_turno()

        if self.ordem_personagens[self.personagem_atual] in self.aliados:
            return 'aliado'
        else:
            return 'inimigo'

    def atualiza_menu(self, janela, estado_batalha, posicao_seta_menu):
        # Desenha a vida dos aliados no menu direito
        for i, aliado in enumerate(self.aliados):
            fonte = pygame.font.Font(None, 45)
            if aliado.morreu():
                texto_nome = fonte.render(f"{aliado.nome.upper()}", True, Cores.MORTO.value)
                texto_vida = fonte.render(f"{aliado.vida_atual}/{aliado.vida_total}", True, Cores.MORTO.value)
            else:
                texto_nome = fonte.render(f"{aliado.nome.upper()}", True, Cores.TEXTO_PADRAO.value)
                texto_vida = fonte.render(f"{aliado.vida_atual}/{aliado.vida_total}", True, Cores.TEXTO_PADRAO.value)
                if aliado.esta_defendendo():
                    texto_nome = fonte.render(f"{aliado.nome.upper()}", True, Cores.DEFESA.value)
                    texto_vida = fonte.render(f"{aliado.vida_atual}/{aliado.vida_total}", True, Cores.DEFESA.value)
            janela.blit(texto_nome, (665, 570 + 53 * i))
            janela.blit(texto_vida, (850, 570 + 53 * i))

        personagem = self.ordem_personagens[self.personagem_atual]

        if estado_batalha == 'selecionando_acao':
            # Desenha a vez do personagem atual e as opções de ação
            if personagem in self.aliados:
                # Desenhar açoes do personagem
                fonte = pygame.font.Font(None, 45)
                texto_vez = fonte.render(f"{personagem.nome.upper()}\'S TURN", True, Cores.TEXTO_PADRAO.value)
                janela.blit(texto_vez, (70, 570))
                texto_attack = fonte.render("ATTACK", True, Cores.TEXTO_PADRAO.value)
                janela.blit(texto_attack, (70, 620))
                texto_defend = fonte.render("DEFEND", True, Cores.TEXTO_PADRAO.value)
                janela.blit(texto_defend, (400, 620))
                texto_atk_status = fonte.render(f"ATK: {personagem.ataque}", True, Cores.ATAQUE.value)
                janela.blit(texto_atk_status, (70, 680))
                texto_def_status = fonte.render(f"DEF:", True, Cores.DEFESA.value)
                janela.blit(texto_def_status, (400, 680))
                texto_def_status = fonte.render(f"{personagem.defesa_atual}", True, Cores.DEFESA.value)
                if personagem.esta_defendendo():
                    texto_def_status = fonte.render(f"{personagem.defesa_atual}", True, Cores.BUFF_DEFESA.value)
                janela.blit(texto_def_status, (480, 680))
            else:
                pass
        elif estado_batalha == 'selecionando_alvo':
            if posicao_seta_menu == 0 or posicao_seta_menu == 1:
                fonte = pygame.font.Font(None, 45)
                texto_escolhendo = fonte.render("SELECTING ENEMY TO ATTACK", True, Cores.TEXTO_PADRAO.value)
                janela.blit(texto_escolhendo, (70, 570))
                texto_nome_inimigo = fonte.render(f"{self.inimigos[posicao_seta_menu].nome.upper()}", True, Cores.NOME_INIMIGO.value)
                janela.blit(texto_nome_inimigo, (70, 620))
                texto_vida_inimigo = fonte.render(f"HP: {self.inimigos[posicao_seta_menu].vida_atual}/{self.inimigos[posicao_seta_menu].vida_total}", True, Cores.VIDA_INIMIGO.value)
                janela.blit(texto_vida_inimigo, (70, 670))
                texto_def = fonte.render("DEF: ", True, Cores.DEFESA.value)
                janela.blit(texto_def, (350, 670))
                if self.inimigos[posicao_seta_menu].esta_defendendo():
                    texto_defesa_inimigo = fonte.render(f"{self.inimigos[posicao_seta_menu].defesa_atual}", True, Cores.BUFF_DEFESA.value)
                else:
                    texto_defesa_inimigo = fonte.render(f"{self.inimigos[posicao_seta_menu].defesa_atual}", True, Cores.DEFESA.value)
                janela.blit(texto_defesa_inimigo, (430, 670))
        elif estado_batalha == 'mostrando_ataque':
            if personagem in self.aliados:
                # Desenha o dano causado
                fonte = pygame.font.Font(None, 45)
                texto_dano = fonte.render(f"{personagem.nome.upper()} DEALT {personagem.ultimo_dano_causado} DAMAGE!", True, Cores.DANO.value)
                janela.blit(texto_dano, (60, 580))
                if self.inimigos[posicao_seta_menu].morreu():
                    texto_morte = fonte.render(f"{self.inimigos[posicao_seta_menu].nome.upper()} DIED", True, Cores.MORREU.value)
                    janela.blit(texto_morte, (60, 650))
                else:
                    texto_vida_inimigo = fonte.render(f"{self.inimigos[posicao_seta_menu].nome.upper()}'S NEW HP: {self.inimigos[posicao_seta_menu].vida_atual}/{self.inimigos[posicao_seta_menu].vida_total}", True, Cores.TEXTO_PADRAO.value)
                    janela.blit(texto_vida_inimigo, (60, 650))
            else: # Se quem atacou é inimigo 
                fonte = pygame.font.Font(None, 45)
                texto_dano = fonte.render(f"{personagem.nome.upper()} INFLICTED {personagem.ultimo_dano_causado}", True, Cores.VIDA_INIMIGO.value)
                janela.blit(texto_dano, (60, 580))
                texto_dano = fonte.render(f"DAMAGE TO THE {self.aliados[self.ultimo_aliado_atacado].nome.upper()}!", True, Cores.VIDA_INIMIGO.value)
                janela.blit(texto_dano, (60, 630))
                if self.aliados[self.ultimo_aliado_atacado].morreu():
                    texto_morte = fonte.render(f"{self.aliados[self.ultimo_aliado_atacado].nome.upper()} DIED", True, Cores.MORREU.value)
                    janela.blit(texto_morte, (60, 680))
        elif estado_batalha == 'mostrando_defesa':
            # Desenha a defesa
            fonte = pygame.font.Font(None, 45)
            texto_defesa = fonte.render(f"{personagem.nome.upper()} IS DEFENDING!", True, Cores.BUFF_DEFESA.value)
            janela.blit(texto_defesa, (60, 600))
            texto_def = fonte.render("NEW DEF: ", True, Cores.DEFESA.value)
            janela.blit(texto_def, (60, 670))
            texto_defesa_inimigo = fonte.render(f"{personagem.defesa_atual}", True, Cores.BUFF_DEFESA.value)
            janela.blit(texto_defesa_inimigo, (220, 670))


    def efetua_ataque(self, posicao_seta_menu):
        personagem = self.ordem_personagens[self.personagem_atual]
        personagem.atacar(self.inimigos[posicao_seta_menu])
        if self.inimigos[posicao_seta_menu].morreu():
            self.inimigos_mortos += 1

    def efetua_defesa(self):
        personagem = self.ordem_personagens[self.personagem_atual]
        personagem.defender()

    def realiza_acao_do_inimigo(self):
        inimigo = self.ordem_personagens[self.personagem_atual]
        alvo = None
        while alvo == None or alvo.morreu():
            alvo = random.choice(self.aliados)
        if random.random() < 0.7:
            inimigo.atacar(alvo)
            if alvo.morreu():
                self.aliados_mortos += 1
            self.ultimo_aliado_atacado = self.aliados.index(alvo)
            return 'ataque'
        else:
            inimigo.defender()
            return 'defesa'

    def esta_morto(self, posicao_seta_menu):
        return self.inimigos[posicao_seta_menu].morreu()
    
    def verifica_fim_batalha(self):
        if self.aliados_mortos == len(self.aliados):
            return 'derrota'
        elif self.inimigos_mortos == len(self.inimigos):
            return 'vitoria'
        return 'continua'