import os
import subprocess

# Concatena os videos de uma viagem
def concatenacao(viagens, diretorioCard, diretorioVideosConcatenados, condutor):
    playlist_file='playlist.txt'
    for viagem in viagens:
        with open(playlist_file,'w') as pFile:
            for video in viagem.elementos:
                pFile.write(f"file '{diretorioCard}/{video}'\n")
                
        nomeVideo=f'{diretorioVideosConcatenados}/Viagem{condutor}{viagem.index}-{viagem.nome}-{viagem.categoria}.mp4'
        command=['ffmpeg','-f','concat','-safe','0','-i',playlist_file,'-c','copy',nomeVideo]
        # subprocess.run(command)
        os.remove(playlist_file)
            
    pFile.close() 