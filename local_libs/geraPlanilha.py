"""

    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Última atualização: 24/09/2023
    Link para o repositório: https://github.com/LeonardooBecker/processa_dados

"""

import datetime
import sqlite3
from local_libs import constants as ct
from local_libs import utils as utils

# Função que converte o timestamp em um objeto do tipo datetime
def convert_unix_timestamp(unix_timestamp):
    dt = datetime.datetime.fromtimestamp(unix_timestamp)
    return dt

# Função que converte o objeto datetime em segundos
def toSeconds(value):
    return value.hour*3600+value.minute*60+value.second

# Função que preenche o arquivo CSV
def preencheArquivoCSV(tabela, arquivo, driver, trip):

    # Preenche o cabeçalho do arquivo CSV
    for elem in ct.headerCSV:
        arquivo.write(elem)

    timeAcumulado = 0
    for i in range(len(tabela)):

        linhaAtual = tabela[i]
        # Informações fornecidas pelo próprio txt que não precisam ser tratadas
        ct.dictCSV["LAT"] = str(linhaAtual[2])+';'
        ct.dictCSV["LONG"] = str(linhaAtual[3])+';'
        ct.dictCSV["GPS_FILE"] = linhaAtual[9]+';'

        # Timestamp - Primeira coluna do arquivo txt
        timestamp = convert_unix_timestamp(linhaAtual[0])
        diaAtual = timestamp.strftime("%d/%m/%Y")
        horarioAtual = timestamp.strftime("%H:%M:%S")
        segundosAtual = toSeconds(timestamp)
        ct.dictCSV["DAY"] = diaAtual+';'
        ct.dictCSV["PR"] = horarioAtual+';'

        # Velocidade
        velocidadeKMH = float(linhaAtual[5])*3.6/100
        velocidadeMPH = velocidadeKMH/1.609
        ct.dictCSV["SPD_KMH"] = str('{:05f}'.format(
            velocidadeKMH)).replace('.', ',')+';'
        ct.dictCSV["SPD_MPH"] = str('{:05f}'.format(
            velocidadeMPH)).replace('.', ',')+';'

        ct.dictCSV['S'] = str(0)+';'
        ct.dictCSV['TIME_ACUM'] = str(0)+';'
        ct.dictCSV['ACEL_MS2'] = str(0)+';'
        ct.dictCSV["DRIVER"] = driver+';'
        ct.dictCSV["TRIP"] = driver+str(trip)+';'

        # A partir da segunda linha é possivel calcular a diferença de segundos e aceleração
        if (i > 0):
            linhaAnterior = tabela[i-1]
            timestampAnterior = convert_unix_timestamp(linhaAnterior[0])
            segundosAnterior = toSeconds(timestampAnterior)

            diffSegundos = abs(segundosAtual-segundosAnterior)

            velocidadeAnteriorKMH = float(linhaAnterior[5])*3.6/100
            aceleracaoMPS = (
                velocidadeKMH-velocidadeAnteriorKMH)/diffSegundos/3.6

            timeAcumulado += diffSegundos

            ct.dictCSV['ACEL_MS2'] = str('{:05f}'.format(
                aceleracaoMPS)).replace('.', ',')+';'
            ct.dictCSV['S'] = str(diffSegundos)+';'
            ct.dictCSV['TIME_ACUM'] = str(timeAcumulado)+';'

        # Preenche o arquivo CSV
        for key in ct.dictCSV:
            arquivo.write(ct.dictCSV[key])


# Função que gera o arquivo CSV contendo os dados das viagens sem vídeo
def geraSemVideoCSV(viagensBack, condutor, diretorioGPSConcatenado):

    conexao = sqlite3.connect(ct.dataBaseAuxiliar)
    cursor = conexao.cursor()

    # Define nome do arqvui CSV
    semVideoCSV = f'{diretorioGPSConcatenado}/{ct.planilhaSemVideo}.csv'

    # Busca o último vídeo da última viagem previamente definida
    lastViagem = viagensBack[len(viagensBack)-1].elementos
    lastViagem = lastViagem[len(lastViagem)-1][21:24]

    # QuerySQL devolvendo todos os dados cuja id do vídeo seja maior que o último vídeo da última viagem
    consulta_sql = f"SELECT * FROM card_table WHERE VIDEO>{lastViagem} AND HOVER='A'"
    cursor.execute(consulta_sql)

    tabela = cursor.fetchall()
    tabela = utils.corrigeTabela(tabela)
    if (len(tabela) > 1):
        with open(semVideoCSV, 'w') as arquivoGPS:
            preencheArquivoCSV(tabela, arquivoGPS, condutor,
                               viagensBack[len(viagensBack)-1].index+1)
        arquivoGPS.close()

    conexao.commit()
    conexao.close()


# Função que gera as planilhas CSV que possuem vídeos associados, capturados pela plataforma
def geraPlanilhasOficial(viagensBack, condutor, diretorioGPSConcatenado, indexInicial):

    conexao = sqlite3.connect(ct.dataBaseAuxiliar)
    cursor = conexao.cursor()
    # Para cada viagem contida no Card
    for i in range(len(viagensBack)):
        tabela = []

        # Para cada video da viagem é necessário obter os dados do banco de dados
        for video in viagensBack[i].elementos:
            # QuerySQL
            consulta_sql = f"SELECT * FROM card_table WHERE GPS_FILE like '%{video}%' AND HOVER='A'"
            cursor.execute(consulta_sql)
            matriz = cursor.fetchall()

            # Junção de todos os vídeos de determinada viagem em uma única estrutura de dados
            tabela.extend(matriz)

        # Correção da tabela de dados ( manter 1 segundo de diferença para cada linha )
        tabela = utils.corrigeTabela(tabela)
        try:
            nomeArquivoCSV = f'{diretorioGPSConcatenado}/Viagem{condutor}{indexInicial+i}-{convert_unix_timestamp(tabela[0][0]).strftime("%Y%m%d-%H%M%S")}.csv'
        except:
            nomeArquivoCSV = f'{diretorioGPSConcatenado}/Viagem{condutor}{indexInicial+i}-{viagensBack[i].nome}.csv'
        with open(nomeArquivoCSV, 'w') as arquivoGPS:
            # Com a tabela obtida e corrigida, é possível criar os arquivos CSV
            preencheArquivoCSV(tabela, arquivoGPS, condutor,
                               viagensBack[i].index)
        arquivoGPS.close()
    conexao.commit()
    conexao.close()
