# Decisões técnicas do chatbot

**Escopo:** MVP completo da trilha de chatbot nos 15 dias, com definição
arquitetural inicial realizada nos dias 1–3.

## Decisão

| Camada | Escolha | Motivo |
|---|---|---|
| Linguagem e runtime | Python 3.11 | Compatível com a imagem leve do serviço e o ecossistema do projeto. |
| API HTTP | FastAPI + Uvicorn | API assíncrona, validação tipada e endpoint simples para integração com o frontend. |
| Orquestração conversacional | LangChain | Integra o modelo com ferramentas controladas para FAQ e intents. |
| Modelo de linguagem | Ollama local, `llama3.2` configurável | Sem cobrança por chamada nem chave de provedor; o modelo roda na máquina local. |
| Configuração | `pydantic-settings` e variáveis de ambiente | Mantém URLs e configuração fora do código. |
| Integração com backend | `httpx.AsyncClient` | Cliente assíncrono para chamar a API Spring Boot e encaminhar o JWT fora do prompt. |
| Testes | `pytest` e `FastAPI TestClient` | Testes sem dependência obrigatória de serviços externos. |
| Execução | Docker Compose com chatbot, Ollama e `ollama-init` | `docker compose up` sobe tudo; o `ollama-init` baixa o modelo na primeira vez e o deixa carregado. GPU NVIDIA opcional via `docker-compose.gpu.yml`. |

## Custo, latência e qualidade

LangChain é adotado para o MVP completo com Ollama local. Não há custo por
chamada nem necessidade de chave de API, mas é necessário baixar os pesos do
modelo, que ocupam armazenamento e consomem memória e CPU/GPU. A imagem do
chatbot não inclui os pesos.

A RNF11 limita a resposta a 10 segundos. Inferência local pode exceder esse
tempo em máquinas com poucos recursos; configurar timeout, limitar o histórico
enviado ao modelo e manter fallback determinístico em pt-BR. Validar o tempo
com o modelo realmente carregado antes da entrega.

O modelo não é fonte da verdade de serviços, preços, duração, horários livres,
agendamentos ou status. Esses dados vêm da API Spring Boot ou de regras
institucionais aprovadas. Em caso de dado ausente ou falha, informar que não
foi possível confirmar em vez de completar por inferência.

## Limites de segurança e ações

- Nunca enviar JWT, chaves ou segredos ao prompt/modelo.
- O JWT é encaminhado pelo cliente HTTP diretamente ao backend, que valida a
  identidade e autorização do tutor (RN03).
- O LLM pode identificar intenções e solicitar ferramentas permitidas; não
  decide autorização e não executa livremente criação ou cancelamento.
- A aplicação mantém estado e confirmação explícita fora do LLM. Apenas uma
  confirmação inequívoca do tutor para o resumo pendente permite iniciar a
  mutação.
- O backend revalida propriedade, disponibilidade, expediente, data futura,
  antecedência de cancelamento e transição de status.
- Tratar timeout e falha do modelo sem declarar sucesso ou executar ações.

Variáveis principais: `LLM_PROVIDER=ollama`, `LLM_MODEL=llama3.2` e
`OLLAMA_BASE_URL=http://ollama:11434`. O serviço `ollama-init` baixa o modelo
no volume `ollama_data` na primeira subida e o carrega na memória antes de o
chatbot iniciar; `OLLAMA_KEEP_ALIVE=-1` mantém o modelo carregado.

Em CPU, os modelos testados não cabem no limite de 6 s do modelo:
`qwen3.5:4b` levou 13–23 s e `llama3.2` (3b) 5–14 s, ambos com boas respostas;
`llama3.2:1b` respondeu em 1–3 s, mas ignorou as regras do prompt. Com GPU
(`docker-compose.gpu.yml` e NVIDIA Container Toolkit), `qwen3.5:4b` respondeu
em menos de 1 s.

## Arquitetura

```text
Frontend
  └── POST /api/chat + Authorization: Bearer <JWT>
        └── FastAPI (validação do contrato e roteamento)
              ├── LangChain (interpretação e escolha limitada de ferramenta)
              │     └── Ollama local (sem JWT/segredos no prompt)
              ├── regras, estado e confirmação determinísticos
              └── cliente HTTP autenticado (JWT fora do LLM)
                    └── API Spring Boot (/api)
```

## Alinhamentos com outras trilhas

1. Confirmar com o backend os DTOs de pets, serviços, agendamentos, horários e
   erros, conforme o contrato REST do documento de requisitos.

## Relação com requisitos e regras

| Requisito/regra | Decisão |
|---|---|
| RN03 / RNF01 | JWT encaminhado; autorização de pets e agendamentos fica no backend. |
| RN05, RN06, RN08, RN10 | O chatbot orienta; API/backend valida e persiste. |
| RF14 | FAQ com regras aprovadas e catálogo atual da API. |
| RF15–RF17 | Consultas e mutações via API; confirmação antes de ação. |
| RF18 | Recusa cordial fora de escopo sem inventar canal de atendimento. |
| RNF02 | Segredos em variáveis de ambiente, nunca em código ou prompt. |
| RNF11 | pt-BR, dados verificáveis, timeout e meta de até 10 segundos. |
| RNF12 | Chatbot, Ollama e download do modelo sobem com `docker compose up`. |
