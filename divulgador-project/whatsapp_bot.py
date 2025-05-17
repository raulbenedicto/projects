import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import WHATSAPP_GRUPOS, TEMPO_ENTRE_MENSAGENS

os.makedirs("logs", exist_ok=True)

def esperar_whatsapp_web(driver):
    try:
        print("[INFO] Aguardando carregamento do WhatsApp Web...")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        print("[OK] WhatsApp Web carregado com sucesso.")
    except Exception as e:
        print(f"[ERRO] Timeout ao aguardar WhatsApp Web: {e}")
        driver.save_screenshot("erro_whatsapp.png")
        driver.quit()
        exit()

def enviar_whatsapp(ofertas):
    log_file = open("logs/whatsapp_log.txt", "a", encoding="utf-8")

  # Comando para abrir o Chrome com debug ativado e user data dir
    # Este comando é específico para Windows
    os.system('start chrome --remote-debugging-port=9222 --user-data-dir="C:\\Users\\Raul\\SeleniumSession"')
    time.sleep(5) # Dar um tempo para o Chrome abrir antes de tentar conectar

    chrome_options = Options()
    chrome_options.debugger_address = "127.0.0.1:9222"  # Conectar a sessão existente

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://web.whatsapp.com")
    esperar_whatsapp_web(driver)

    for oferta in ofertas:
        if oferta['canal'].lower() != 'whatsapp':
            continue

        grupo = oferta['grupo']
        nome_grupo = WHATSAPP_GRUPOS.get(grupo)

        if not nome_grupo:
            msg = f"[ERRO] Grupo '{grupo}' não configurado.\n"
            print(msg)
            log_file.write(msg)
            continue

        mensagem = (
            "\U0001F6D2 *OFERTA ESPECIAL*\n"
            f"\U0001F4E6 Produto: {oferta['produto']}\n"
            f"\U0001F4B0 Preço: {oferta['preco']}\n"
            f"\U0001F4DD Detalhes: {oferta['descricao']}"
        )

        try:
            # Buscar grupo
            search_box = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            search_box.click()
            search_box.clear()
            search_box.send_keys(nome_grupo)
            time.sleep(2)
            search_box.send_keys(Keys.ENTER)

            # Campo de mensagem
            message_box = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            print("[DEBUG] Campo de mensagem localizado.")

            driver.execute_script("arguments[0].focus();", message_box)
            message_box.click()

            # ✅ Espera 6 segundos antes de começar a digitar
            print("[INFO] Esperando 2 segundos antes de digitar...")
            time.sleep(2)

            # Digita mensagem linha por linha com SHIFT+ENTER
            actions = ActionChains(driver)
            for line in mensagem.split('\n'):
                actions.send_keys(line)
                actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
            actions.perform()

            # ✅ Espera 4 segundos após digitar, antes de enviar
            print("[INFO] Aguardando alguns segundos antes de enviar...")
            time.sleep(TEMPO_ENTRE_MENSAGENS)

            # Envia a mensagem
            message_box.send_keys(Keys.ENTER)

            msg_ok = f"[OK] Mensagem enviada para: {grupo}\n"
            print(msg_ok)
            log_file.write(msg_ok)

        except Exception as envio_erro:
            erro_txt = f"[FALHA] Erro ao enviar para {grupo}: {envio_erro}"
            print(erro_txt)
            log_file.write(erro_txt + "\n")

        time.sleep(4)

    log_file.close()
    print("\n✅ Envio concluído. Navegador permanece aberto para conferência.")
