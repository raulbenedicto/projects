import csv
import os
import sys
import gdown
from telegram_bot import enviar_telegram
from whatsapp_bot import enviar_whatsapp

# ID do arquivo no Google Drive (caso use)
ARQUIVO_ID = '1ABCdEFGhIJKlmnOPQRsTuvWXyZ'  # Substitua pelo seu ID real

def baixar_ofertas_do_drive():
    url = f"https://drive.google.com/uc?id={ARQUIVO_ID}"
    output = "ofertas.csv"
    if not os.path.exists(output):
        print("[INFO] Baixando ofertas.csv do Google Drive...")
        gdown.download(url, output, quiet=False)
        print("[OK] Download concluído.")

def carregar_ofertas():
    with open('ofertas.csv', newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def main():
    # opcional: baixar_ofertas_do_drive()

    ofertas = carregar_ofertas()

    if len(sys.argv) < 2:
        print("Uso: python main.py [telegram|whatsapp|ambos]")
        return

    escolha = sys.argv[1].lower()

    if escolha == 'telegram':
        enviar_telegram(ofertas)
    elif escolha == 'whatsapp':
        enviar_whatsapp(ofertas)
    elif escolha == 'ambos':
        enviar_telegram(ofertas)
        enviar_whatsapp(ofertas)
    else:
        print("Opção inválida. Use: telegram | whatsapp | ambos")

if __name__ == '__main__':
    main()
