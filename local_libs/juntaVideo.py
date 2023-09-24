"""

    Autor: Leonardo Becker de Oliveira
    Contato: leonardobecker79@gmail.com
    Última atualização: 24/09/2023
    Link para o repositório: https://github.com/LeonardooBecker/processa_dados

"""

import os
import subprocess
import sys

# Concatena os videos de uma viagem
def concatenaVideos(viagens, diretorioCard, diretorioVideosConcatenados, condutor):
    playlist_file = 'playlist.txt'
    for viagem in viagens:
        with open(playlist_file, 'w') as pFile:
            for video in viagem.elementos:
                pFile.write(f"file '{diretorioCard}/{video}'\n")

        nomeVideo = f'{diretorioVideosConcatenados}/Viagem{condutor}{viagem.index}-{viagem.nome}-{viagem.categoria}.mp4'
        command = ['ffmpeg', '-f', 'concat', '-safe', '0',
                   '-i', playlist_file, '-c', 'copy', nomeVideo]
        
        # Se na chamada do programa for passado "0" como argumento, não é feita a concatenação dos vídeos
        try:
            if(sys.argv[2]!="0"):
                subprocess.run(command)
        except:
            subprocess.run(command)
        os.remove(playlist_file)

    pFile.close()
