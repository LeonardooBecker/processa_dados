"""

    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Última atualização: 24/09/2023
    Link para o repositório: https://github.com/LeonardooBecker/processa_dados

"""

import os

# Deixa todas as linhas da tabela com exatamente 1 segundo de diferença
def corrigeTabela(matriz):
    novaMatriz = []
    for i in range(len(matriz)):
        if (i > 0):
            timeAtual = matriz[i][0]
            timeAnterior = matriz[i-1][0]
            # Se a diferença entre os timestamps for >= 2 significa linha faltante, logo são feita adições
            if (abs(timeAtual-timeAnterior) >= 2):

                matriz[i-1] = (matriz[i-1][0]+timeAtual -
                               timeAnterior,)+matriz[i-1][1:]

                for i in range(abs(timeAtual-timeAnterior)-1):
                    novaMatriz.append((timeAnterior+i+1,)+matriz[i][1:])
                novaMatriz.append(matriz[i])
            # Caso normal
            elif (abs(timeAtual-timeAnterior) == 1):
                novaMatriz.append(matriz[i])
            # Comando não necessário, mas o outro caso seria quando a diferença entre time é 0, não sendo necessário inserções
        # Primeira iteração
        else:
            novaMatriz.append(matriz[i])
    return novaMatriz


# Caso diretório não exista, cria o mesmo, caso contrario limpa o diretório
def limpaDiretorio(diretorio):
    if not os.path.exists(f'{diretorio}'):
        os.makedirs(f'{diretorio}')
    else:
        arquivos = os.listdir(diretorio)
        for i in arquivos:
            os.remove(f'{diretorio}/{i}')
