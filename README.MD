# Evolution API - Projeto de Integração WhatsApp

Este projeto fornece uma integração completa com a Evolution API v2.3.7 para envio de mensagens e mídias via WhatsApp utilizando Python.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como Subir o Projeto](#como-subir-o-projeto)
- [Arquivo de Teste](#arquivo-de-teste)
- [Documentação](#documentação)
- [Solução de Problemas](#solução-de-problemas)

## 🎯 Visão Geral

Este projeto utiliza Docker Compose para orquestrar três serviços principais:

- **Evolution API**: API para integração com WhatsApp
- **PostgreSQL**: Banco de dados para persistência
- **Redis**: Cache e gerenciamento de filas

## 📁 Estrutura do Projeto

```
evolution/
├── docker-compose.yml    # Configuração dos containers Docker
├── evotest.py           # Funções para envio de mensagens e arquivos
├── filetypes.py         # Definição de tipos de mídia e MIME types
├── webhook.py           # Handler para webhooks da Evolution API
├── .env                 # Variáveis de ambiente (criar)
└── README.MD            # Este arquivo
```

### Descrição dos Arquivos

#### `docker-compose.yml`

Arquivo de orquestração dos containers Docker que define:

- **evolution-api**: Container principal da API na porta 8080
  - Imagem: evoapicloud/evolution-api:v2.3.7
  - Volume: `evolution_instances` para persistência de instâncias
  - Dependências: PostgreSQL e Redis

- **postgres**: Banco de dados PostgreSQL 17
  - Porta: 5432
  - Configurado para suportar até 1000 conexões simultâneas
  - Volume: `postgres_data` para persistência dos dados

- **redis**: Cache Redis
  - Porta: 6379
  - Persistência habilitada (appendonly)
  - Volume: `redis` para dados persistentes

#### `evotest.py`

Script Python com funções para interagir com a Evolution API:

- `send_text(message, contact)`: Envia mensagens de texto
- `send_file_url(url_file, contact, ...)`: Envia arquivos via URL (imagens, documentos, etc)
- `send_file(path, contact, ...)`: Envia arquivos locais em base64
- `file_to_base64(path)`: Função auxiliar para converter arquivos em base64

#### `filetypes.py`

Define os tipos de mídia suportados e seus MIME types:

- **PDF**: `Type("document", "application/pdf")`
- **XLSX**: `Type("document", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")`
- **PNG**: `Type("image", "image/png")`
- **JPEG/JPG**: `Type("image", "image/jpeg")`

#### `webhook.py`

Handler para processar webhooks recebidos da Evolution API (para eventos em tempo real).

## 🔧 Pré-requisitos

- Docker Desktop instalado ([Download](https://www.docker.com/products/docker-desktop))
- Docker Compose (geralmente incluído no Docker Desktop)
- Python 3.8+ (para executar o arquivo de teste)
- Biblioteca `requests` do Python: `pip install requests`

## ⚙️ Instalação e Configuração

### 1. Clone ou baixe o projeto

```bash
cd "c:\Users\renan\Python Projects\MyProjects\evolutionAPI"
```

### 2. Crie o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# PostgreSQL
POSTGRES_PASSWORD=sua_senha_segura

# Evolution API - Configurações básicas
SERVER_URL=http://localhost:8080
DEL_INSTANCE=false

# Autenticação
AUTHENTICATION_TYPE=apikey
AUTHENTICATION_API_KEY=sua-chave-api-segura
AUTHENTICATION_EXPOSE_IN_FETCH_INSTANCES=true

# Database
DATABASE_ENABLED=true
DATABASE_PROVIDER=postgresql
DATABASE_CONNECTION_URI=postgresql://postgres:sua_senha_segura@postgres:5432/evolution
DATABASE_CONNECTION_CLIENT_NAME=evolution_exchange

# Redis
CACHE_REDIS_ENABLED=true
CACHE_REDIS_URI=redis://redis:6379/1
CACHE_REDIS_PREFIX_KEY=evolution
CACHE_LOCAL_ENABLED=false

# Nome da instância (usado no evotest.py)
INSTANCE_NAME=nome-da-sua-instancia
```

> ⚠️ **Importante**: Substitua `sua_senha_segura` e `sua-chave-api-segura` por valores seguros!

## 🚀 Como Subir o Projeto

### Iniciando os containers

1. Abra um terminal na pasta do projeto

2. Inicie os containers:

```bash
docker-compose up -d
```

3. Verifique se os containers estão rodando:

```bash
docker-compose ps
```

Você deve ver 3 containers em execução:

- `evolution_api`
- `postgres`
- `redis`

### Acessando a interface de gerenciamento

Após subir os containers, acesse:

- **Manager**: http://localhost:8080/manager
- **API Docs**: http://localhost:8080/docs

### Criar uma instância

1. Acesse http://localhost:8080/manager
2. Clique em "Criar Instância"
3. Configure o nome da instância (use o mesmo do `.env`)
4. Conecte com o QR Code do WhatsApp

### Parando os containers

```bash
docker-compose down
```

Para parar e remover os volumes (apaga todos os dados):

```bash
docker-compose down -v
```

## 🧪 Exemplos de Uso

### Configuração Inicial

As variáveis de ambiente são carregadas do arquivo `.env`:

```python
from evotest import send_text, send_file, send_file_url
```

### 1. Enviar mensagem de texto

```python
send_text("Olá, mundo!", "5511999999999")
```

**Parâmetros:**

- `message` (str): Texto da mensagem
- `contact` (str): Número do destinatário (formato internacional)

### 2. Enviar arquivo via URL

```python
from filetypes import FileTypes

send_file_url(
    url_file="https://example.com/documento.pdf",
    contact="5511999999999",
    mediatype=FileTypes.PDF.mediatype,
    mimetype=FileTypes.PDF.mimetype,
    caption="Documento importante",
    filename="documento.pdf"
)
```

**Parâmetros:**

- `url_file` (str): URL do arquivo a enviar
- `contact` (str): Número do destinatário
- `mediatype` (str): Tipo de mídia (document, image, etc)
- `mimetype` (str): MIME type do arquivo
- `caption` (str): Legenda/descrição do arquivo
- `filename` (str): Nome que aparecerá no WhatsApp

### 3. Enviar arquivo local

```python
from filetypes import FileTypes

send_file(
    path="./seu-arquivo.png",
    contact="5511999999999",
    caption="Foto da empresa",
    mediatype=FileTypes.PNG.mediatype,
    mimetype=FileTypes.PNG.mimetype
)
```

**Parâmetros:**

- `path` (str): Caminho local do arquivo
- `contact` (str): Número do destinatário
- `caption` (str): Legenda do arquivo
- `mediatype` (str): Tipo de mídia
- `mimetype` (str): MIME type do arquivo

### 4. Converter arquivo para base64

```python
from evotest import file_to_base64

encoded = file_to_base64("./imagem.jpg")
print(encoded)  # String base64 do arquivo
```

## 🧪 Arquivo de Teste

O arquivo `evotest.py` contém exemplos práticos de uso da API.

### Configuração

Antes de executar, configure as variáveis de ambiente ou edite diretamente no arquivo:

```python
headers = {
    "apiKey": "sua-chave-api-segura",  # Mesma do .env
}
instance = "nome-da-sua-instancia"     # Mesma do .env
```

### Como executar

```bash
python evotest.py
```

> 💡 **Dica**: Utilize as funções importando do arquivo:

```python
from evotest import send_text, send_file, send_file_url, file_to_base64
```

## 📚 Documentação

### Documentação Oficial

- **Postman Collection**: https://www.postman.com/agenciadgcode/evolution-api/collection/nm0wqgt/evolution-api-v2-3
- **Documentação Oficial**: https://doc.evolution-api.com/v2/pt/get-started/introduction

### Recursos Auxiliares

1. **PyCodeBr**: https://pickle-reading-bd9.notion.site/py_live-046-1fd9956f3dc980a49b79cc9669404a89
2. **GitHub da Evolution**: https://github.com/EvolutionAPI/evolution-api
3. **Discord**: https://discord.gg/evolution-api

## 🔍 Solução de Problemas

### Container não inicia

```bash
# Ver logs
docker-compose logs evolution-api
docker-compose logs postgres
```

### Erro de conexão com banco

- Verifique se a senha no `.env` está correta
- Confirme que o PostgreSQL está rodando: `docker-compose ps`

### Erro 401 (Unauthorized)

- Verifique se a `AUTHENTICATION_API_KEY` está correta
- Confirme se a chave no `evotest.py` é a mesma do `.env`

### Instância não conecta

- Acesse o manager e gere um novo QR Code
- Verifique os logs: `docker-compose logs -f evolution-api`

### Porta já em uso

Se a porta 8080 já estiver em uso, edite o `docker-compose.yml`:

```yaml
ports:
  - "8081:8080" # Mude 8080 para outra porta
```

## 📝 Notas Importantes

- Os dados são persistidos em volumes Docker
- Sempre use números no formato internacional (ex: 5511999999999)
- A API Key deve ser mantida em segredo
- Faça backup do arquivo `.env`

## 🤝 Contribuindo

Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias!

---

**Desenvolvido para facilitar a integração com WhatsApp via Evolution API** 🚀
