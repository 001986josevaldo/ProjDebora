import cv2
import os

# Nome do arquivo de vídeo
#video_path = 'video.mp4'  # Substitua pelo caminho do seu vídeo
video_path = 'videos/caminhao2.mp4'
# Número de imagens desejadas
num_images = 50


# Nome da pasta para salvar as imagens
output_folder = 'framesCaminhao'

# Cria a pasta se ela não existir
os.makedirs(output_folder, exist_ok=True)

# Carrega o vídeo
cap = cv2.VideoCapture(video_path)

# Verifica se o vídeo foi carregado com sucesso
if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

# Duração total em quadros e taxa de quadros do vídeo
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Calcula o intervalo de quadros para capturar 200 imagens igualmente espaçadas
frame_interval = total_frames // num_images

# Inicializa o contador de imagens salvas
saved_images = 0

def redimensionar_frame(frame, largura=840):
    altura = int(frame.shape[0] * (largura / frame.shape[1]))
    frame = cv2.resize(frame, (largura, altura))
    return frame

# Loop para capturar e salvar as imagens
for i in range(num_images):
    # Calcula o índice do quadro a ser capturado
    frame_id = i * frame_interval
    
    # Define o quadro do vídeo
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
    
    # Lê o quadro
    ret, frame = cap.read()
    frame = redimensionar_frame(frame)
    # Verifica se o quadro foi lido com sucesso
    if not ret:
        print(f"Não foi possível ler o quadro {frame_id}.")
        continue

    # Define o nome do arquivo da imagem
    image_path = os.path.join(output_folder, f"frame_{i+33}.jpg")
    
    # Salva a imagem
    cv2.imwrite(image_path, frame)
    saved_images += 1
    print(f"Imagem {i+1} salva em: {image_path}")

# Libera o vídeo
cap.release()
print(f"Total de imagens salvas: {saved_images}")
print("Processo concluído.")