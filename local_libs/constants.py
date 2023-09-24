"""

    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Última atualização: 24/09/2023
    Link para o repositório: https://github.com/LeonardooBecker/processa_dados

"""

# Constantes usadas no projeto
pastaVideosConcatenados = 'videos_concatenados'
pastaArquivosGPS = 'arquivos_gps'

planilhaSemVideo = 'planilha_sem_video.csv'
arquivoCSVAuxiliar = "dbAux.csv"
dataBaseAuxiliar = "dbAux.db"

# Quantidade mínima de videos para ser considerado uma viagem
quantidadeMinimaVideos = 2

headerCSV = ['DRIVER;', 'LONG;', 'LAT;', 'DAY;', 'DAY_CORRIGIDO;', '03:00:00;', 'TRIP;', 'ID;',
             'PR;', 'H;', 'M;', 'S;', 'TIME_ACUM;', 'SPD_MPH;', 'SPD_KMH;', 'ACEL_MS2;', 'HEADING;', 'ALTITUDE_FT;',
             'VALID_TIME;', 'TIMESTAMP;', 'CPOOL;', 'CPOOLING;', 'WSB;', 'UMP_YN;', 'UMP;', 'PICK_UP;', 'ACTION;',
             'GPS_FILE;', 'CIDADE;', 'BAIRRO;', 'NOME_RUA;', 'HIERARQUIA_CWB;', 'HIERARQUIA_CTB;', 'LIMITE_VEL\n']

headerTXT = ['TIMESTAMP,', 'HOVER,', 'LATITUDE,', 'LONGITUDE,', 'A1,', 'VELOCIDADE,', 'A2,', 'A3,',
             'A4,', 'GPS_FILE,', 'A5,', 'A6,', 'A7,', 'CARD,', 'VIDEO\n']

dictCSV = {
    'DRIVER': ';',
    'LONG': ';',
    'LAT': ';',
    'DAY': ';',
    'DAY_CORRIGIDO': ';',
    '03:00:00': ';',
    'TRIP': ';',
    'ID': ';',
    'PR': ';',
    'H': ';',
    'M': ';',
    'S': ';',
    'TIME_ACUM': ';',
    'SPD_MPH': ';',
    'SPD_KMH': ';',
    'ACEL_MS2': ';',
    'HEADING': ';',
    'ALTITUDE_FT': ';',
    'VALID_TIME': ';',
    'TIMESTAMP': ';',
    'CPOOL': ';',
    'CPOOLING': ';',
    'WSB': ';',
    'UMP_YN': ';',
    'UMP': ';',
    'PICK_UP': ';',
    'ACTION': ';',
    'GPS_FILE': ';',
    'CIDADE': ';',
    'BAIRRO': ';',
    'NOME_RUA': ';',
    'HIERARQUIA_CWB': ';',
    'HIERARQUIA_CTB': ';',
    'LIMITE_VEL': ';',
    '\n': '\n'
}


dictTXT = {
    'TIMESTAMP': ",",
    'HOVER': ",",
    'LATITUDE': ",",
    'LONGITUDE': ",",
    'A1': ",",
    'VELOCIDADE': ",",
    'A2': ",",
    'A3': ",",
    'A4': ",",
    'GPS_FILE': ",",
    'A5': ",",
    'A6': ",",
    'A7': ",",
    'CARD': ",",
    'VIDEO': ",",
    '\n': "\n"
}
