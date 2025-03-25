import csv

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
        # ----------------------------------------------------------------
        self.contIdA = []
        self.contIdB = []
        self.contNomeA = []
        self.contNomeB = []
        self.contagem_veiculos = {"carro": 0, "moto": 0, "caminhao": 0}

        # Mapeamento dos números para os nomes dos veículos
        self.mapeamento_veiculos = {0: "caminhao", 1: "carro", 2: "moto"}

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

# ----------------------------------------------------------------
    def verificar_cruzamento_linha_id_obj(self, cx, cy, obj_id, nomeObjeto):
        """
        Verifica se o objeto cruza a linha A ou a linha B e contabiliza a passagem.
        
        if self.linhaB[1] - 15 < cx < self.linhaB[1] + 15 and self.linhaB[0] < cy < self.linhaB[2]:
            if obj_id not in self.contIdB:
                self.contIdB.append(obj_id)
                self.contNomeB.append(nomeObjeto)
                
                # Obtém o nome do veículo e incrementa a contagem
                nome_veiculo = self.mapeamento_veiculos.get(nomeObjeto, "desconhecido")
                if nome_veiculo in self.contagem_veiculos:
                    self.contagem_veiculos[nome_veiculo] += 1
        """
        nome_veiculo = self.mapeamento_veiculos.get(nomeObjeto, "desconhecido")
        
        # Verifica a passagem pela Linha A
        x1, y, x2 = self.linhaA
        if x1 <= cx <= x2 and (y - 15) <= cy <= (y + 15):
            if obj_id not in self.contIdA:
                self.contIdA.append(obj_id)
                if nome_veiculo in self.contagem_veiculos:
                    self.contagem_veiculos[nome_veiculo] += 1  # Soma à contagem

        # Verifica a passagem pela Linha B
        if self.linhaB[1] - 15 < cx < self.linhaB[1] + 15 and self.linhaB[0] < cy < self.linhaB[2]:
            if obj_id not in self.contIdB:
                self.contIdB.append(obj_id)
                if nome_veiculo in self.contagem_veiculos:
                    self.contagem_veiculos[nome_veiculo] += 1  # Soma à contagem

    def salvar_contagem_csv(self, arquivo="contagem_veiculos.csv"):
        """
        Salva a contagem final dos veículos em um arquivo CSV.
        :param arquivo: Nome do arquivo CSV onde os dados serão salvos.
        """
        # Obtendo a contagem final
        dados = self.contagem_veiculos
        # Definindo os cabeçalhos
        cabecalho = ["Tipo de Veiculo", "Quantidade"]
        
        # Abrindo o arquivo CSV para escrita
        with open(arquivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Escreve o cabeçalho
            writer.writerow(cabecalho)
            # Escreve os dados
            for veiculo, quantidade in dados.items():
                writer.writerow([veiculo, quantidade])
        
        print(f"Contagem salva no arquivo: {arquivo}")






    def obter_contagem_final(self):
        return self.contagem_veiculos
    
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
    
# ----------------------------------------------------------------
class ContadorVeiculos2:
    def __init__(self, linhaA, linhaB):
        """
        Inicializa a classe com as coordenadas das linhas A e B.
        :param linhaA: Coordenadas da linha A (x1, y, x2).
        :param linhaB: Coordenadas da linha B (y1, x, y2).
        """
        self.linhaA = linhaA
        self.linhaB = linhaB
        self.contadorA = {}  # Dicionário para armazenar tipos de veículos que cruzaram a linha A
        self.contadorB = {}  # Dicionário para armazenar tipos de veículos que cruzaram a linha B
        self.mapeamento = {0: "Caminhão", 1: "Carro", 2: "Moto"}  # Mapeamento de nomeObjeto

    def verificar_cruzamento_linhaA2(self, cx, cy, obj_id, nomeObjeto):
        """
        Verifica se o objeto cruzou a linha A e atualiza o contador.
        :param cx: Coordenada x do centro do objeto.
        :param cy: Coordenada y do centro do objeto.
        :param obj_id: ID do objeto.
        :param nomeObjeto: Categoria numérica do objeto (0, 1, 2).
        :return: Nenhum.
        """
        if self.linhaA[0] < cx < self.linhaA[2] and self.linhaA[1] - 15 < cy < self.linhaA[1] + 15:
            if obj_id not in self.contadorA:
                tipo_veiculo = self.mapeamento.get(nomeObjeto, "Desconhecido")
                if tipo_veiculo not in self.contadorA:
                    self.contadorA[tipo_veiculo] = 0
                self.contadorA[tipo_veiculo] += 1

    def verificar_cruzamento_linhaB2(self, cx, cy, obj_id, nomeObjeto):
        """
        Verifica se o objeto cruzou a linha B e atualiza o contador.
        :param cx: Coordenada x do centro do objeto.
        :param cy: Coordenada y do centro do objeto.
        :param obj_id: ID do objeto.
        :param nomeObjeto: Categoria numérica do objeto (0, 1, 2).
        :return: Nenhum.
        """
        if self.linhaB[1] - 15 < cx < self.linhaB[1] + 15 and self.linhaB[0] < cy < self.linhaB[2]:
            if obj_id not in self.contadorB:
                tipo_veiculo = self.mapeamento.get(nomeObjeto, "Desconhecido")
                if tipo_veiculo not in self.contadorB:
                    self.contadorB[tipo_veiculo] = 0
                self.contadorB[tipo_veiculo] += 1

    def get_contadorA2(self):
        """
        Retorna a contagem discriminada de tipos de veículos que cruzaram a linha A.
        :return: Dicionário com a contagem de tipos de veículos.
        """
        return self.contadorA

    def get_contadorB2(self):
        """
        Retorna a contagem discriminada de tipos de veículos que cruzaram a linha B.
        :return: Dicionário com a contagem de tipos de veículos.
        """
        return self.contadorB
