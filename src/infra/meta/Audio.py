
import os

import requests

from dotenv import load_dotenv

from src.service.ConverterAudio import converter_audio
from src.service.DownloadAudio import download_audio

load_dotenv()

TOKEN_META = os.getenv("TOKEN_META")

if not TOKEN_META:
    raise Exception("TOKEN_META não definido no .env")

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