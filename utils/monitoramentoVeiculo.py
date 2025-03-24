import time
import cv2

class MonitoramentoVeiculo:
    def __init__(self):
        self.tempo_entrada_por_veiculo = {}
        self.ultimo_veiculo_id = None
        self.contador_tempo = 0

    def atualizar_tempo_veiculo(self, obj_id, x1, y1, img, veiculo_na_area_risco):
        # Se o veículo entrou na área OU já teve sua contagem iniciada, continua
        if veiculo_na_area_risco(x1, y1) or obj_id in self.tempo_entrada_por_veiculo:
            tempo_atual = time.time()  # Captura o tempo atual

            if obj_id not in self.tempo_entrada_por_veiculo:
                # Se um novo veículo entrou, reinicia a contagem
                self.tempo_entrada_por_veiculo.clear()  # Limpa registros antigos
                self.tempo_entrada_por_veiculo[obj_id] = tempo_atual
                self.ultimo_veiculo_id = obj_id  # Atualiza o último veículo ativo
                self.contador_tempo = 0  # Reinicia o contador
                print(f"Veículo {obj_id} entrou na área. Iniciando nova contagem.")

            # Calcula o tempo decorrido para aquele veículo específico
            self.contador_tempo = tempo_atual - self.tempo_entrada_por_veiculo[obj_id]

            # Converte o tempo para minutos e segundos
            minutos = int(self.contador_tempo // 60)
            segundos = int(self.contador_tempo % 60)
            tempo_formatado = f"{minutos:02d}:{segundos:02d}"

            print(f"Veículo {obj_id} tempo total: {tempo_formatado} minutos.")

            # Exibe a contagem de tempo na imagem
            cv2.putText(img, f"PET = ID {obj_id} Tempo: {tempo_formatado}", (350, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)