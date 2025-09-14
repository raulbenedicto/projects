import streamlit as st
import boto3
import json
import random

# Configuração da página
st.set_page_config(page_title="Quiz & Chat com AWS Bedrock", layout="wide")

# Sidebar para configurações
st.sidebar.header("Configurações AWS Bedrock")
region_name = st.sidebar.text_input("Region", value="us-east-1")
model_id = st.sidebar.text_input("Model ID", value="anthropic.claude-3-haiku-20240307-v1:0")
custom_prompt = st.sidebar.text_area("Prompt Personalizado (opcional)", 
                                   placeholder="Digite um prompt personalizado para o modelo...")

# Função para chamar o Bedrock
def call_bedrock(prompt, region, model):
    try:
        bedrock = boto3.client('bedrock-runtime', region_name=region)
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        response = bedrock.invoke_model(
            modelId=model,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
    
    except Exception as e:
        return f"Erro ao conectar com Bedrock: {str(e)}"

# Função para gerar pergunta de múltipla escolha
def generate_quiz_question():
    base_prompt = """Gere uma pergunta de múltipla escolha sobre um tópico relacionado a AWS especificamente sobre os serviços de AI e ML baseado no guide do exame AI Practitioner AIF-C01.
    Formato exato:
    PERGUNTA: [sua pergunta aqui]
    A) [opção A]
    B) [opção B] 
    C) [opção C]
    D) [opção D]
    RESPOSTA_CORRETA: [A, B, C ou D]
    EXPLICACAO: [breve explicação da resposta]"""
    
    if custom_prompt:
        prompt = f"{custom_prompt}\n\n{base_prompt}"
    else:
        prompt = base_prompt
    
    return call_bedrock(prompt, region_name, model_id)

# Função para parsear a resposta do quiz
def parse_quiz_response(response):
    try:
        lines = response.strip().split('\n')
        question = ""
        options = {}
        correct_answer = ""
        explanation = ""
        
        for line in lines:
            if line.startswith("PERGUNTA:"):
                question = line.replace("PERGUNTA:", "").strip()
            elif line.startswith(("A)", "B)", "C)", "D)")):
                key = line[0]
                value = line[3:].strip()
                options[key] = value
            elif line.startswith("RESPOSTA_CORRETA:"):
                correct_answer = line.replace("RESPOSTA_CORRETA:", "").strip()
            elif line.startswith("EXPLICACAO:"):
                explanation = line.replace("EXPLICACAO:", "").strip()
        
        return question, options, correct_answer, explanation
    except:
        return None, None, None, None

# Título principal
st.title("🤖 Quiz & Chat com AWS Bedrock")

# Criação das abas
tab1, tab2 = st.tabs(["📝 Quiz Múltipla Escolha", "💬 Chat"])

# ABA 1: Quiz
with tab1:
    st.header("Quiz de Múltipla Escolha")
    
    # Inicializar estado da sessão
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = None
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = None
    if 'show_result' not in st.session_state:
        st.session_state.show_result = False
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("🎲 Gerar Nova Pergunta", type="primary"):
            with st.spinner("Gerando pergunta..."):
                response = generate_quiz_question()
                question, options, correct, explanation = parse_quiz_response(response)
                
                if question and options:
                    st.session_state.quiz_data = {
                        'question': question,
                        'options': options,
                        'correct': correct,
                        'explanation': explanation
                    }
                    st.session_state.user_answer = None
                    st.session_state.show_result = False
                else:
                    st.error("Erro ao gerar pergunta. Tente novamente.")
    
    # Exibir pergunta se existir
    if st.session_state.quiz_data:
        st.subheader("Pergunta:")
        st.write(st.session_state.quiz_data['question'])
        
        # Opções de resposta
        options = st.session_state.quiz_data['options']
        selected = st.radio(
            "Escolha sua resposta:",
            options.keys(),
            format_func=lambda x: f"{x}) {options[x]}",
            key="quiz_radio"
        )
        
        if st.button("✅ Confirmar Resposta"):
            st.session_state.user_answer = selected
            st.session_state.show_result = True
        
        # Mostrar resultado
        if st.session_state.show_result and st.session_state.user_answer:
            correct_answer = st.session_state.quiz_data['correct']
            user_answer = st.session_state.user_answer
            
            if user_answer == correct_answer:
                st.success(f"🎉 Correto! A resposta é {correct_answer}")
            else:
                st.error(f"❌ Incorreto. A resposta correta é {correct_answer}")
            
            st.info(f"💡 Explicação: {st.session_state.quiz_data['explanation']}")

# ABA 2: Chat
with tab2:
    st.header("Chat com Claude Haiku 3.0")
    
    # Inicializar histórico do chat
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Exibir histórico do chat
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.chat_message("user").write(message['content'])
        else:
            st.chat_message("assistant").write(message['content'])
    
    # Input do usuário
    user_input = st.chat_input("Digite sua pergunta...")
    
    if user_input:
        # Adicionar mensagem do usuário ao histórico
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        st.chat_message("user").write(user_input)
        
        # Preparar prompt
        if custom_prompt:
            full_prompt = f"{custom_prompt}\n\nUsuário: {user_input}"
        else:
            full_prompt = user_input
        
        # Obter resposta do modelo
        with st.spinner("Pensando..."):
            response = call_bedrock(full_prompt, region_name, model_id)
        
        # Adicionar resposta ao histórico e exibir
        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
        st.chat_message("assistant").write(response)
    
    # Botão para limpar chat
    if st.button("🗑️ Limpar Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("💡 **Dica:** Configure suas credenciais AWS usando `aws configure` ou variáveis de ambiente.")