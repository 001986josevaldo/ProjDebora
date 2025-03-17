import cv2
from ultralytics import YOLO
from utils.sort import *
import cvzone
import time
#import numpy as np

# Carrega o modelo YOLO
model = YOLO("modelos/trafego.pt")
tracker = Sort(max_age=30)  # Rastreador

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

# Coordenadas do retângulo de contagem
rect_x1, rect_y1 = 185, 250
rect_x2, rect_y2 = 330, 380



    # Inicializa a lista de IDs dos contadores
contadorA = []
contadorB = []
total_objetos = 0  # Variável para contar o total de objetos

    # Variável de controle para armazenar a posição anterior
x2anterior = None  
tempo_anterior = None  # Inicializa o tempo anterior fora do loop principal

# Redimensiona o frame
#video = redimensionar_frame(video)

while True:
    _, img = video.read()
    if img is None:
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
    detections = np.empty((0,5))
  
    print("detections", results)
    # itera sopbre todos os objetos detectados
    for obj in results:
        dados = obj.boxes
        for x in dados:
            #conf
            conf = int(x.conf[0]*100)
            cls = int(x.cls[0])
            nomeClass = classNames[cls]

            if conf >= 50 and nomeClass == "carro" or nomeClass=="moto" or nomeClass=="caminhao":

                    # Coordenadas do bounding box
                x1, y1, x2, y2 = x.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                # Calcula o centro do bounding box
                cx, cy = x1 + w // 2, y1 + h // 2  
                #classe
                
                # cvzone.cornerRect(img,(x1,y1,w,h),colorR=(255,0,255))
                #cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 1)# desenha o retangulo nos objettos
                #cvzone.putTextRect(img,nomeClass,(x1,y1-10),scale=1,thickness=1)
                
                cv2.putText(img, nomeClass, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1)
                
                crArray = np.array([x1,y1,x2,y2,conf])
                detections = np.vstack((detections,crArray))

                # logica dos veiculos na area de risco
                if rect_x1 <= x1 <= rect_x2 and rect_y1 <= y1 <= rect_y2:
                    contagem_veiculos += 1

               
                


    resultTracker = tracker.update(detections)

    print("resulttracker: ", resultTracker)

    for result in resultTracker:
        x1,y1,x2,y2,id = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        w, h = x2 - x1, y2 - y1
        cx,cy = x1+w//2, y1+h//2 # meio dos objetos
        
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 1)# desenha o retangulo nos objettos
        
        #cvzone.putTextRect(img,str(int(id)),(x1,y1-10),scale=1,thickness=1)
        
        #for id:
        print("----------------------------\n","Classe: ", nomeClass ,"| id: ", id, "| Total ",len(contadorB)+len(contadorA))

        # logica da velocidade pela entrada B
        if 85 <= x2 <= 185 and 250 <= y1 <= 380:
            #print(f"ID: {id}, Posição x2: {x2}")

           
            if x2anterior is None:
                x2anterior = x2  # Inicializa a posição anterior
                tempo_anterior = time.time()  # Captura o tempo inicial
                print("Inicializando x2 anterior e tempo_anterior")


            if x2 != x2anterior:
                # Calcula a diferença de posição (delta_x2)
                #print(x2, x2anterior, x2 - x2anterior)
                deltax2 = x2 - x2anterior
            
                # Captura o tempo atual e calcula o tempo decorrido
                tempo_atual = time.time()
                delta_tempo = tempo_atual - tempo_anterior
            
            #    Calcula a velocidade (metros por segundo e km/h)
                if delta_tempo > 0:  # Evita divisão por zero
                    velocidade_m_s = (deltax2 * 5.12 / 53) / delta_tempo  # Conversão de pixels para metros
                    velocidade_km_h = velocidade_m_s * 3.6
                
                    #print(f"Velocidade do objeto {id}: {velocidade_m_s:.3f} m/s ({velocidade_km_h:.3f} km/h)")
                    #cvzone.putTextRect(img, f"{int(velocidade_km_h)} Km/h", (x2 + 10, y1 + 10), scale=1, thickness=1) # exibe a velocidade
                    # Desenha o texto diretamente na imagem sem a caixa ao redor
                    if velocidade_km_h > 0 and velocidade_km_h < 100:
                        cv2.putText(img, f"{int(velocidade_km_h)} Km/h", (x2 + 10, y1 + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1)
                # Atualiza o tempo e a posição anteriores
                    tempo_anterior = tempo_atual
                    x2anterior = x2

# ---------------------- CONTAGEM DOS VEICULOS QUE ENTRAM NO CENARIO ENTYRADA A feita pelo id ----------------
                # Definição da linha A
        linhaA = (250, 60, 360)
                # Definição da linha de cima 
                #cv2.line(img, (linhaB[0], linhaB[1]), (linhaB[2], linhaB[1]), (255, 255, 255), 2)
                # Verificar se o centro do objeto cruzou a linha B
        if linhaA[0] < cx < linhaA[2] and linhaA[1] -15 < cy < linhaA[1] + 15:
            if contadorA.count(id) == 0:
                contadorA.append(id)
                        #cv2.line(img, (linha[0], linha[1]), (linha[2], linha[3]), (0, 255, 0), 5)
# ------------------------------------------------------------------------------------------------
# ---------------------- CONTAGEM DOS VEICULOS QUE ENTRAM NO CENARIO ENTRADA B feita pelo id ----------------
                # Definição da linha B
        linhaB = ( 220, 50, 330)# (Y1, X, Y2)
                 #cv2.line(img, (linhaB[1], linhaB[0]), (linhaB[1], linhaB[2]), (255, 255, 255), 2)
                # Verificar se o centro do objeto cruzou a linha B
        if linhaB[1] - 15 < cx < linhaB[1] + 15 and linhaB[0] < cy < linhaB[2]:
            if contadorB.count(id) == 0:
                contadorB.append(id)
# -------------------------------------------------------------------------------------------------\
    if cv2.waitKey(1) == 27:
        break
    # Desenha o retângulo de contagem na imagem
    cv2.rectangle(img, (rect_x1, rect_y1), (rect_x2, rect_y2), (255, 255, 255), 1)
    # Exibe a contagem de veículos dentro do retângulo
    cv2.putText(img, f"Veiculos na area de risco: {contagem_veiculos}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1)
    cv2.putText(img, f"Entrada A: {len(contadorA)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img, f"Entrada B: {len(contadorB)}", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,127 , 255), 2)

    

    # Escrever o frame no vídeo
    out.write(img)
    #cvzone.putTextRect(img, str(f'Entrada A: - {len(contadorb)}'), (25, 50), scale=0.5, thickness=1)
    #img = redimensionar_frame(img)
    cv2.imshow('Conflitos de Trafego',img)
    


# Fechar o vídeo e arquivo de texto
video.release()
out.release()
cv2.destroyAllWindows()








#        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 1)# desenha o retangulo nos objettos
        
        




        #cx,cy = x1+w//2, y1+h//2
        # circulo do centro das detecçoes
        #cv2.circle(img,(cx,cy),2,(255,0,255),1)
        
        





