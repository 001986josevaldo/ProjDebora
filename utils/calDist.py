


import cv2
import numpy as np

# Carrega a imagem
imagem = cv2.imread('E:/ProjetoDebora/codigos/Rotatoria.jpeg')


   # linha verde   
x1_v = 85 # primeira linha
x2_v = x1_v + 100 # segunda linha
y1_v = 250 # inicio da linha 
y2_v = y1_v + 100  # final da linha
# Coordenadas manuais das linhas (substitua pelos valores exatos após verificação)
linha_verde1_inicio = (x1_v, y1_v)  # Coordenada inicial da linha verde
linha_verde1_fim = (x2_v, y2_v)     # Coordenada final da linha verde

x1_v2 = x2_v


'''linha_verde2_inicio = (x1_v2, y1_v2)
linha_verde2_fim = (x2_v2, y2_v2)'''

    # linha vermelha 
y1_r = 150
y2_r = y1_r + 100
x1_r = 200
x2_r = x1_r + 100
linha_vermelha1_inicio = (x1_r, y1_r)  # Coordenada inicial da linha vermelha
linha_vermelha1_fim = (x2_r, y2_r)     # Coordenada final da linha vermelha

'''linha_vermelha2_inicio = (x1_r2, y1_r2)
linha_vermelha2_fim = (x2_r2, y2_r2)'''

# Função para calcular a distância entre dois pontos
def calcular_distancia(ponto2, ponto1):
    return (ponto2 - ponto1)

# Redimensiona o frame para uma largura fixa (ex: 640px), mantendo a proporção
def redimensionar_frame(frame, largura=840):
    altura = int(frame.shape[0] * (largura / frame.shape[1]))
    frame = cv2.resize(frame, (largura, altura))
    return frame

'''# Calcula a distância entre as linhas (neste exemplo, entre os pontos médios das linhas)
ponto_medio_verde = ((linha_verde_inicio[0] + linha_verde_fim[0]) // 2, (linha_verde_inicio[1] + linha_verde_fim[1]) // 2)
ponto_medio_vermelha = ((linha_vermelha_inicio[0] + linha_vermelha_fim[0]) // 2, (linha_vermelha_inicio[1] + linha_vermelha_fim[1]) // 2)
'''
imagem = redimensionar_frame(imagem)

distancia_pixels = calcular_distancia(x2_v, x1_v)

# Exibe a distância calculada
print(f"A distância entre as linhas em pixels é: {distancia_pixels:.2f}")

# Desenha os pontos médios e as linhas entre eles para visualização
cv2.circle(imagem, (x2_v, x2_v), 5, (0, 255, 0), -1)
cv2.circle(imagem, (x2_v, x1_v), 5, (0, 0, 255), -1)
cv2.line(imagem, (x2_v, y1_v),(x2_v, x1_v), (255, 0, 0), 2)

# Mostra a imagem com as linhas e pontos médios
cv2.imshow("Imagem com Distância entre Linhas", imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()