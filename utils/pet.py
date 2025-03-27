import time
#import random

class PETCalculator:
    def __init__(self, ponto_x):
        self.ponto_x = ponto_x  # Ponto de referência na via
        self.tempos = []  # Lista para armazenar os tempos de passagem
        self.pets = []  # Lista para armazenar os PETs calculados

    def registrar_passagem(self, x2):
        """
        Registra a passagem de um veículo pelo ponto_x e retorna o PET calculado.
        O registro só acontece se x2 estiver dentro da variação de ±5 do ponto_x.
        """
        if abs(x2 - self.ponto_x) <= 50:  # Verifica se x2 está dentro do intervalo permitido
            tempo_atual = time.time()
            self.tempos.append(tempo_atual)
            
            # Se houver pelo menos dois veículos registrados, calcular o PET
            if len(self.tempos) > 1:
                pet = self.tempos[-1] - self.tempos[-2]
                self.pets.append(pet)
                #print(f"Novo PET registrado: {pet:.2f} segundos")
                return pet
            return None  # Primeiro veículo não gera PET
        else:
            print(f"Veículo ignorado: x2={x2} está fora da faixa de {self.ponto_x}±5")
        return None

    def obter_pets(self):
        """ Retorna a lista de PETs calculados """
        return self.pets
    
'''
# Criando o objeto PETCalculator
pet_calc = PETCalculator(ponto_x=50)

# Simulação contínua de veículos passando pelo ponto X
print("Monitorando passagens de veículos...\nPressione CTRL+C para parar.")

try:
    while True:
        # Simula a passagem de um veículo em um intervalo aleatório de 2 a 6 segundos
        time.sleep(random.uniform(2, 6))
        pet_calc.registrar_passagem()
except KeyboardInterrupt:
    print("\nMonitoramento encerrado.")
    print("Lista de PETs registrados:", pet_calc.obter_pets())'''