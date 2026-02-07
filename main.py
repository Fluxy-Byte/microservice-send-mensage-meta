
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from typing import List, Any
from src.infra.meta.Audio import get_audio
from src.infra.meta.SendMensageToMeta import send_mensagem
from src.infra.meta.SendCampaingToMeta import send_campaing

# Carrega .env
load_dotenv()

# =========================
# FASTAPI
# =========================

app = FastAPI(
    title="Meta WhatsApp API",
    version="1.0.0"
)


# =========================
# CLASSES PARA INTERFACE
# =========================
class MensagemRequest(BaseModel):
    mensagem: str
    idMensagem: str
    numeroDoContato: str

    
class AudioRequest(BaseModel):
    idAudio: str

    
class Language(BaseModel):
    code: str


class Template(BaseModel):
    name: str
    language: Language
    components: List[Any]


class Body(BaseModel):
    messaging_product: str
    recipient_type: str
    to: str
    type: str
    template: Template


class CampaingRequest(BaseModel):
    type: str
    body: Body


@app.post("/send-message")
def send_camapanha(data: CampaingRequest):

    try:

        response = send_campaing(data)

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
