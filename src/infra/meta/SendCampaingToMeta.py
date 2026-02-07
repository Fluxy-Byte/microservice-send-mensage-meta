import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

TOKEN_META = os.getenv("TOKEN_META")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

if not TOKEN_META:
    raise Exception("TOKEN_META não definido no .env")

if not PHONE_NUMBER_ID:
    raise Exception("PHONE_NUMBER_ID não definido no .env")


logger = logging.getLogger(__name__)


def send_campaing(payload: dict):

    url_meta = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN_META}"
    }

    try:
        response = requests.post(
            url_meta,
            json=payload,
            headers=headers,
            timeout=15
        )

        logger.info(f"Meta response: {response.status_code}")

        return response

    except requests.exceptions.RequestException as e:

        logger.error(f"Erro ao chamar Meta API: {e}")

        raise Exception("Falha ao se comunicar com a Meta API")
