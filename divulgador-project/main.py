import csv
import os
from telegram_bot import enviar_telegram
from whatsapp_bot import enviar_whatsapp

def carregar_ofertas():
    try:
        with open('ofertas.csv', newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print("[ERRO] Arquivo ofertas.csv não encontrado.")
        exit()

def main():
    print("=== DIVULGADOR DE OFERTAS ===")
    
    # Etapa 1 – Carregar ofertas
    ofertas = carregar_ofertas()

    # Etapa 2 – Escolha do canal
    print("1 - Enviar para Telegram")
    print("2 - Enviar para WhatsApp")
    print("3 - Enviar para ambos")
    escolha = input("Escolha a opção: ")

    if escolha == '1':
        enviar_telegram(ofertas)
    elif escolha == '2':
        enviar_whatsapp(ofertas)
    elif escolha == '3':
        enviar_telegram(ofertas)
        enviar_whatsapp(ofertas)
    else:
        print("Opção inválida.")

if __name__ == '__main__':
    main()
