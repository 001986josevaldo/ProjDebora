import cv2
from ultralytics import YOLO
from utils.sort import *
from utils.velocidadeDetector import *
from utils.contarClasses import *
from utils.monitoramentoVeiculo import MonitoramentoVeiculo
import cvzone
import time
from collections import defaultdict

# Dicionário para contar as classes detectadas
contador_classes = defaultdict(int)
# Lista para armazenar as detecções
detecoes = []
#import numpy as np
# Criando uma instância da classe
detector_velocidade = VelocidadeDetector()

# Cria uma instância do contador
contador = contarClasses()

# Criando o objeto PETCalculator
#pet_calc = PETCalculator(ponto_x=150)

# Inicializa a classe
monitor = MonitoramentoVeiculo()

# Carrega o modelo YOLO
model = YOLO("modelos/trafego.pt")
tracker = Sort(max_age=60, min_hits=1)  # Rastreador

# Carrega o vídeo
video = cv2.VideoCapture('videos/trafego2.mp4')
#video = cv2.VideoCapture('videos/lionsOtavioPitaluga.mp4')
# ----------------------------------------------------------------------
# Configuração do nome e formato do arquivo de saída
conflitosdetransito = 'saida.mp4'
# Definir o codec e criar o objeto VideoWriter
# Use 'mp4v' para o formato MP4
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 30  # Frames por segundo
frame_size = (840, 472)  # Dimensão do vídeo

# Criando o objeto VideoWriter
out = cv2.VideoWriter(conflitosdetransito, fourcc, fps,frame_size)
# -----------------------------------------------------------------------
# Classes de veículos
classNames = ["caminhao", "carro", "moto",]

# Redimensiona o frame para uma largura fixa (ex: 840px), mantendo a proporção
def redimensionar_frame(frame, largura=840):
    altura = int(frame.shape[0] * (largura / frame.shape[1]))
    frame = cv2.resize(frame, (largura, altura))
    #print(largura, altura )
    return frame

# Função para verificar se um veículo está na área de risco
def veiculo_na_area_risco(x1, y1):
    return rect_x1 <= x1 <= rect_x2 and rect_y1 <= y1 <= rect_y2

# Coordenadas do retângulo de contagem
rect_x1, rect_y1 = 270, 300
rect_x2, rect_y2 = 330, 350

crArray =[]
total_objetos = 0  # Variável para contar o total de objetos

    # Variável de controle para armazenar a posição anterior
x2anterior = None  
tempo_anterior = None  # Inicializa o tempo anterior fora do loop principal

# Definição da linha A e B para contegem de entrada dos veiculos
linhaA = (250, 60, 360)
linhaB = (220, 50, 330)  # Definição da linha B (y1, x, y2)
# Criando uma instância da classe
contadorEntradas = ContadorVeiculos(linhaA, linhaB)
tempo_entrada = None  # Armazena o tempo de entrada do último veículo
ultimo_veiculo_id = None  # Armazena o último veículo que iniciou a contagem
contador_tempo = 0    # Contador de tempo decorrido
tempo_entrada_por_veiculo = {}  # Dicionário para armazenar tempos de entrada por obj_id

while True:
    _, img = video.read()
    if img is None:
        print("Erro: Não foi possível abrir o vídeo ou o vídeo chegou ao fim.")
        break
    
    # Redimensiona o frame
    img = redimensionar_frame(img)
    #print(img.shape[:2])  # Exibe (altura, largura)
    # Desenha o retângulo de contagem na imagem
    #cv2.rectangle(img, (rect_x1, rect_y1), (rect_x2, rect_y2), (255, 255, 255), 1)
    
    # Inicializa a contagem de veículos dentro do retângulo
    contagem_veiculos = 0
    
    # Linha 
    xlinha1 = 85
    xlinha2 = xlinha1 + 100
    y1 = 250
    y2 = y1 + 100
    #cv2.line(img, (xlinha1, y1), (xlinha1, y2), (0, 255, 0), 2)
    #cv2.line(img, (xlinha2, y1), (xlinha2, y2), (0, 255, 0), 2)

    # Linha 
    ylinha1 = 150
    ylinha2 = ylinha1 + 100
    x1 = 200
    x2 = x1 + 100
    #cv2.line(img, (x1, ylinha1), (x2, ylinha1), (0, 0, 255), 2)
    #cv2.line(img, (x1, ylinha2), (x2, ylinha2), (0, 0, 255), 2)

    # Detecta veículos
    results = model(img, stream=True)
    detections = np.empty((0,7))
    #print("detections", results)

    # Inicializa o dicionário para mapear IDs às classes
    id_to_class = {}
    classes = []
    ids = []
    # itera sopbre todos os objetos detectados

    cv2.line(img, (185, 250), (185, 350), (0, 255, 0), 2)

    for obj in results:
        dados = obj.boxes
        for x in dados:
            #conf
            conf = int(x.conf[0]*100)
            cls = int(x.cls[0])
            #print("cls-=> ",cls)
            nomeClass = classNames[cls]
            #print(nomeClass)
            
            # Verifica classes desejadas
            if  nomeClass in ["carro", "moto", "caminhao"]:
                # Atualiza a contagem da classe
                contador_classes[nomeClass] += 1
                classes.append(nomeClass)
                # Coordenadas do bounding box
                x1, y1, x2, y2 = x.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                # Calcula o centro do bounding box
                cx, cy = x1 + w // 2, y1 + h // 2  

                # Adiciona a detecção ao tracker
                crArray = np.array([x1, y1, x2, y2, 0, conf, cls])
                detections = np.vstack((detections,crArray))

                # logica dos veiculos na area de risco
                if rect_x1 <= x1 <= rect_x2 and rect_y1 <= y1 <= rect_y2:
                    contagem_veiculos += 1

    #print("classes: ",classes)
        # Exibir a contagem das classes            
    #print(detections)
    resultTracker = tracker.update2(detections)
    '''    
    # Processa cada resultado
    for result in resultTracker:
        contador.processar_deteccao(result)    
    contador.contar_veiculos()
    # Obtém a contagem total de veículos
    contagem = contador.obter_contagem()
    print("Contagem total de veículos detectados:", contagem)
    '''
    #print("")
    #print(resultTracker)
    tempo1 = time.time()
    # Exibe os resultados corrigidos
    for result in resultTracker:
        num_colunas = result.shape[0]
        if len(result) == 5:
            x1, y1, x2, y2, obj_id = result
            con = None  # Valor padrão para `con`
            nomeObjeto = None  # Valor padrão para `resto`
        elif len(result) == 7:
            x1, y1, x2, y2, obj_id, con, nomeObjeto = result
        else:
            raise ValueError("Formato de 'result' não reconhecido.")
        # Converte as coordenadas para inteiros
        x1, y1, x2, y2 = (int(x1)), int(y1), (int(x2)), int(y2)
        w, h = x2 - x1, y2 - y1 # Largura e altura do objeto
        cx,cy = x1+w//2, y1+h//2 # Centro do objeto

            # Chama o método para verificar se cruzou a linha A ou B
            # contagem dos veiculos por classes
        if nomeObjeto is not None:  # Evita chamar o método se `nomeObjeto` for None
            contadorEntradas.verificar_cruzamento_linha_id_obj(cx, cy, obj_id, nomeObjeto)

        # Chama o método para atualizar o tempo que o veículo passou na area de risco PET 
        monitor.atualizar_tempo_veiculo(obj_id, x1, y1, img, veiculo_na_area_risco)

        # exibir id na imagem
        #cv2.putText(img, str(obj_id), (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1)
        ids.append(obj_id)
        mapeamento_nomes = {
        0: "Caminhao",
        1: "Carro",
        2: "Moto"
        }
        nome_str = mapeamento_nomes.get(nomeObjeto, "Desconhecido")  # Retorna "Desconhecido" se o valor não estiver no dicionário

        posicao_inicial = [x2,(y1-20)]
        vel = detector_velocidade.calcular_velocidade(x2,y2, obj_id)

        #print(f"ID {obj_id} - Velocidade: {vel} Km/h")
        #cv2.putText(img, nomeClass, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1)
        
        dados = [
            f"Classe: {nome_str}",
            f"Conf.: {con}%",
            f"ID: {obj_id}",
            f'Vel: {vel}'
        ]
        img = detector_velocidade.exibir_texto_na_imagem(img, dados,posicao_inicial,)

        # ---------------------- CONTAGEM DOS VEICULOS QUE ENTRAM NO CENARIO PELA ENTRADA A E ENTRADA B ----------------
        contadorA = contadorEntradas.verificar_cruzamento_linhaA(cx, cy, obj_id)
        contadorB = contadorEntradas.verificar_cruzamento_linhaB(cx, cy, obj_id)               



    #detector_velocidade.contar_classes(ids, classes) # Conta os objetos detectados
    coordenadas = [(cx,cy)]
    '''
    # Loop para processar cada objeto
    for obj_id, classe, (cx, cy) in zip(ids, classes, coordenadas):
        # Verificar cruzamentos
        contadorEntradas.verificar_cruzamento_linhaA(cx, cy, obj_id)
        contadorEntradas.verificar_cruzamento_linhaB(cx, cy, obj_id)
        '''
        # Exibir informações
        #print(f"Classe: {classe} | ID: {obj_id} | Total: {len(contadorEntradas.get_contadorA()) + len(contadorEntradas.get_contadorB())}")

    # Exibe a contagem total de veículos
    total = len(contadorEntradas.get_contadorA())+ len(contadorEntradas.get_contadorB())
    
    print(f"\nTotal Aprox. Veiculos: {total}")
    # Exibe a contagem final
    print("\nContagem final Aprox. de veículos:", contadorEntradas.obter_contagem_final(),"\n")
    
    # Liberar a captura de vídeo    
        # -------------------------------------------------------------------------------------------------\
    if cv2.waitKey(1) == 27:
        break
    # Desenha o retângulo de contagem na imagem
    cv2.rectangle(img, (rect_x1, rect_y1), (rect_x2, rect_y2), (255, 255, 255), 1)
    # Exibe a contagem de veículos dentro do retângulo
    cv2.putText(img, f"Area de risco (PET): {contagem_veiculos}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1)
    cv2.putText(img, f"Entrada A: {len(contadorEntradas.get_contadorA())}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img, f"Entrada B: {len(contadorEntradas.get_contadorB())}", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,127 , 255), 2)
    
     # Desenhar a linha A
    cv2.line(img, (linhaA[0], linhaA[1]), (linhaA[2], linhaA[1]), (255, 0, 0), 2)

    # Desenhar a linha B
    cv2.line(img, (linhaB[1], linhaB[0]), (linhaB[1], linhaB[2]), (255, 0, 0), 2)

    # Escrever o frame no vídeo
    out.write(img)
    cv2.imshow('Conflitos de Trafego',img)
    # Salva a contagem final em um CSV
    contadorEntradas.salvar_contagem_csv("contagem_veiculos.csv")


# Fechar o vídeo e arquivo de texto
video.release()
out.release()
cv2.destroyAllWindows()
