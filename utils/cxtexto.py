import cv2
import numpy as np
from ultralytics import YOLO
from sort import *

# Carrega o modelo YOLO
model = YOLO("modelos/trafego.pt")
# Classes de veículos
classNames = ["caminhao", "carro", "moto",]
tracker = Sort(max_age=30)  # Rastreador


def redimensionar_frame(frame, largura=840):
    altura = int(frame.shape[0] * (largura / frame.shape[1]))
    frame = cv2.resize(frame, (largura, altura))
    #print(largura, altura )
    return frame


def exibir_texto_na_imagem(img, textos, posicao_inicial, espacamento=10, fonte=cv2.FONT_HERSHEY_SIMPLEX, escala=0.3, cor=(255, 255, 255), espessura=1):
    """
    Exibe textos em uma lista vertical, com posições calculadas automaticamente.

    Parâmetros:
        img (numpy.ndarray): A imagem onde o texto será desenhado.
        textos (list): Lista de strings contendo os textos a serem exibidos.
        posicao_inicial (tuple): Tupla (x, y) com a posição inicial do primeiro texto.
        espacamento (int): Espaçamento vertical entre as linhas de texto (padrão é 30 pixels).
        fonte (int): Fonte do texto (padrão é cv2.FONT_HERSHEY_SIMPLEX).
        escala (float): Escala do texto (padrão é 0.7).
        cor (tuple): Cor do texto no formato BGR (padrão é branco (255, 255, 255)).
        espessura (int): Espessura do texto (padrão é 2).

    Retorna:
        numpy.ndarray: A imagem com os textos desenhados.
    """
    x, y = posicao_inicial  # Desempacota a posição inicial

    for texto in textos:
        # Desenha o texto na posição atual
        cv2.putText(img, texto, (x, y), fonte, escala, cor, espessura)
        # Atualiza a coordenada y para a próxima linha
        y += espacamento

    return img

# Exemplo de uso
if __name__ == "__main__":
    # Cria uma imagem preta (fundo)
    img = np.zeros((500, 500, 3), dtype=np.uint8)
    # Caminho da imagem
    caminho_imagem = r"E:/ProjetoDebora/codigos/imagens/Rotatoria.jpeg"
    # Carrega a imagem
    img = cv2.imread(caminho_imagem)
     # Redimensiona o frame
    img = redimensionar_frame(img)

    # Detecta veículos
    results = model(img, stream=True)
    detections = np.empty((0,5))


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
                '''
                    # Formata os textos
                texto = [
                    f"Classe: {nomeClass}",
                    f"Confiança: {conf}%"
                ]'''

                
                # Detalhes da detecção
                #exibir_texto_na_imagem(img, texto, posicao_inicial)

                crArray = np.array([x1,y1,x2,y2,conf])
                detections = np.vstack((detections,crArray))


    resultTracker = tracker.update(detections)
    for result in resultTracker:
        x1,y1,x2,y2,id = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        w, h = x2 - x1, y2 - y1
        cx,cy = x1+w//2, y1+h//2 # meio dos objetos

        posicao_inicial = (x2,y1)
        #adicionar id ao texto
        #chamar a função exibir texto
            # Formata os textos com o ID
        texto = [
            f"Classe: {nomeClass}",
            f"Conf.: {conf}%",
            f"ID: {id}"
        ]
        # Exibe os textos na imagem
        img = exibir_texto_na_imagem(img, texto, posicao_inicial)


    # Mostra a imagem
    cv2.imshow("Imagem com Texto", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()