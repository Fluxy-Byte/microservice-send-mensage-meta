import os
import time
import requests

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

from src.infra.rabbit.ConectRabbit import conectar, fechar

# =========================
# CONFIG
# =========================

# Carrega .env
load_dotenv()

# OpenAI Client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

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

    url_meta = "https://graph.facebook.com/v22.0/872884792582393/messages"

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

# =========================
# META - GET + TRANSCRIBE
# =========================


def get_audio(id_audio: str):

    try:

        # 1️⃣ Buscar dados do áudio
        url = f"https://graph.facebook.com/v24.0/{id_audio}"

        headers = {
            "Authorization": f"Bearer {TOKEN_META}"
        }

        response = requests.get(url, headers=headers, timeout=30)

        data = response.json()

        audio_url = data.get("url")

        if not audio_url:
            raise Exception("URL do áudio não encontrada")

        # 2️⃣ Download
        result = download_audio(audio_url)

        if not result["status"]:
            raise Exception("Falha no download")

        file_path = result["local"]

        # 3️⃣ Converter
        convert = converter_audio(file_path)

        # 4️⃣ Remove arquivo
        try:
            os.remove(file_path)
        except:
            pass

        return {
            "status": convert["status"],
            "data": convert["text"]
        }

    except Exception as e:

        print("Erro no get_audio:", e)

        return {
            "status": False,
            "data": ""
        }


def download_audio(audio_url: str):

    try:

        base_dir = os.getcwd()
        audio_dir = os.path.join(base_dir, "audios")

        os.makedirs(audio_dir, exist_ok=True)

        filename = f"audio_{int(time.time() * 1000)}.ogg"
        filepath = os.path.join(audio_dir, filename)

        headers = {
            "Authorization": f"Bearer {TOKEN_META}"
        }

        response = requests.get(
            audio_url,
            headers=headers,
            timeout=60
        )

        if response.status_code != 200:
            raise Exception("Erro ao baixar áudio")

        with open(filepath, "wb") as f:
            f.write(response.content)

        print("Áudio salvo:", filepath)

        return {
            "status": True,
            "local": filepath
        }

    except Exception as e:

        print("Erro no download:", e)

        return {
            "status": False,
            "local": ""
        }


def converter_audio(path: str):

    try:

        with open(path, "rb") as audio_file:

            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                language="pt"
            )

        return {
            "status": True,
            "text": transcription.text
        }

    except Exception as e:

        print("Erro na transcrição:", e)

        return {
            "status": False,
            "text": ""
        }

# =========================
# ROUTES
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


@app.post("/transcribe-audio")
def transcribe_audio(data: AudioRequest):

    try:

        result = get_audio(data.idAudio)

        if not result["status"]:

            raise HTTPException(
                status_code=400,
                detail="Erro ao transcrever áudio"
            )

        return {
            "mensagem": result["data"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.on_event("startup")
def startup():
    conectar()


@app.on_event("shutdown")
def shutdown():
    fechar()
