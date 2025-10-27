import datetime
import os
import wikipedia
import pywhatkit
from utils import falar, ouvir_comando

def executar_tarefas(comando):
    if 'horas' in comando:
        hora = datetime.datetime.now().strftime('%H:%M')
        falar(f'Senhor Guilherme, a hora atual é {hora}')
    elif 'abrir youtube' in comando:
        falar('Abrindo YouTube, senhor Guilherme.')
        pywhatkit.playonyt('youtube') # Abre o YouTube no navegador
    elif 'pesquisar' in comando:
        termo = comando.replace('pesquisar', '').strip()
        falar(f'Pesquisando {termo} na internet.')
        pywhatkit.search(termo)
    elif 'quem é' in comando:
        pessoa = comando.replace('quem é', '').strip()
        info = wikipedia.summary(pessoa, 1) # Resume a informação em 1 frase
        falar(info)
    elif 'o que é' in comando:
        termo = comando.replace('o que é', '').strip()
        info = wikipedia.summary(termo, 1)
        falar(info)
    elif 'tocar' in comando:
        musica = comando.replace('tocar', '').strip()
        falar(f'Tocando {musica} no YouTube.')
        pywhatkit.playonyt(musica)
    elif 'tchau' in comando or 'sair' in comando:
        falar('Até a próxima, senhor Guilherme.')
        exit()
    else:
        falar('Não entendi. Poderia repetir?')

def principal():
    falar('Olá, eu sou B.I.B.I.G.O., seu assistente pessoal. Em que posso ajudar?')
    while True:
        comando = ouvir_comando()
        if 'bibigo' in comando:
            comando = comando.replace('bibigo', '')
            executar_tarefas(comando)
        elif 'sair' in comando:
            executar_tarefas('sair')

if __name__ == "__main__":
    wikipedia.set_lang('pt')
    principal()
