"""

    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Última atualização: 24/09/2023
    Link para o repositório: https://github.com/LeonardooBecker/processa_dados

"""

import sqlite3
import csv
from local_libs import constants as ct

# Preenche os dados da linha e retorna se ela eh valida ou não
def preencheChaves(dicionarioCSV,linha,nomeCard):
    parts=linha.split(',')
    if(len(parts)==13):
        dicionarioCSV['TIMESTAMP']=parts[0]+','
        dicionarioCSV['HOVER']=parts[1]+','
        dicionarioCSV['LATITUDE']=parts[2]+','
        dicionarioCSV['LONGITUDE']=parts[3]+','
        dicionarioCSV['A1']=parts[4]+','
        dicionarioCSV['VELOCIDADE']=parts[5]+','
        dicionarioCSV['A2']=parts[6]+','
        dicionarioCSV['A3']=parts[7]+','
        dicionarioCSV['A4']=parts[8]+','
        dicionarioCSV['GPS_FILE']=parts[9]+','
        dicionarioCSV['A5']=parts[10]+','
        dicionarioCSV['A6']=parts[11]+','
        dicionarioCSV['A7']=parts[12]+','
        dicionarioCSV['CARD']=nomeCard+','
        dicionarioCSV['VIDEO']=int(parts[9][21:24])
        return 1
    else:
        return 0
            
# Cria um banco contendo as informações de todos os cards ( formato arquivo txt )
def newBanco(conteudoArquivo, nomeCard, limpar):
    
    # Conectar-se ao banco de dados SQLite (ele será criado se não existir)
    conexao = sqlite3.connect(ct.dataBaseAuxiliar)
    cursor = conexao.cursor()
    
    with open(ct.arquivoCSVAuxiliar, 'w') as arch:
        for elem in ct.headerTXT:
            arch.write(elem)
        for linha in conteudoArquivo:
            if(preencheChaves(ct.dictTXT,linha.strip(),nomeCard)):
                for key in ct.dictTXT:
                    arch.write(f'{ct.dictTXT[key]}')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS card_table (
        TIMESTAMP INTEGER,
        HOVER STRING,
        LATITUDE REAL,
        LONGITUDE REAL,
        A1 STRING,
        VELOCIDADE REAL,
        A2 STRING,
        A3 STRING,
        A4 STRING,
        GPS_FILE STRING,
        A5 STRING,
        A6 STRING,
        A7 STRING,
        CARD STRING,
        VIDEO INTEGER
    )
    ''')
       
    # Leia o arquivo CSV e insira os dados na tabela
    with open(ct.arquivoCSVAuxiliar, 'r') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        # Suponha que a primeira linha do CSV contenha os nomes das colunas
        colunas = next(leitor_csv)
        
        if(limpar):
            cursor.execute('DELETE FROM card_table')
        # Prepare a instrução SQL para inserir dados
        instrucao_sql = f'INSERT INTO card_table ({", ".join(colunas)}) VALUES ({", ".join(["?"] * len(colunas))})'

        # # Itere pelas linhas do CSV e insira-as na tabela
        for linha in leitor_csv:
            cursor.execute(instrucao_sql, linha)

        # # Commit as mudanças e feche a conexão com o banco de dados
        conexao.commit()
        conexao.close()    