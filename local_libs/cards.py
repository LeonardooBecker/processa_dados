import os
import sys
import fnmatch

class Cards:
    def __init__(self, nomeCard, diretorio, diretorioBack, diretorioFront, diretorioGps, videosBack=None, videosFront=None):
        self.nomeCard = nomeCard
        self.diretorio = diretorio
        self.diretorioBack = diretorioBack
        self.diretorioFront = diretorioFront
        self.diretorioGps = diretorioGps
        self.videosBack = videosBack
        self.videosFront = videosFront

    def printParametros(self):
        print(f'Nome da pasta: {self.nomeCard}')
        print(f'Diretorio: {self.diretorio}')
        print(f'Diretorio Back: {self.diretorioBack}')
        print(f'Diretorio Front: {self.diretorioFront}')
        print(f'Diretorio GPS: {self.diretorioGps}')
        print(f'Quantidade de videos pasta Back: {len(self.videosBack)}')
        print(f'Quantidade de videos pasta Front: {len(self.videosFront)}')
        print()


# Função que verifica se as informações obtidas são válidas
def validaInformacoes(nomePasta, diretorioBack, diretorioFront, diretorioGps):
    valido = 1
    if(diretorioBack==None):
        print(f'Erro ao criar objeto {nomePasta} - Diretorio Back não encontrado')
        valido = 0
    if(diretorioFront==None):
        print(f'Erro ao criar objeto {nomePasta} - Diretorio Front não encontrado')
        valido = 0
    if(diretorioGps==None):
        print(f'Erro ao criar objeto {nomePasta} - Arquivo GPS não encontrado')
        valido = 0
    return valido

# Função que preenche os objetos Cards com as informações obtidas
def obtemCards(diretorio):
    pastas = os.listdir(diretorio)
    pastas=sorted(pastas)
    elementos=[]
    for nomePasta in pastas:
        if not os.path.isfile(nomePasta):
            if "card".lower() in nomePasta.lower():    
                diretorioBack=None
                diretorioFront=None
                diretorioGPS=None
                
                diretorioPasta=f'{diretorio}/{nomePasta}'
                conteudoPasta=os.listdir(diretorioPasta)
                for elemento in conteudoPasta:
                    if("Back" in elemento or "back" in elemento):
                        diretorioBack=f'{diretorioPasta}/{elemento}'
                    elif("Front" in elemento or "front" in elemento):
                        diretorioFront=f'{diretorioPasta}/{elemento}'
                        
                    # Inclusão biblioteca fnmatch para poder utilizar o ( * ) como um caractere coringa
                    elif(fnmatch.fnmatch(elemento, '*GPS*.txt') or fnmatch.fnmatch(elemento, '*gps*.txt')):
                        diretorioGPS=f'{diretorioPasta}/{elemento}'


                if(validaInformacoes(nomePasta,diretorioBack,diretorioFront,diretorioGPS)):
                    # Obtem os videos de cada pasta
                    videosBack=os.listdir(diretorioBack)
                    videosFront=os.listdir(diretorioFront)
                    # Preenche o objeto card com as informações obtidas - Objeto principal de trabalho
                    cardAtual = Cards(nomePasta,diretorioPasta,diretorioBack,diretorioFront,diretorioGPS,videosBack,videosFront)   
                else:
                    sys.exit()
                                            
                elementos.append(cardAtual)

    return elementos    