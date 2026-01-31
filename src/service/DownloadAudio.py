import os
import time
import requests

from dotenv import load_dotenv


# Carrega .env
load_dotenv()

TOKEN_META = os.getenv("TOKEN_META")

if not TOKEN_META:
    raise Exception("TOKEN_META não definido no .env")


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
