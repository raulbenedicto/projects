
import os
import time
from google import genai  # Assumindo que esta biblioteca existisse com esta estrutura
from google.genai import types

GOOGLE_API_KEY = 'adicionar aqui sua chave de API'  # Substitua pela sua chave de API real ou use variáveis de ambiente


print(f"Script iniciado em: {timestamp}")
# --- CORREÇÃO 1: Definir a API Key (ex: a partir de uma variável de ambiente) ---
# Antes de rodar, defina a variável de ambiente: export GOOGLE_API_KEY="sua_chave_api"
api_key = GOOGLE_API_KEY

if not api_key:
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não foi definida.")

client = genai.Client(
    api_key=api_key,
)

#VEO_MODEL_ID = "veo-2.0-generate-001" # @param ["veo-2.0-generate-001"] {"allow-input":true, isTemplate: true}

# --- CORREÇÃO 2: Remover parâmetros conflitantes ---
# Vamos definir a duração e o FPS, e deixar a API calcular o número de frames.

import time
from google.genai import types
from IPython.display import Video, HTML

prompt = "In a beautiful field of flowers, show a cute bunny that is slowly revealed to be an eldritch horror from outside time and space." # @param {type: "string"}

  # Here are a few prompts to help you get started and spark your creativity:
  # 1. Wide shot of a futuristic cityscape at dawn. Flying vehicles zip between skyscrapers. Camera pans across the skyline as the sun rises.
  # 2. A close up of a thief's gloved hand that reaches for a priceless diamond necklace in a museum display case. Camera slowly tracks the hand, with dramatic lighting and shadows.
  # 3. A giant, friendly robot strolls through a field of wildflowers, butterflies fluttering around its head. Camera tilts upwards as the robot looks towards the sky.
  # 4. A single, perfectly ripe apple hangs from a branch. It is covered in dew. A gentle breeze sways the branch, causing the apple to rotate slowly.
  # 5. A beehive nestled in a hollow tree trunk in a magical forest. Bees fly in and out of the hive, carrying pollen and nectar
  # 6. In a beautiful field of flowers, show a cute bunny that is slowly revealed to be an eldritch horror from outside time and space.

# Optional parameters
negative_prompt = "" # @param {type: "string"}
person_generation = "dont_allow"  # @param ["dont_allow", "allow_adult"]
aspect_ratio = "16:9" # @param ["16:9", "9:16"]
number_of_videos = 1 # @param {type:"slider", min:1, max:4, step:1}
duration = 5

operation = client.models.generate_videos(
    model="veo-2.0-generate-001",
    prompt=prompt,
      config=types.GenerateVideosConfig(
        person_generation=person_generation,
        aspect_ratio=aspect_ratio,  # 16:9 or 9:16
        number_of_videos=number_of_videos, # supported value is 1-4
        negative_prompt=negative_prompt,
        duration_seconds=duration, # supported value is 5-8
      ),
)

print("Iniciando a geração do vídeo. Isso pode levar alguns minutos...")
while not operation.done:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Aguardando o resultado...{timestamp}")
    time.sleep(20)
# Verificar se a operação foi concluída com sucesso
if operation.done:
    print("Operação concluída com sucesso!")
# Verificar se houve erros na operação
if operation.error:
    print(f"Erro na operação: {operation.error.message}")
# Verificar se a resposta contém vídeos gerados
if not operation.response or not operation.response.generated_videos:
    print("Nenhum vídeo gerado na resposta.")
# Baixar e salvar os vídeos gerados
import os
# Verificar se o diretório de saída existe, caso contrário, criar
output_dir = "generated_videos"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# Baixar os vídeos gerados
import os
# Verificar se a operação foi concluída com sucesso
if not operation.done:
    print("A operação ainda não foi concluída. Aguardando...")
    while not operation.done:
        time.sleep(20)  # Esperar 20 segundos antes de verificar novamente
if operation.error:
    print(f"Erro na operação: {operation.error.message}")
    exit(1) 
# Verificar se a resposta contém vídeos gerados
if not operation.response or not operation.response.generated_videos:
    print("Nenhum vídeo gerado na resposta.")
    exit(1)


for n, generated_video in enumerate(operation.response.generated_videos):
    print(f"Baixando vídeo {n+1}...")
    try:
        # A função de download deve retornar os bytes do vídeo
        video_bytes = client.files.download(file=generated_video.video)
        
        # Salvar os bytes em um arquivo local
        file_path = f"video_{n}.mp4"
        with open(file_path, "wb") as f:
            f.write(video_bytes)
        print(f"Vídeo salvo com sucesso em: {file_path}")

    except Exception as e:
        print(f"Falha ao baixar ou salvar o vídeo {n+1}: {e}")

# Exibir o vídeo gerado
from IPython.display import Video, display
for n in range(len(operation.response.generated_videos)):
    display(Video(f"video_{n}.mp4", embed=True, width=640, height=480))
    print(f"Vídeo {n+1} exibido.")
# Limpeza dos arquivos de vídeo após exibição
for n in range(len(operation.response.generated_videos)):
    os.remove(f"video_{n}.mp4")
print("Todos os vídeos foram exibidos e removidos do diretório.")
# Exibir mensagem final
print("Processo de geração de vídeo concluído com sucesso!")
