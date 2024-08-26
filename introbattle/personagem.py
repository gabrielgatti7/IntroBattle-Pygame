class Personagem:
    def __init__(self, nome, vida, ataque, defesa, velocidade):
        self.nome = nome
        self.vida_total = vida
        self.vida_atual = vida
        self.ataque = ataque
        self.defesa = defesa
        self.defesa_atual = defesa
        self.velocidade = velocidade
        self.ultimo_dano_causado = 0

    def atacar(self, alvo):
        dano = round(self.ataque*(50/(50+alvo.defesa_atual)))
        alvo.tomar_dano(dano)
        self.ultimo_dano_causado = dano

    def defender(self):
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