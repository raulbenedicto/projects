import csv
from telegram_bot import enviar_telegram
from whatsapp_bot import enviar_whatsapp

def carregar_ofertas():
    with open('ofertas.csv', newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def main():
    print("=== DIVULGADOR DE OFERTAS ===")
    print("1 - Enviar para Telegram")
    print("2 - Enviar para WhatsApp")
    print("3 - Enviar para ambos")
    escolha = input("Escolha a opção: ")

    ofertas = carregar_ofertas()

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
