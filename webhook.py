from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Webhook Receiver",
    version="1.0.0",
    description="A simple webhook receiver service.",
)


@app.post("/webhook")
async def webhook(req: Request):
    """Webhook para receber mensagens da Evolution API.

    Args:
        req (Request): Requisição HTTP contendo o payload do webhook.

    Returns:
        JSONResponse: Resposta HTTP indicando o status do processamento do webhook.
    """
    body = await req.json()
    print("Received webhook payload:")
    # se o corpo da requisição estiver vazio, retorna OK
    if not body:
        return JSONResponse(status_code=HTTPStatus.OK, content={"status": "ok"})
    # se o evento for do tipo messages.upsert (atualizações de mensagens), extrai o remoteJid e a conversa
    if body.get("event") == "messages.upsert":
        data = body.get("data")
        # verifica se o payload contém a chave "key"
        if data and "key" in data:
            conversation, base64_image = None, None
            # obtém o remoteJid (identificador do grupo)
            remote_id = data.get("key").get("remoteJid")
            # verifica se a mensagem contém uma conversa ou uma imagem em base64
            if "conversation" in data.get("message"):
                conversation = data.get("message").get("conversation")
            elif "imageMessage" in data.get("message"):
                base64_image = data.get("message").get("imageMessage").get("base64")
            print(f"Event: {body.get('event')}, Remote ID: {remote_id}")
            print(f"Conversation: {conversation}")
            print(f"Base64 Image: {base64_image}")
            # TODO: Adicionar lógica adicional para processar a conversa ou a imagem conforme necessário.
    return JSONResponse(status_code=HTTPStatus.OK, content={"status": "ok"})


@app.get("/")
async def read():
    return {"status": HTTPStatus.OK, "message": "Service is up and running"}
