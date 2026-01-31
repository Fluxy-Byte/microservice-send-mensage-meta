
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv


from src.infra.meta.Audio import get_audio
from src.infra.meta.SendMensageToMeta import send_mensagem


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
