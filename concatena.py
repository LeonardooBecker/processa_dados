"""

    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Última atualização: 23/09/2023
    Descrição: Painel de visualização dos dados do Estudo Naturalístico de Direção Brasileiro
    Link para o painel: https://painelndsbr.streamlit.app
    Link para o repositório: https://github.com/LeonardooBecker/streamlit

"""

import os
import sys
import os
import sqlite3

from local_libs import cards as cd
from local_libs import geraPlanilha as gp
from local_libs import utils
from local_libs import juntaVideo        as jv
from local_libs import viagem as vg
from local_libs import constants as ct
from local_libs import criaBanco


# Leitura dos cards e seus respectivos videos
totalCards=cd.obtemCards('./')

# Entrada do condutor por argumento
try:
    condutor=sys.argv[1]
    print("Condutor",condutor)
except: 
    print("Condutor não informado")
    sys.exit()            


limparBanco=1
indexInicial=1
# Para cada Card obtido na leitura inicial é necessário gerar os arquivos de GPS e os videos concatenados
for card in totalCards:
    try:
        with open(card.diretorioGps, 'r') as arquivo:
            conteudoGPS=arquivo.readlines()
        arquivo.close()
    except:
        print("Erro ao abrir arquivo GPS")
        sys.exit()
        
    # Criação e limpeza do diretorio GPS
    diretorioGPSConcatenado=f'{card.diretorio}/{ct.pastaArquivosGPS}'
    utils.limpaDiretorio(diretorioGPSConcatenado)
        
    viagensBack=None
    viagensFront=None
    viagensBack=vg.preencheViagens(card.videosBack,"Back",indexInicial)
    viagensFront=vg.preencheViagens(card.videosFront,"Front",indexInicial)    

    # Cria um banco contendo as informações de todos os cards ( formato arquivo txt )
    criaBanco.newBanco(conteudoGPS, card.nomeCard, limparBanco)
    limparBanco=0


    conexao = sqlite3.connect(ct.dataBaseAuxiliar)
    cursor = conexao.cursor()  
      
    # Para cada viagem contida no Card
    for i in range(len(viagensBack)):
        tabela=[]
                
        # Para cada video da viagem é necessário obter os dados do banco de dados
        for video in viagensBack[i].elementos:
            # QuerySQL
            consulta_sql=f"SELECT * FROM card_table WHERE GPS_FILE like '%{video}%' AND HOVER='A'"
            cursor.execute(consulta_sql)
            matriz=cursor.fetchall()
            
            # Junção de todos os vídeos de determinada viagem em uma única estrutura de dados
            tabela.extend(matriz)            
        
        # Correção da tabela de dados ( manter 1 segundo de diferença para cada linha )
        tabela=utils.corrigeTabela(tabela)
        try:
            nomeArquivoCSV=f'{diretorioGPSConcatenado}/Viagem{condutor}{indexInicial+i}-{gp.convert_unix_timestamp(tabela[0][0]).strftime("%Y%m%d-%H%M%S")}.csv'
        except:
            nomeArquivoCSV=f'{diretorioGPSConcatenado}/Viagem{condutor}{indexInicial+i}-{viagensBack[i].nome}.csv'
        with open(nomeArquivoCSV, 'w') as arquivoGPS:    
            # Com a tabela obtida e corrigida, é possível criar os arquivos CSV
            gp.preencheArquivoCSV(tabela,arquivoGPS,condutor,viagensBack[i].index)
        arquivoGPS.close()
    
    
    # Gera o arquivo CSV que contém os dados das viagens sem vídeo
    gp.geraSemVideoCSV(viagensBack,condutor,diretorioGPSConcatenado)
    
    # Criação e limpeza do diretorio de videos concatenados
    diretorioVideosConcatenados=f'{card.diretorio}/{ct.pastaVideosConcatenados}'
    utils.limpaDiretorio(diretorioVideosConcatenados)
    
    # Concatena os vídeos
    jv.concatenacao(viagensBack, card.diretorioBack, diretorioVideosConcatenados, condutor)
    jv.concatenacao(viagensFront, card.diretorioFront, diretorioVideosConcatenados, condutor)

    # Atualiza o indexInicial para o próximo Card, Card2 sequência do Card1 no número de viagem
    indexInicial=len(viagensBack)+1
    
    card.printParametros()