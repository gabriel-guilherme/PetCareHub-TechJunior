# PetCare Hub — Chatbot

Assistente virtual do PetCare Hub: uma API em FastAPI que usa LangChain e um modelo local servido pelo Ollama. Este guia sobe o projeto com Docker, com ou sem GPU.

## 1. Pré-requisitos

**Nos dois modos:**

- Docker com o plugin Compose (`docker compose version` deve responder).
- Internet na primeira subida, para baixar o modelo `llama3.2` (cerca de 2 GB).
- Cerca de 4 GB de memória livre para o modelo.

**Só no modo GPU:**

- Placa NVIDIA com o driver instalado (`nvidia-smi` deve listar a placa) e cerca de 4 GB de VRAM.
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) instalado e configurado no Docker:

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Para confirmar que o Docker enxerga a GPU:

```bash
docker run --rm --gpus all ubuntu nvidia-smi
```

O comando deve mostrar a mesma tabela do `nvidia-smi` da máquina.

## 2. Criar o `.env`

Todos os comandos deste guia rodam dentro da pasta `chatbot/`. O `.env` é obrigatório: sem ele, o Compose não sobe.

```bash
cd chatbot
cp .env.example .env
```

Depois, edite o `.env` e troque esta linha:

```env
BACKEND_MOCK=true
```

Esse é o único ajuste necessário para rodar. O `.env` fica fora do Git, e a [seção 6](#6-entendendo-o-env) explica cada variável.

## 3. Subir o projeto

Escolha um dos modos. O de GPU só acrescenta a placa ao serviço `ollama`; o resto é igual.

### Sem GPU (CPU)

```bash
docker compose up -d --build
```

Use em máquinas sem placa NVIDIA. O modelo fica mais lento, então vale aumentar os limites de tempo no `.env` antes de subir:

```env
LLM_TIMEOUT_SECONDS=30
TEMPO_MAXIMO_RESPOSTA_SECONDS=35
```

Se ainda assim demorar, defina `LLM_REDACAO=false` para responder só com as mensagens padrão.

### Com GPU (NVIDIA)

```bash
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d --build
```

Para confirmar que o modelo está na placa:

```bash
docker compose exec ollama ollama ps
```

A coluna `PROCESSOR` deve mostrar `100% GPU`. Se mostrar `100% CPU`, o `ollama` não recebeu a GPU.

### O que acontece na subida

A primeira subida demora alguns minutos por causa do download do modelo, que fica salvo no volume `ollama_data`. A API só começa a responder depois que o modelo estiver carregado. Para acompanhar:

```bash
docker compose logs -f ollama-init chatbot
```

| Serviço | Papel |
|---|---|
| `ollama` | Servidor do modelo. Só é acessível de dentro da rede do Compose. |
| `ollama-init` | Baixa o modelo, se preciso, e o carrega na memória. Termina sozinho. |
| `chatbot` | API em `http://localhost:8001`. |

## 4. Testar

```bash
curl http://localhost:8001/health
```

```json
{"status": "ok"}
```

Uma pergunta geral, sem login:

```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"mensagem": "Qual o horário de funcionamento?"}'
```

Uma consulta como tutor logado. A API simulada aceita os tokens `token-tutor-1` e `token-tutor-2`:

```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token-tutor-1" \
  -d '{"mensagem": "Quais são meus agendamentos?"}'
```

A documentação interativa fica em `http://localhost:8001/docs`.

## 5. Comandos do dia a dia

| Ação | Comando |
|---|---|
| Ver o estado dos serviços | `docker compose ps -a` |
| Ver os logs do chatbot | `docker compose logs -f chatbot` |
| Parar tudo | `docker compose down` |
| Parar e apagar o modelo baixado | `docker compose down -v` |

Esses comandos servem para os dois modos. Já o `up` precisa ser repetido com os mesmos arquivos: rodar `docker compose up -d` sem o `docker-compose.gpu.yml` recria o `ollama` em CPU.

## 6. Entendendo o `.env`

Depois de editar o `.env`, rode de novo o `up` do seu modo. O `docker compose restart` não aplica as mudanças.

### Backend

| Variável | Valor no `.env.example` | O que faz |
|---|---|---|
| `BACKEND_MOCK` | `false` | `true` usa a API simulada em memória, com serviços, pets e agendamentos de exemplo. `false` chama o backend real em `BACKEND_API_URL`. |
| `BACKEND_API_URL` | `http://backend:8080/api` | URL da API Spring Boot, com o prefixo `/api`. Só é usada com `BACKEND_MOCK=false`. |
| `BACKEND_TIMEOUT_SECONDS` | `3` | Limite de cada chamada ao backend. |

Use `BACKEND_MOCK=true` por enquanto. O `backend/compose.yaml` roda em outra rede Docker e não publica a porta da API, então o endereço padrão não resolve a partir do container do chatbot.

### Modelo

| Variável | Valor no `.env.example` | O que faz |
|---|---|---|
| `LLM_MODEL` | `llama3.2` | Modelo do Ollama. Ao trocar, o `up` baixa o novo modelo. |
| `OLLAMA_BASE_URL` | `http://ollama:11434` | Endereço do Ollama visto de dentro do container. Não precisa mudar. |
| `LLM_REDACAO` | `true` | `false` desliga a reescrita pelo modelo e responde só com as mensagens padrão. |
| `LLM_TIMEOUT_SECONDS` | `15` | Limite de cada chamada ao modelo. |
| `TEMPO_MAXIMO_RESPOSTA_SECONDS` | `20` | Prazo total da resposta. A reescrita só roda se ainda houver tempo. |

Quando o modelo estoura o tempo, o chatbot continua respondendo: a intenção é classificada por palavras-chave e a resposta sai na mensagem padrão.

### Textos e fuso

| Variável | Valor no `.env.example` | O que faz |
|---|---|---|
| `HORARIO_FUNCIONAMENTO` | `de segunda a sábado, das 8h às 18h, com horários a cada 30 minutos` | Horário informado ao tutor. |
| `CANAL_ATENDIMENTO_HUMANO` | `procure a recepção do PetCare Hub` | Orientação incluída na resposta quando o assunto foge do escopo do chatbot. |
| `TIMEZONE` | `America/Sao_Paulo` | Fuso usado para interpretar datas e horários. |

### Variáveis sem efeito hoje

| Variável | Motivo |
|---|---|
| `LLM_PROVIDER` | O código só usa o Ollama. |
| `LLM_API_KEY` | Modelo local não precisa de chave. Deixe vazia. |
| `PORT` | O Compose fixa a porta interna em `8001`. Para mudar a porta da máquina, use `CHATBOT_HOST_PORT`. |
