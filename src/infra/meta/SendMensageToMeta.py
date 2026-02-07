import os
import requests

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

# =========================
# CONFIG
# =========================

# Carrega .env
load_dotenv()

TOKEN_META = os.getenv("TOKEN_META")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

if not TOKEN_META:
    raise Exception("TOKEN_META não definido no .env")

if not PHONE_NUMBER_ID:
    raise Exception("PHONE_NUMBER_ID não definido no .env")

# =========================
# FASTAPI
# =========================

app = FastAPI(
    title="Meta WhatsApp API",
    version="1.0.0"
)

# =========================
# MODELS
# =========================


class MensagemRequest(BaseModel):
    mensagem: str
    idMensagem: str
    numeroDoContato: str


class AudioRequest(BaseModel):
    idAudio: str

# =========================
# META - SEND MESSAGE
# =========================


def send_mensagem(mensagem: str, id_mensagem: str, numero_contato: str):

    url_meta = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN_META}"
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
