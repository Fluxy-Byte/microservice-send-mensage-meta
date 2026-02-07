import os
import time
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

if not TOKEN_META:
    raise Exception("TOKEN_META não definido no .env")

# =========================
# FASTAPI
# =========================

app = FastAPI(
    title="Meta WhatsApp API",
    version="1.0.0"
)


def send_campaing(payload):

    url_meta = "https://graph.facebook.com/v22.0/872884792582393/messages"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN_META}"
    }

    response = requests.post(
        url_meta,
        json=payload,
        headers=headers,
        timeout=15
    )

    return response
