import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv


# Carrega .env
load_dotenv()

app = FastAPI(
    title="Meta WhatsApp API",
    version="1.0.0"
)


# =========================
# MODELO DO BODY
# =========================
class MensagemRequest(BaseModel):
    mensagem: str
    idMensagem: str
    numeroDoContato: str


# =========================
# FUNÇÃO DE ENVIO
# =========================
def send_mensagem(mensagem, id_mensagem, numero_contato):

    url_meta = "https://graph.facebook.com/v22.0/872884792582393/messages"

    token_meta = os.getenv("TOKEN_META")

    if not token_meta:
        raise Exception("TOKEN_META não definido")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_meta}"
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": numero_contato,
        "context": {
            "message_id": id_mensagem
        },
        "type": "text",
        "text": {
            "preview_url": False,
            "body": mensagem
        }
    }

    response = requests.post(
        url_meta,
        json=payload,
        headers=headers,
        timeout=15
    )

    return response


# =========================
# ROTA DA API
# =========================
@app.post("/send-message")
def send_message(data: MensagemRequest):

    try:
        response = send_mensagem(
            data.mensagem,
            data.idMensagem,
            data.numeroDoContato
        )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        return {
            "status": "success",
            "meta_response": response.json()
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# ROTA DE HEALTHCHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}
