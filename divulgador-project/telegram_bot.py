import csv
import time
import requests
import os
from config import TELEGRAM_BOT_TOKEN, CHAT_IDS, TEMPO_ENTRE_MENSAGENS
from datetime import datetime

#variavel de data e hora
datetime_now = datetime.now()

# Garantir pasta de logs
os.makedirs("logs", exist_ok=True)

def enviar_telegram(ofertas):
    log_file = open("logs/telegram_log.txt", "a", encoding="utf-8")
    for oferta in ofertas:
        if oferta['canal'].lower() != 'telegram':
            continue

        grupo = oferta['grupo']
        chat_id = CHAT_IDS.get(grupo)

        if not chat_id:
            mensagem_erro = f"{datetime_now}[ERRO] Grupo '{grupo}' não configurado.\n"
            print(mensagem_erro)
            log_file.write(mensagem_erro)
            continue

        mensagem = f"🛍️ *OFERTA ESPECIAL* 🛍️\n📦 Produto: {oferta['produto']}\n💰 Preço: {oferta['preco']}\n📝 Detalhes: {oferta['descricao']}"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {'chat_id': chat_id, 'text': mensagem, 'parse_mode': 'Markdown'}

        response = requests.post(url, data=data)

        if response.status_code == 200:
            msg_ok = f"{datetime_now}[OK] Enviado para Telegram - Grupo: {grupo}\n"
            print(msg_ok)
            log_file.write(msg_ok)
        else:
            msg_fail = f"{datetime_now}[FALHA] Não enviado para {grupo}. Status: {response.status_code} - {response.text}\n"
            print(msg_fail)
            log_file.write(msg_fail)

        time.sleep(TEMPO_ENTRE_MENSAGENS)
    log_file.close()
