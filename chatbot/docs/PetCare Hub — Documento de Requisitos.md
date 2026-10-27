# PetCare Hub — Documento de Requisitos

Oct 18, 2026 · @Filipe Campos

O PetCare Hub é uma plataforma web em que tutores cadastram seus pets, agendam serviços e conversam com um assistente virtual; este documento define o que cada trilha (Design, Frontend, Backend e Chatbot) deve entregar.

## 1. Objetivo e escopo

O desafio avalia cada candidato na sua trilha, a partir de um sistema pequeno e bem definido que as equipes conseguem concluir em uma sprint de 15 dias.

**Dentro do escopo (MVP):**

- Cadastro e login de tutores
- Cadastro, edição, listagem e exclusão de pets
- Consulta ao catálogo de serviços
- Agendamento, listagem e cancelamento de atendimentos
- Assistente virtual (chatbot) integrado à interface

**Fora do escopo:**

- Pagamentos online
- Painel administrativo completo
- Notificações por e-mail ou SMS
- Aplicativo mobile nativo
- Múltiplas unidades ou clínicas

**Stack obrigatória:**
- React (frontend);
- Spring Boot com Java 17 ou superior (backend);
- Banco relacional (H2 ou PostgreSQL);
- Figma (design);
- A tecnologia do chatbot é livre *(sugestão: langchain)*, desde que gratuita e justificada.

## 2. Perfis e regras de negócio

O sistema tem um único perfil de uso, o tutor, e um conjunto fixo de regras que o backend deve impor e o frontend e o chatbot devem respeitar.

| Perfil | Descrição | Permissões |
| --- | --- | --- |
| Visitante | Pessoa sem login | Ver a página inicial, o catálogo de serviços, cadastrar-se e entrar |
| Tutor | Usuário autenticado | Gerenciar os próprios pets e agendamentos e usar o chatbot |

| ID | Regra de negócio |
| --- | --- |
| RN01 | O e-mail do tutor é único no sistema. |
| RN02 | A senha tem no mínimo 8 caracteres e é armazenada com hash (BCrypt). |
| RN03 | Um tutor só vê, edita e cancela seus próprios pets e agendamentos. |
| RN04 | Um pet tem nome, espécie (cão, gato ou outro) e idade em anos, de 0 a 40. |
| RN05 | Um agendamento exige pet, serviço, data e hora, e deve estar no futuro. |
| RN06 | O atendimento funciona de segunda a sábado, das 08h às 18h, em intervalos de 30 minutos; os candidatos podem ajustar esse horário. |
| RN07 | Não pode haver dois agendamentos para o mesmo serviço no mesmo horário. |
| RN08 | O cancelamento só é permitido com pelo menos 2 horas de antecedência. |
| RN09 | Um pet com agendamentos futuros não pode ser excluído. |
| RN10 | Status do agendamento: AGENDADO, CANCELADO ou CONCLUÍDO. |

## 3. Requisitos funcionais

São 18 requisitos funcionais; os de prioridade Alta formam o mínimo para a entrega ser considerada completa.

| ID | Requisito | Prioridade | Trilhas |
| --- | --- | --- | --- |
| RF01 | O visitante pode se cadastrar informando nome, e-mail, telefone e senha. | Alta | Back, Front, Design |
| RF02 | O tutor pode entrar com e-mail e senha e recebe um token JWT. | Alta | Back, Front, Design |
| RF03 | O tutor pode sair do sistema (logout) e a sessão é encerrada no cliente. | Alta | Front |
| RF04 | O tutor pode cadastrar um pet (nome, espécie, raça opcional, idade). | Alta | Back, Front, Design |
| RF05 | O tutor pode listar seus pets. | Alta | Back, Front, Design |
| RF06 | O tutor pode editar os dados de um pet. | Média | Back, Front |
| RF07 | O tutor pode excluir um pet, respeitando a RN09. | Média | Back, Front |
| RF08 | Qualquer visitante pode listar os serviços (nome, descrição, duração, preço). | Alta | Back, Front, Design |
| RF09 | O tutor pode consultar os horários livres de um serviço em uma data. | Alta | Back, Front |
| RF10 | O tutor pode criar um agendamento escolhendo pet, serviço, data e hora. | Alta | Back, Front, Design |
| RF11 | O tutor pode listar seus agendamentos, filtrando por status. | Alta | Back, Front, Design |
| RF12 | O tutor pode cancelar um agendamento, respeitando a RN08. | Alta | Back, Front |
| RF13 | O tutor pode ver o detalhe de um agendamento. | Baixa | Back, Front |
| RF14 | O chatbot responde perguntas frequentes sobre horários, serviços, preços e funcionamento. | Alta | Chatbot |
| RF15 | O chatbot lista os agendamentos do tutor autenticado. | Alta | Chatbot, Back |
| RF16 | O chatbot cria um agendamento a partir da conversa, pedindo os dados que faltarem. | Média | Chatbot, Back |
| RF17 | O chatbot cancela um agendamento mediante confirmação do tutor. | Baixa | Chatbot, Back |
| RF18 | O chatbot recusa educadamente perguntas fora do tema e indica como falar com um atendente humano. | Média | Chatbot |

## 4. Requisitos não funcionais

Estes requisitos valem para todas as trilhas e pesam na avaliação junto com o funcionamento.

| ID | Categoria | Requisito |
| --- | --- | --- |
| RNF01 | Segurança | Endpoints de pets e agendamentos exigem JWT válido; senhas nunca são retornadas pela API. |
| RNF02 | Segurança | Chaves de API e segredos ficam em variáveis de ambiente, nunca no repositório. |
| RNF03 | Validação | Backend e frontend validam os dados; erros voltam em JSON com código HTTP correto (400, 401, 403, 404, 409). |
| RNF04 | Desempenho | Endpoints comuns respondem em até 1 segundo em ambiente local. |
| RNF05 | Usabilidade | Interface responsiva, funcional de 360 px a 1920 px de largura. |
| RNF06 | Acessibilidade | Contraste mínimo AA (4,5:1), campos com rótulo e navegação por teclado nos formulários. |
| RNF07 | Qualidade | Código organizado em camadas (controller, service, repository no back; componentes e serviços no front). |
| RNF08 | Testes | Backend com testes unitários nas regras de negócio RN05 a RN09; frontend com ao menos um teste de componente. |
| RNF09 | Documentação | README com pré-requisitos, passos para executar e decisões técnicas; API documentada com Swagger/OpenAPI. |
| RNF10 | Versionamento | Repositório GitHub da equipe organizado pelo Git Flow (main, develop e branches de feature), com commits frequentes e mensagens claras. |
| RNF11 | Chatbot | Respostas em português do Brasil, em até 10 segundos, e sem inventar horários, preços ou agendamentos. |
| RNF12 | Entrega | Cada equipe de desenvolvimento fornece um ambiente Docker (Dockerfile e docker-compose.yml) que sobe a aplicação completa, com frontend, backend, banco de dados, chatbot e todas as dependências, usando apenas o comando docker compose up e um arquivo .env de exemplo. |

## 5. Modelo de dados

Quatro entidades bastam: um tutor tem vários pets, e cada agendamento liga um pet a um serviço.

| Entidade | Campos | Relacionamentos |
| --- | --- | --- |
| Tutor | id, nome, e-mail (único), telefone, senhaHash, criadoEm | 1 tutor → N pets |
| Pet | id, nome, espécie, raça (opcional), idade, tutorId | N pets → 1 tutor; 1 pet → N agendamentos |
| Serviço | id, nome, descrição, duraçãoMinutos, preço | 1 serviço → N agendamentos |
| Agendamento | id, petId, servicoId, dataHora, status, observação (opcional), criadoEm | N agendamentos → 1 pet e 1 serviço |

O catálogo de serviços deve ser carregado por script na inicialização com ao menos cinco itens, por exemplo banho, tosa, consulta veterinária, vacinação e hospedagem diurna.

## 6. Contrato da API

A API REST usa JSON e prefixo `/api`; este contrato permite que Frontend e Chatbot trabalhem com dados simulados (mock) antes de o backend ficar pronto; qualquer mudança no contrato deve ser combinada entre as trilhas da equipe.

| Método | Rota | Auth | Descrição | Requisito |
| --- | --- | --- | --- | --- |
| POST | /api/auth/register | Não | Cadastra um tutor | RF01 |
| POST | /api/auth/login | Não | Retorna o token JWT | RF02 |
| GET | /api/pets | Sim | Lista os pets do tutor | RF05 |
| POST | /api/pets | Sim | Cadastra um pet | RF04 |
| PUT | /api/pets/{id} | Sim | Edita um pet | RF06 |
| DELETE | /api/pets/{id} | Sim | Exclui um pet | RF07 |
| GET | /api/servicos | Não | Lista os serviços | RF08 |
| GET | /api/servicos/{id}/horarios?data=AAAA-MM-DD | Sim | Lista horários livres | RF09 |
| POST | /api/agendamentos | Sim | Cria um agendamento | RF10 |
| GET | /api/agendamentos?status= | Sim | Lista os agendamentos do tutor | RF11 |
| GET | /api/agendamentos/{id} | Sim | Detalha um agendamento | RF13 |
| PATCH | /api/agendamentos/{id}/cancelar | Sim | Cancela um agendamento | RF12 |

Todo erro retorna um corpo no formato `{"status": 409, "erro": "Horário indisponível", "campos": []}`, em que `campos` lista os erros de validação, quando houver.

## 7. Requisitos por trilha

Cada trilha entrega apenas o que lhe cabe, usando o contrato da API (seção 6) como ponto de encontro.

### Design

- Protótipo navegável no Figma com as telas: login, cadastro, início, meus pets, cadastro de pet, serviços, novo agendamento, meus agendamentos e janela do chat
- Versões mobile (360 px) e desktop (1440 px) das telas principais
- Guia de estilo com paleta (cores primária, secundária, neutras e de erro), tipografia, espaçamento e componentes (botão, campo, cartão, modal)
- Fluxo do usuário do cadastro até o primeiro agendamento
- Estados de interface: vazio, carregando, erro e sucesso
- Entrega: link do Figma com permissão de visualização, um PDF com o guia de estilo e a apresentação do protótipo ao final do dia 3; apenas o design escolhido pela organização será usado pelas equipes de desenvolvimento

### Frontend (React)

- Aplicação em React 18 ou superior, com Vite, rotas (React Router) e componentes reutilizáveis
- Telas de login, cadastro, pets, serviços, novo agendamento e meus agendamentos (RF01 a RF13), seguindo o design escolhido pela organização
- Rotas protegidas: sem token, o usuário é levado ao login
- Consumo de dados simulados (mock) que seguem o contrato da API, enquanto o backend não está pronto; a troca pela API real é feita na integração, entre os dias 10 e 12
- Formulários com validação e mensagens de erro claras; indicadores de carregamento
- Widget de chat fixo no canto da tela, que envia mensagens ao endpoint do chatbot
- Entrega: repositório com README e instruções para executar

### Backend (Spring Boot)

- API REST em Spring Boot 3 com Java 17 ou superior, Spring Data JPA e Spring Security
- Todos os endpoints da seção 6, com as regras RN01 a RN10
- Autenticação com JWT e senhas com BCrypt
- Tratamento global de exceções e validação com Bean Validation
- Banco H2 ou PostgreSQL, com carga inicial dos serviços
- Documentação Swagger/OpenAPI e testes unitários das regras de negócio
- Entrega: repositório com README e o Dockerfile do serviço, que compõe o ambiente Docker da equipe (RNF12)

### Chatbot

- Serviço que recebe `POST /api/chat` com a mensagem e o histórico e devolve a resposta em texto
- Responde dúvidas frequentes (RF14) com base nos dados reais de serviços, horários e preços
- Consulta e cria agendamentos chamando a API do backend em nome do tutor autenticado (RF15 a RF17)
- Pede confirmação antes de criar ou cancelar qualquer agendamento
- Tem limites claros de escopo (RF18) e trata falhas da API sem travar a conversa
- Abordagem livre, desde que sem custo: regras e fluxos, NLU open source (Rasa) ou LLM em plano gratuito ou modelo local (Ollama, por exemplo); a organização não fornece chaves de API; o candidato justifica a escolha no README
- Entrega: repositório, README com a arquitetura escolhida e um roteiro de ao menos 10 conversas de teste

## 8. Critérios de avaliação

Cada trilha é avaliada de 0 a 100 pontos, com o funcionamento e a aderência aos requisitos valendo mais que os extras.

| Critério | Design | Frontend | Backend | Chatbot |
| --- | --- | --- | --- | --- |
| Atendimento aos requisitos de Alta prioridade | 30 | 30 | 30 | 30 |
| Funcionamento (sobe com docker compose up, sem erros, seguindo o README) | n/a | 20 | 20 | 20 |
| Qualidade e organização do código ou do arquivo Figma | 20 | 15 | 20 | 15 |
| Usabilidade, acessibilidade e consistência visual | 30 | 15 | n/a | 10 |
| Validações, segurança e tratamento de erros | n/a | 5 | 15 | 15 |
| Documentação (README, Swagger, guia de estilo) | 10 | 10 | 10 | 5 |
| Extras (testes, deploy, criatividade) | 10 | 5 | 5 | 5 |
| **Total** | **100** | **100** | **100** | **100** |

**Trilha de Design:** as duplas são avaliadas por criatividade, usabilidade, consistência e aderência às regras de design. O design usado como base não é necessariamente o mais bem avaliado: a organização escolhe o mais viável de implementar no prazo da sprint.

## 9. Metodologia, equipes e cronograma

O desafio segue o Scrum em uma única sprint de 15 dias: o design só bloqueia o frontend, então backend e chatbot trabalham em paralelo desde o dia 1, seguindo o contrato da API (seção 6).

Nos dias 1 a 3, as 4 duplas de design trabalham separadamente e apresentam seus protótipos ao final do dia 3; a organização escolhe o design mais viável de implementar no prazo, que serve de base para todas as equipes. Os marcos de acompanhamento são a apresentação dos designs (dia 3), o frontend com dados simulados (dia 9) e a integração funcionando (dia 12). A entrevista técnica com cada candidato ocorre depois do dia 15.

| Dias | Frontend | Backend | Chatbot |
| --- | --- | --- | --- |
| 1 a 3 | Esqueleto React, rotas e componentes base | Esqueleto Spring Boot, banco, entidades e JWT | Escolha da tecnologia e desenho das conversas |
| 4 a 9 | Telas do design escolhido, com dados simulados | Endpoints e regras de negócio do contrato, com testes | Fluxos de FAQ e de agendamento, seguindo o contrato |
| 10 a 12 | Troca dos dados simulados pela API real | Correções reveladas pela integração | Widget de chat integrado à interface |
| 13 a 15 | Ajustes, documentação e Docker | Ajustes, documentação e Docker | Ajustes, roteiro de testes e Docker |

**Equipes**

| Grupo | Formação |
| --- | --- |
| Design | 4 duplas (8 pessoas), que trabalham separadamente e apresentam seus designs ao final do dia 3 |
| Desenvolvimento | 4 equipes de 8 pessoas (32), cada uma com 2 a 3 em backend, 2 a 3 em frontend e 2 a 3 em chatbot; a divisão exata (3+3+2 em alguma ordem) depende das inscrições por trilha |
| Total | 40 candidatos |

**Rotina e comunicação**

- Reunião de acompanhamento com cada equipe a cada 2 dias
- Comunicação oficial pelo Discord
- Um repositório no GitHub por equipe, organizado pelo Git Flow, com as pastas frontend/, backend/ e chatbot/
- A participação é critério eliminatório
- Cada candidato é avaliado individualmente, mas o trabalho em equipe também conta

**Custos:** o desafio deve ser totalmente gratuito. Figma, GitHub, Discord, banco de dados local e as ferramentas do chatbot precisam ter plano gratuito ou ser de código aberto, e a organização não fornece chaves de API.

**Entrega técnica:** cada equipe de desenvolvimento entrega um ambiente Docker que roda a aplicação completa com todas as dependências, para que a organização execute e avalie tudo com um único comando (RNF12).
