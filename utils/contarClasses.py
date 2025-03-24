class contarClasses:
    def __init__(self):
        """
        Inicializa o detector de velocidade e a contagem de veículos.
        """
        # Dicionário para armazenar obj_id e nomeObjeto
        self.veiculos_detectados = {}

        # Dicionário para armazenar a contagem de cada classe
        self.contagem_classes = {
            "Carro": 0,
            "Moto": 0,
            "Caminhao": 0
        }

    def processar_deteccao(self, result):
        """
        Processa uma detecção e armazena o obj_id e nomeObjeto se não estiverem no dicionário.

        Parâmetros:
            result (np.array): Uma linha de detecção no formato [x1, y1, x2, y2, obj_id, con, nomeObjeto].
        """
        if len(result) == 5:
            x1, y1, x2, y2, obj_id = result
            nomeObjeto = None
        elif len(result) == 7:
            x1, y1, x2, y2, obj_id, con, nomeObjeto = result
        else:
            raise ValueError("Formato de 'result' não reconhecido.")

        # Verifica se o obj_id já foi processado
        if obj_id not in self.veiculos_detectados:
            self.veiculos_detectados[obj_id] = nomeObjeto  # Armazena o obj_id e nomeObjeto

    def contar_veiculos(self):
        """
        Conta quantos veículos de cada tipo foram detectados.
        """
        # Reinicia a contagem
        self.contagem_classes = {
            "Carro": 0,
            "Moto": 0,
            "Caminhao": 0
        }

        # Conta os veículos com base no nomeObjeto armazenado
        for nomeObjeto in self.veiculos_detectados.values():
            if nomeObjeto == 1:
                self.contagem_classes["Carro"] += 1
            elif nomeObjeto == 2:
                self.contagem_classes["Moto"] += 1
            elif nomeObjeto == 0:
                self.contagem_classes["Caminhao"] += 1

    def obter_contagem(self):
        """
        Retorna a contagem de veículos detectados.

        Retorno:
            dict: Um dicionário com a contagem de cada classe de veículo.
        """
        return self.contagem_classes
    
class ContadorVeiculos:
    def __init__(self, linhaA, linhaB):
        """
        Inicializa a classe com as coordenadas das linhas A e B.
        :param linhaA: Coordenadas da linha A (x1, y, x2).
        :param linhaB: Coordenadas da linha B (y1, x, y2).
        """
        self.linhaA = linhaA
        self.linhaB = linhaB
        self.contadorA = []  # Lista para armazenar IDs que cruzaram a linha A
        self.contadorB = []  # Lista para armazenar IDs que cruzaram a linha B

    def verificar_cruzamento_linhaA(self, cx, cy, obj_id):
        """
        Verifica se o objeto cruzou a linha A e atualiza o contador.
        :param cx: Coordenada x do centro do objeto.
        :param cy: Coordenada y do centro do objeto.
        :param obj_id: ID do objeto.
        :return: Nenhum.
        """
        if self.linhaA[0] < cx < self.linhaA[2] and self.linhaA[1] - 15 < cy < self.linhaA[1] + 15:
            if obj_id not in self.contadorA:
                self.contadorA.append(obj_id)

    def verificar_cruzamento_linhaB(self, cx, cy, obj_id):
        """
        Verifica se o objeto cruzou a linha B e atualiza o contador.
        :param cx: Coordenada x do centro do objeto.
        :param cy: Coordenada y do centro do objeto.
        :param obj_id: ID do objeto.
        :return: Nenhum.
        """
        if self.linhaB[1] - 15 < cx < self.linhaB[1] + 15 and self.linhaB[0] < cy < self.linhaB[2]:
            if obj_id not in self.contadorB:
                self.contadorB.append(obj_id)

    def get_contadorA(self):
        """
        Retorna a lista de IDs que cruzaram a linha A.
        :return: Lista de IDs.
        """
        return self.contadorA

    def get_contadorB(self):
        """
        Retorna a lista de IDs que cruzaram a linha B.
        :return: Lista de IDs.
        """
        return self.contadorB