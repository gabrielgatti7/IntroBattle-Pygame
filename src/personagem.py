import random
import pygame

class Personagem:
    """
    Classe que representa um personagem do jogo.

    Atributos:
    - nome (str): O nome do personagem.
    - vida_total (int): A quantidade total de vida do personagem.
    - vida_atual (int): A quantidade atual de vida do personagem.
    - ataque (int): O valor do ataque do personagem.
    - defesa (int): O valor da defesa padrão do personagem.
    - defesa_atual (int): O valor atual da defesa do personagem.
    - velocidade (int): A velocidade do personagem.
    - ultimo_dano_causado (int): O último dano causado pelo personagem.
    - som_ataque (str): O caminho do arquivo de som do ataque do personagem.
    - som_dano_recebido (str): O caminho do arquivo de som do dano recebido pelo personagem.
    - som_defesa (str): O caminho do arquivo de som da defesa do personagem.

    Métodos:
    - atacar(alvo, critico=0): Realiza um ataque ao alvo, com chance de ser crítico de acordo
                            com o valor passado (Opcional, padrão = 0).
    - defender(): Define a defesa atual como o dobro do valor da defesa padrão.
    - tomar_dano(dano): Reduz a vida do personagem de acordo com o dano recebido.
    - esta_defendendo(): Verifica se o personagem está sob o efeito de defender.
    - morreu(): Verifica se o personagem está morto.
    - reseta_turno(): Reseta o valor da defesa atual do personagem.
    """

    def __init__(self, nome, vida, ataque, defesa, velocidade, som_path):
        self.nome = nome
        self.vida_total = vida
        self.vida_atual = vida
        self.ataque = ataque
        self.defesa = defesa
        self.defesa_atual = defesa
        self.velocidade = velocidade
        self.ultimo_dano_causado = 0
        self.som_ataque = som_path
        self.som_dano_recebido = 'media/sounds/video-game-hit-noise-001-135821.mp3'
        self.som_defesa = 'media/sounds/shield-block-shortsword-143940.mp3'

    def atacar(self, alvo, critico=0):
        if self.som_ataque != None:
            som_efeito = pygame.mixer.Sound(self.som_ataque)
            som_efeito.play()
        else:
            som_efeito = pygame.mixer.Sound(self.som_dano_recebido)
            som_efeito.play()
            som_efeito.set_volume(0.5)

        if random.random() < critico:
            dano = 100
        else:
            dano = round(self.ataque*(50/(50+alvo.defesa_atual)))
        alvo.tomar_dano(dano)
        self.ultimo_dano_causado = dano

    def defender(self):
        som_efeito = pygame.mixer.Sound(self.som_defesa)
        som_efeito.play()
        self.defesa_atual = self.defesa * 2

    def tomar_dano(self, dano):
        self.vida_atual -= dano

    def esta_defendendo(self):
        return self.defesa_atual > self.defesa

    def morreu(self):
        if(self.vida_atual <= 0):
            self.vida_atual = 0
            return True
        return False

    def reseta_turno(self):
        self.defesa_atual = self.defesa

    def __str__(self):
        return f'{self.nome} ({self.vida} vida, {self.ataque} ataque)'