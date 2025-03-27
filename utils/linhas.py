import cv2
# Inicializa o vídeo
video = cv2.VideoCapture('videos/trafego.mp4')
#video = cv2.VideoCapture('Rotatoria.jpeg')
# Verifica se o vídeo foi carregado corretamente
if not video.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

def marcar_linha_x(frame, y, x_inicial, x_final, cor=(0, 255, 0), espessura=2):
    altura, largura = frame.shape[:2]
    if x_final is None:
        x_final = largura
    cv2.line(frame, (x_inicial, y), (x_final, y), cor, espessura)
    return frame

def marcar_linha_y(frame, x, y_inicial, y_final, cor=(255, 0, 0), espessura=2):
    altura, largura = frame.shape[:2]
    if y_final is None:
        y_final = altura
    cv2.line(frame, (x, y_inicial), (x, y_final), cor, espessura)
    return frame

# Redimensiona o frame para uma largura fixa (ex: 640px), mantendo a proporção
def redimensionar_frame(frame, largura=840):
    altura = int(frame.shape[0] * (largura / frame.shape[1]))
    frame = cv2.resize(frame, (largura, altura))
    return frame

while True:
    ret, frame = video.read()

    if not ret:
        break

    frame = redimensionar_frame(frame)
                 
    # linha verde   
    xlinha1 = 85
    xlinha2 = xlinha1 + 100
    y1 = 250
    y2 = y1 + 100           # x, y inicial, x, y final
    frame = cv2.line(frame, (xlinha1,y1), (xlinha1, y2), (0, 255, 0),4)
    frame = cv2.line(frame, (xlinha2,y1), (xlinha2, y2), (0, 255, 0),4)

    # linha vermelha 
    ylinha1 = 150
    ylinha2 = ylinha1 + 100
    x1 = 200
    x2 = x1 + 100
    frame = cv2.line(frame, (x1,ylinha1), (x2, ylinha1), (0, 0, 255),4)
    frame = cv2.line(frame, (x1,ylinha2), (x2, ylinha2), (0, 0, 255),4)


    cv2.imshow('Video com Linhas de Referência', frame)
    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Libera o vídeo e fecha as janelas
video.release()
cv2.destroyAllWindows()