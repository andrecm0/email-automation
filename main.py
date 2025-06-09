# main.py

from auth.gmail_auth import get_gmail_service
from core.llm_chat import gerar_resposta_local as gerar_resposta
from core.responder import criar_mensagem, enviar_mensagem
import base64

def processar_emails():
    service = get_gmail_service()
    resultados = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=3).execute()
    mensagens = resultados.get('messages', [])

    for msg in mensagens:
        msg_completo = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_completo['payload']
        headers = payload['headers']

        remetente = next((h['value'] for h in headers if h['name'] == 'From'), '')
        assunto = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        partes = payload.get('parts', [])
        corpo = ""

        for parte in partes:
            if parte['mimeType'] == 'text/plain' and 'data' in parte['body']:
                corpo = base64.urlsafe_b64decode(parte['body']['data']).decode()
                break

        if not corpo:
            print(f"Email de {remetente} sem corpo em texto simples. Pulando.")
            continue

        print(f"\n>>> Respondendo: {remetente} | Assunto: {assunto}")

        corpo_resumido = corpo[:800]  # Limita o prompt
        mensagem = f"Remetente: {remetente}\nAssunto: {assunto}\nMensagem: {corpo_resumido}"
        resposta = gerar_resposta(mensagem)

        print("\n--- Resposta gerada pela Aurora local ---\n")
        print(resposta)
        input("\nPressione Enter para enviar este email ou CTRL+C para cancelar...\n")

        mensagem_email = criar_mensagem(remetente, assunto, resposta)
        enviar_mensagem(service, mensagem_email)

        # Marcar como lido
        service.users().messages().modify(userId='me', id=msg['id'], body={'removeLabelIds': ['UNREAD']}).execute()

if __name__ == '__main__':
    processar_emails()
