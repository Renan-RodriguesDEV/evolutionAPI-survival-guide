import base64
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from filetypes import FileTypes

load_dotenv()
# Cabeçalhos padrão para as requisições
headers = {
    "Content-Type": "application/json",
    "apiKey": os.getenv("AUTHENTICATION_API_KEY", "your-api-key"),
}
base_url = os.getenv(
    "BASE_URL", "http://localhost:8080"
)  # Altere para o URL do seu servidor Evolution API
instance = os.getenv("INSTANCE_NAME", "your-instance-name")


def send_text(message: str, contact: str):
    """Envia uma mensagem de texto para o número especificado.

    Args:
        message (str): Mensagem que será enviada.
        contact (str): Numero do destinatário no formato internacional (ex: 5511999999999).

    Returns:
        dict: Resposta da API.
    """
    url = f"{base_url}/message/sendText/{instance}"
    # Corpo da requisição em dict que será passado como JSON
    payload = {"number": contact, "text": message}
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    return response.status_code, response.json()


def send_file_url(
    url_file: str,
    contact: str,
    mediatype: str = FileTypes.PNG.mediatype,
    mimetype: str = FileTypes.PNG.mimetype,
    caption: str = "Only image",
    filename: str = "only_image.png",
):
    """Envia um arquivo a partir de uma URL para o número especificado.

    Args:
        url_file (str): URL do arquivo que será enviado.
        contact (str): Numero do destinatário no formato internacional (ex: 5511999999999).
        mediatype (str): Tipo da midia do arquivo (ex. document, image e etc). Default: FileTypes.PNG.mediatype.
        mimetype (str): Tipo da MIME do arquivo (ex. image/png, application/pdf e etc). Default: FileTypes.PNG.mimetype.
        caption (str): Legenda do arquivo.
        filename (str): Nome do arquivo que irá aparecer no WhatsApp.
    Returns:
        dict: Resposta da API.
    """
    url = f"{base_url}/message/sendMedia/{instance}"
    payload = {
        "number": contact,
        # Tipo de mídia
        "mediatype": mediatype,
        # MIME type do arquivo
        "mimetype": mimetype,
        # Legenda da Arquivo
        "caption": caption,
        # url da imagem
        "media": url_file,
        "fileName": filename,
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    return response.status_code, response.json()


def file_to_base64(path: str) -> str:
    """Converte o arquivo (path) em base64 encode e depois decodifica para String (basicamente um binario em str).

    Args:
        path (str): Caminho parcial ou completo do arquivo.

    Returns:
        str: String codificada em base64 do arquivo.
    """
    # Pega os bytes do arquivo
    data = Path(path).read_bytes()
    # Converte para base64 e decodifica para string
    return base64.b64encode(data).decode()


def send_file(
    path: str,
    contact: str,
    caption="",
    mediatype: str = FileTypes.PDF.mediatype,
    mimetype: str = FileTypes.PDF.mimetype,
):
    """Envia um arquivo em base64 para o número especificado.

    Args:
        path (str): Caminho parcial ou completo do arquivo.
        contact (str): Numero do destinatário no formato internacional (ex: 5511999999999).
        caption (str): Legenda do arquivo.
        mediatype (str): Tipo da midia do arquivo (ex. document, image e etc). Default: FileTypes.PDF.mediatype.
        mimetype (str): Tipo da MIME do arquivo (ex. image/png, application/pdf e etc). Default: FileTypes.PDF.mimetype.
    Returns:
        dict: Resposta da API.
    """
    url = f"{base_url}/message/sendMedia/{instance}"
    payload = {
        "number": contact,
        # Tipo de mídia
        "mediatype": mediatype,
        # MIME type do arquivo
        "mimetype": mimetype,
        # Dados da arquivo em base64
        "media": file_to_base64(path),
        # Nome do arquivo que irá aparecer no WhatsApp
        "fileName": Path(path).name,
        # Legenda da Arquivo
        "caption": caption,
    }
    response = requests.post(url=url, json=payload, headers=headers)
    print(response.json())
    return response.status_code, response.json()
