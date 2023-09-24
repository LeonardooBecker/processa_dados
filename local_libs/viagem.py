"""

    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Última atualização: 24/09/2023
    Link para o repositório: https://github.com/LeonardooBecker/processa_dados

"""

from local_libs import constants as ct

# Classe utilizada para separar as viagens de cada card
class Viagem:
    def __init__(self, nome, index, categoria, elementos=None):
        self.nome = nome
        self.index = index
        self.categoria = categoria
        self.elementos = elementos

    def printViagem(self):
        print(f'Nome: {self.nome}')
        print(f'Index: {self.index}')
        print(f'Categoria: {self.categoria}')
        print(f'Elementos: {self.elementos}')

# Função que converte o timestamp do GPS para dias
def converteDias(texto):
    data = int(texto)
    anos = int(data/10000)
    meses = int((data % 10000)/100)
    dias = int(data % 100)
    return anos*365+meses*30+dias

# Função que converte o timestamp do GPS para segundos
def converteNumero(texto):
    horas = int(int(texto)/10000)
    minutos = int(int(texto) % 10000/100)
    segundos = int(texto) % 100
    return horas*3600+minutos*60+segundos

# Função que verifica se dois vídeos são da mesma viagem
def ehMesmaViagem(videoAnterior, videoAtual):
    partsVideoAnterior = videoAnterior.split('-')
    partsVideoAtual = videoAtual.split('-')

    diasAnterior = converteDias(
        partsVideoAnterior[0][2:len(partsVideoAnterior[0])])
    segundosAnterior = converteNumero(partsVideoAnterior[1])
    diasAtual = converteDias(partsVideoAtual[0][2:len(partsVideoAtual[0])])
    segundosAtual = converteNumero(partsVideoAtual[1])

    if (diasAnterior == diasAtual and abs(segundosAtual-segundosAnterior) < 190 and abs(segundosAtual-segundosAnterior) > 170):
        return 1
    else:
        return 0

# Função que preenche as viagens de cada Card dentro do objeto Viagem
def preencheViagens(viagensTotais, categoria, index):
    vetorViagens = []
    viagem = []
    viagensTotais = sorted(viagensTotais)
    viagem.append(viagensTotais[0])
    for i in range(len(viagensTotais)):
        if (i > 0):
            if (ehMesmaViagem(viagensTotais[i-1], viagensTotais[i])):
                viagem.append(viagensTotais[i])
            else:
                # [2:17] - Apenas a região que contém o dia e o horário do vídeo
                objViagem = Viagem(viagem[0][2:17], index, categoria, viagem)
                if (len(objViagem.elementos) >= ct.quantidadeMinimaVideos):
                    vetorViagens.append(objViagem)
                    index += 1
                viagem = []
                viagem.append(viagensTotais[i])

    # [2:17] - Apenas a região que contém o dia e o horário do vídeo
    objViagem = Viagem(viagem[0][2:17], index, categoria, viagem)
    if (len(objViagem.elementos) >= ct.quantidadeMinimaVideos):
        vetorViagens.append(objViagem)
        index += 1

    return vetorViagens
