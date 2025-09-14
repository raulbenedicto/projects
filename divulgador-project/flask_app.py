# Importa a classe Flask do pacote flask
from flask import Flask, request, jsonify
# Importa a função processar_ofertas do módulo main
from main import processar_ofertas
# Importa a função carregar_configuracoes do módulo config
from config import carregar_configuracoes

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Carrega as configurações da aplicação
config = carregar_configuracoes()

# Define a rota inicial ('/') que aceita requisições GET e POST
@app.route('/', methods=['GET', 'POST'])
def index():
    # Verifica se a requisição é do tipo POST
    if request.method == 'POST':
        # Obtém os dados JSON enviados na requisição
        data = request.get_json()
        # Extrai o caminho do arquivo de ofertas dos dados recebidos, usando um valor padrão se não for fornecido
        caminho_arquivo = data.get('caminho_arquivo', config['caminho_arquivo_ofertas'])
        # Extrai a lista de canais dos dados recebidos, usando um valor padrão se não for fornecida
        canais = data.get('canais', config['canais_divulgacao'])

        # Chama a função processar_ofertas com o caminho do arquivo e a lista de canais
        processar_ofertas(caminho_arquivo, canais)

        # Retorna uma resposta JSON indicando sucesso
        return jsonify({"message": "Processamento iniciado!"}), 200
    else:
        # Se a requisição for GET, retorna uma mensagem simples
        return "Bem-vindo ao divulgador de ofertas!"

# Verifica se o script está sendo executado diretamente
if __name__ == '__main__':
    # Executa a aplicação Flask em modo debug
    app.run(debug=True)
