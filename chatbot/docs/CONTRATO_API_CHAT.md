# Contrato da API do chat

**Status:** proposta implementada no chatbot; validar com o frontend
(DESENHO_CONVERSAS.md, seção 9).

## `POST /api/chat`

| Item | Valor |
|---|---|
| Autenticação | Opcional. `Authorization: Bearer <JWT>` do tutor. Sem token, apenas FAQ, fora de escopo e boas-vindas. |
| Content-Type | `application/json` |

O JWT é repassado somente ao backend e nunca entra no prompt do modelo.

### Requisição

```json
{
  "mensagem": "Quero marcar um banho pro Thor",
  "historico": [
    {"papel": "tutor", "texto": "oi"},
    {"papel": "assistente", "texto": "Olá! Como posso ajudar?"}
  ],
  "conversaId": "3f2b9c..."
}
```

| Campo | Tipo | Obrigatório | Regras |
|---|---|---|---|
| `mensagem` | string | Sim | 1 a 1000 caracteres, sem ser só espaços. |
| `historico` | lista | Não | Até 20 itens; `papel` é `tutor` ou `assistente`. Serve só de contexto e nunca prova confirmação. |
| `conversaId` | string | Não | Até 64 caracteres. Na primeira mensagem, omitir; reenviar o valor devolvido nas seguintes. |

### Resposta 200

```json
{
  "resposta": "Claro! Para qual dia você quer o banho do Thor?",
  "conversaId": "3f2b9c...",
  "intencao": "CRIAR_AGENDAMENTO",
  "loginNecessario": false,
  "aguardandoConfirmacao": false
}
```

| Campo | Descrição |
|---|---|
| `resposta` | Texto em pt-BR para exibir ao tutor. |
| `conversaId` | Identificador da conversa no servidor do chatbot. |
| `intencao` | `FAQ`, `LISTAR_AGENDAMENTOS`, `CRIAR_AGENDAMENTO`, `CANCELAR_AGENDAMENTO`, `FORA_DE_ESCOPO` ou `INDEFINIDA`. |
| `loginNecessario` | `true` quando o tutor precisa entrar (sem token ou sessão expirada). O frontend pode exibir o botão de login. |
| `aguardandoConfirmacao` | `true` quando há um resumo esperando SIM ou NÃO. O frontend pode exibir botões de atalho. |

Falhas do backend ou do modelo **não** viram erro HTTP: o chatbot responde 200
com uma mensagem útil (DESENHO_CONVERSAS.md, seção 7).

### Erros

Mesmo formato do restante da API:

```json
{"status": 400, "erro": "Dados inválidos", "campos": [{"campo": "mensagem", "mensagem": "..."}]}
```

| Código | Quando |
|---|---|
| 400 | Corpo ausente, mensagem vazia ou longa demais, histórico inválido. |
| 500 | Erro inesperado no chatbot. |
