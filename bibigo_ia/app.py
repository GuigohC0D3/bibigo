# app.py
from voice.ouvir import ouvir_comando
from voice.falar import falar
from commands.router import rotear

def main():
    falar("Olá, eu sou B.I.B.I.G.O., seu assistente pessoal. Em que posso ajudar?")
    while True:
        comando = ouvir_comando()
        if not comando or comando == "nenhum":
            continue

        resposta = rotear(comando)

        if resposta == "__EXIT__":
            falar("Até a próxima, senhor Guilherme.")
            break

        if resposta:
            print("BIBIGO:", resposta)
            try:
                falar(resposta)
            except Exception:
                pass

if __name__ == "__main__":
    main()
