while True:
    # Lê um frame do vídeo
    ret, img = video.read()

    # Verifica se o vídeo foi aberto corretamente ou chegou ao fim
    if not ret or img is None:
        print("Erro: Não foi possível abrir o vídeo ou o vídeo chegou ao fim.")
        break

    # Redimensiona o frame
    img = redimensionar_frame(img)

    # Inicializa a contagem de veículos dentro do retângulo
    contagem_veiculos = 0

    # Define as linhas de contagem
    xlinha1, xlinha2, y1, y2 = 85, 185, 250, 350
    ylinha1, ylinha2, x1, x2 = 150, 250, 200, 300

    # Detecta veículos no frame
    results = model(img, stream=True)
    detections = np.empty((0, 5))

    # Dicionário para armazenar a classe associada a cada ID do rastreador
    id_to_class = {}

    # Itera sobre os objetos detectados
    for obj in results:
        dados = obj.boxes
        for x in dados:
            conf = int(x.conf[0] * 100)  # Confiança da detecção
            cls = int(x.cls[0])  # Índice da classe
            nomeClass = classNames[cls]  # Nome da classe

            # Filtra apenas os veículos desejados com confiança >= 50%
            if conf >= 50 and nomeClass in ["carro", "moto", "caminhao"]:
                x1, y1, x2, y2 = map(int, x.xyxy[0])  # Bounding box
                w, h = x2 - x1, y2 - y1
                cx, cy = x1 + w // 2, y1 + h // 2  # Centro do objeto

                # Adiciona a detecção ao rastreador
                crArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, crArray))

                # Verifica se o veículo está na área de risco
                if rect_x1 <= cx <= rect_x2 and rect_y1 <= cy <= rect_y2:
                    contagem_veiculos += 1

    # Verifica se há detecções antes de atualizar o rastreador
    if detections.shape[0] > 0:
        resultTracker = tracker.update(detections)

        # Associa cada ID à sua classe correspondente
        for i, result in enumerate(resultTracker):
            x1, y1, x2, y2, id = map(int, result)
            id_to_class[id] = nomeClass  # Salva o ID e a classe no dicionário

        print("resultTracker:", resultTracker)

        for result in resultTracker:
            x1, y1, x2, y2, id = map(int, result)
            w, h = x2 - x1, y2 - y1
            cx, cy = x1 + w // 2, y1 + h // 2  # Centro do objeto

            # Desenha o retângulo ao redor do objeto
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 1)

            # Obtém a classe associada ao ID (com segurança)
            nomeClass = id_to_class.get(id, "Desconhecido")

            # Exibe a classe e o ID corretamente
            print("----------------------------")
            print(f"Classe: {classes} | ID: {id} | Total: {len(contadorB) + len(contadorA)}")

