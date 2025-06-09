# core/responder.py

import os
import base64
from email.mime.text import MIMEText
from dotenv import load_dotenv
from openai import OpenAI

# Carrega a chave da API do .env
load_dotenv()

# Instancia segura do cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_resposta(remetente, assunto, conteudo_email):
    prompt = f"""
Você é uma inteligência artificial que responde e-mails de forma clara, respeitosa e profissional.

Remetente: {remetente}
Assunto: {assunto}
Mensagem: {conteudo_email}

Responda de forma apropriada:
"""

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )

    return resposta.choices[0].message.content.strip()

def criar_mensagem(destinatario, assunto, corpo):
    mensagem = MIMEText(corpo)
    mensagem['to'] = destinatario
    mensagem['subject'] = f"Re: {assunto}"
    return {'raw': base64.urlsafe_b64encode(mensagem.as_bytes()).decode()}

def enviar_mensagem(service, mensagem):
    return service.users().messages().send(userId='me', body=mensagem).execute()
