import base64
import os
from pathlib import Path

import requests

# Cabeçalhos padrão para as requisições
headers = {
    "Content-Type": "application/json",
    "apiKey": os.getenv("AUTHENTICATION_API_KEY", "your-api-key"),
}
base_url = "http://localhost:8080"  # Altere para o URL do seu servidor Evolution API
instance = os.getenv("INSTANCE_NAME", "your-instance-name")


def send_text(message: str, number: str):
    """Envia uma mensagem de texto para o número especificado.

    Args:
        message (str): Mensagem que será enviada.
        number (str): Numero do destinatário no formato internacional (ex: 5511999999999).

    Returns:
        dict: Resposta da API.
    """
    url = f"{base_url}/message/sendText/{instance}"
    # Corpo da requisição em dict que será passado como JSON
    payload = {"number": number, "text": message}
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    return response.status_code, response.json()


def send_image_url(
    url_file: str,
    number: str,
    caption: str = "Only image",
    filename: str = "only_image.png",
):
    """Envia uma imagem a partir de uma URL para o número especificado.

    Args:
        url_file (str): URL da imagem que será enviada.
        number (str): Numero do destinatário no formato internacional (ex: 5511999999999).
        caption (str): Legenda da imagem.
        filename (str): Nome do arquivo que irá aparecer no WhatsApp.
    Returns:
        dict: Resposta da API.
    """
    url = f"{base_url}/message/sendMedia/{instance}"
    payload = {
        "number": number,
        # Tipo de mídia
        "mediatype": "image",
        "caption": caption,
        # url da imagem
        "media": url_file,
        "fileName": filename,
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    return response.status_code, response.json()


def file_to_base64(path: str) -> str:
    """Converte a imagem (path) em base64 encode e depois decodifica para String (basicamente um binario em str).

    Args:
        path (str): Caminho parcial ou completo da imagem.

    Returns:
        str: String codificada em base64 da imagem.
    """
    # Pega os bytes do arquivo
    data = Path(path).read_bytes()
    # Converte para base64 e decodifica para string
    return base64.b64encode(data).decode()


def send_image_file(image_path: str, number: str):
    """Envia uma imagem em base64 para o número especificado.

    Args:
        image_path (str): Caminho parcial ou completo da imagem.
        number (str): Numero do destinatário no formato internacional (ex: 5511999999999).

    Returns:
        dict: Resposta da API.
    """
    url = f"{base_url}/message/sendMedia/{instance}"

    base64_data = file_to_base64(image_path)

    payload = {
        "number": number,
        # Tipo de mídia
        "mediatype": "image",
        # MIME type da imagem
        "mimetype": "image/png",
        # Dados da imagem em base64
        "media": f"{base64_data}",
        # Nome do arquivo que irá aparecer no WhatsApp
        "fileName": Path(image_path).name,
        # Legenda da imagem
        "caption": "Only image",
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    return response.json()


## Examples:

"""
path = "./your-image.png"

url_image = "https://path-to-image.jpg"

send_text("Hello World!", "5521999999999")

send_image_url(
    url_image,
    "5514998778713")
send_image_file(path, "5521999999999")

"""
