import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def converter_audio(path: str):
    try:
        with open(path, "rb") as audio_file:

            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                language="pt"
            )

        # ✅ Apaga o arquivo depois de usar
        if os.path.exists(path):
            os.remove(path)
            print(f"🗑 Arquivo removido: {path}")

        return {
            "status": True,
            "text": transcription.text
        }

    except Exception as e:

        print("Erro na transcrição:", e)

        # ⚠️ Tenta apagar mesmo se der erro
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"🗑 Arquivo removido após erro: {path}")
            except Exception as err:
                print("Erro ao apagar arquivo:", err)

        return {
            "status": False,
            "text": ""
        }
