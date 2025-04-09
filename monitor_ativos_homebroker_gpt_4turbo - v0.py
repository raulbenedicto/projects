import pyautogui
import pytesseract
import pygetwindow as gw
# Caminho do executável do Tesseract no Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image
from openai import OpenAI
import time
from datetime import datetime
import winsound
import base64



# Configurações
client = OpenAI(api_key = "add secret here")
TITULO_JANELA = "Home Broker"  # ajuste conforme a aba do navegador
OCR_LIMPAR = lambda x: x.replace('\n', ' ').replace('\x0c', '').strip()

# Define caminho para o Tesseract se necessário (Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Captura da tela completa (ou pode usar pygetwindow para capturar só a janela do navegador)
#def capturar_tela(nome="grafico.png"):
#    img = pyautogui.screenshot()
#    img.save(nome)
#    return nome


def capturar_tela(titulo_aba="Home Broker", nome_arquivo="grafico.png", tentativas=3):
    for tentativa in range(1, tentativas + 1):
        try:
            print(f"[⏳] Tentando capturar a janela ({tentativa}/{tentativas})...")
            janelas = gw.getWindowsWithTitle(titulo_aba)
            if not janelas:
                print(f"[❌] Janela com título '{titulo_aba}' não encontrada.")
                time.sleep(1)
                continue

            janela = janelas[0]

            if janela.isMinimized:
                print("[ℹ️] Janela minimizada. Restaurando...")
                janela.restore()
                time.sleep(1)

            if not janela.isMaximized:
                janela.maximize()
                time.sleep(1)

            try:
                janela.activate()
                time.sleep(1)
            except Exception:
                print("[⚠️] Não foi possível ativar a janela (seguindo sem ativar).")

            left, top, width, height = janela.left, janela.top, janela.width, janela.height
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            screenshot.save(nome_arquivo)
            print(f"[✅] Captura realizada com sucesso ({nome_arquivo})")
            return nome_arquivo
        except Exception as e:
            print(f"[❌] Erro ao capturar a janela: {e}")
            time.sleep(2)
    return None




# Converte imagem para base64
def imagem_para_base64(caminho):
    with open(caminho, "rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")


# Envia imagem para análise via GPT-4 com visão
def analisar_imagem(image_path):
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(image_path, "rb") as f:
        imagem_base64 = base64.b64encode(f.read()).decode("utf-8")
    
    prompt = f"""
Você é um analista técnico profissional que analisa gráficos de 1 minuto para tomar decisões de trading de curto prazo (scalping).
Analise a imagem do gráfico enviada e diga:
🕒 Timestamp: {timestamp}  
🔍 Análise: Interprete os últimos candles e contexto técnico  
📊 Sinal: COMPRA (CALL), VENDA (PUT) ou AGUARDAR  
📈 Aguardando: O que seria necessário para confirmar uma entrada (se aplicável)
Seja objetivo e direto, linguagem de trader.
Caso uma ação não seja clara, faça a sugestão de um novo indicador e também a sugestão de troca de analise dos Ativos.
    """


    response = client.chat.completions.create(
        model="gpt-4-turbo",  # ← modelo atualizado com visão
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{imagem_base64}"
                    }},
                ]
            }
        ],
        max_tokens=500,
    )

    resultado = response.choices[0].message.content.strip()
    print(f"\n📢 Resultado da Análise:\n{resultado}\n")
    # Gera timestamp atual
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"[DATA/HORA]: {timestamp}")
    return resultado



#    response = client.chat.completions.create(
#        model="gpt-3.5-turbo",
#        messages=[{"role": "user", "content": prompt}],
#        temperature=0.4,
#        max_tokens=200
#    )

#    resultado = response.choices[0].message.content.strip().upper()
#   print(f"[PROMPT GERADO]: {prompt}")
#    print("-------------------------------------------------------------------")
#    print("-------------------------------------------------------------------")
##    print(f"[SINAL GERADO]: {resultado}")
#    # Gera timestamp atual
#    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
##    print(f"[DATA/HORA]: {timestamp}")
#    return resultado

def alertar_sinal(sinal):
    if "COMPRA" in sinal.upper():
        print("[🔔] Alerta de COMPRA — tocando som A")
        winsound.Beep(880, 1000)  # 880 Hz por 1s
    elif "VENDA" in sinal.upper():
        print("[🔔] Alerta de VENDA — tocando som B")
        winsound.Beep(440, 1000)  # 440 Hz por 1s



# Loop principal
while True:
    imagem = capturar_tela(titulo_aba=TITULO_JANELA)
    if imagem:
        resultado = analisar_imagem(imagem)
        alertar_sinal(resultado)
    else:
        print("[❌] Não foi possível capturar a imagem.")
    time.sleep(60)  # Aguardar 1 min



