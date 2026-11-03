# Tutorial: executar e testar o backend

Este guia explica como iniciar o backend do PetCare Hub e testar a API pela interface Swagger.

## Pré-requisitos

- Git para clonar o repositório.
- Docker instalado e em execução, com suporte ao comando `docker compose` (por exemplo, Docker Desktop no Windows).
- As portas `8080` e `5432` disponíveis.
- Conexão com a internet na primeira execução, para baixar a imagem do PostgreSQL e as dependências necessárias para compilar a aplicação.

O backend usa Java 17, Spring Boot e PostgreSQL 18. Não é necessário instalar Java ou Gradle na máquina para seguir este guia: o Dockerfile compila e executa a aplicação dentro de containers.

## 1. Clonar o repositório

```powershell
git clone https://github.com/gabriel-guilherme/PetCareHub-TechJunior.git
cd PetCareHub-TechJunior
```

Execute os próximos comandos na raiz do repositório, onde ficam `.env.example` e a pasta `backend`.

## 2. Criar e preencher o `.env`

Copie o arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

Edite `.env` e defina os valores de `POSTGRES_USER`, `POSTGRES_DB` e `POSTGRES_PASSWORD`. O exemplo contém valores apenas para desenvolvimento local; substitua-os conforme necessário.

`JWT_SECRET` deve ser uma chave codificada em Base64 que represente pelo menos 32 bytes. O texto ilustrativo que vem no `.env.example` não é uma chave válida. No PowerShell do Windows, gere uma chave com:

```powershell
$bytes = New-Object byte[] 32
$rng = New-Object System.Security.Cryptography.RNGCryptoServiceProvider
$rng.GetBytes($bytes)
$rng.Dispose()
[Convert]::ToBase64String($bytes)
```

Copie o resultado para `JWT_SECRET` no `.env`, sem aspas. Não compartilhe nem faça commit do `.env`.

## 3. Iniciar os containers

Na raiz do repositório, execute:

```powershell
docker compose --env-file .env -f backend\compose.yaml up --build -d
```

O comando compila a aplicação e inicia o backend e o PostgreSQL em segundo plano. O backend aguarda o healthcheck do PostgreSQL antes de iniciar.

Confira o estado dos serviços:

```powershell
docker compose --env-file .env -f backend\compose.yaml ps
```

Para acompanhar os logs do backend:

```powershell
docker compose --env-file .env -f backend\compose.yaml logs -f backend
```

Quando a aplicação estiver iniciada, abra o Swagger:

- Interface interativa: <http://localhost:8080/swagger-ui/index.html>
- Documento OpenAPI: <http://localhost:8080/v3/api-docs>

## 4. Registrar um tutor e autenticar

No Swagger, use `POST /api/auth/register` para criar um tutor. Exemplo de corpo:

```json
{
  "nome": "Pessoa Avaliadora",
  "email": "avaliador@example.com",
  "telefone": "11999999999",
  "senha": "senha123"
}
```

O nome, e-mail, telefone e senha são obrigatórios; a senha deve ter pelo menos 8 caracteres. Cada e-mail pode ser cadastrado uma única vez.

Em seguida, use `POST /api/auth/login` com o e-mail e a senha cadastrados:

```json
{
  "email": "avaliador@example.com",
  "senha": "senha123"
}
```

Copie o valor do campo `token` da resposta. No botão **Authorize** do Swagger, informe o token (sem escrever `Bearer` antes dele, pois a interface adiciona esse prefixo). O token expira após 60 minutos; faça login novamente para obter outro.

## 5. Testar os recursos da API

- `GET /api/servicos/` é público e pode ser usado para consultar os serviços.
- As operações de pets e agendamentos exigem autenticação. No Swagger, use **Authorize** após fazer login.
- Não há dados de demonstração carregados automaticamente. Para testar um agendamento, crie um serviço e um pet usando os endpoints de criação no Swagger, consulte os horários disponíveis e então crie o agendamento.
- Consulte os modelos de requisição e resposta apresentados pelo próprio Swagger para os campos e formatos aceitos em cada operação.

## 6. Parar os containers

Para parar os serviços sem apagar os dados do banco:

```powershell
docker compose --env-file .env -f backend\compose.yaml down
```

O banco persiste em um volume Docker chamado `postgres_data`. Para apagar também esse volume e todos os dados cadastrados localmente:

```powershell
docker compose --env-file .env -f backend\compose.yaml down -v
```

> **Atenção:** `down -v` apaga permanentemente os dados do banco deste ambiente local.
