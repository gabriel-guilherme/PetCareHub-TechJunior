"""Mensagens padrão do chatbot (DESENHO_CONVERSAS.md, seção 6).

Os campos entre chaves são preenchidos apenas com dados da API ou da
configuração.
"""

BOAS_VINDAS = (
    "Olá! Posso tirar dúvidas sobre serviços, preços e horários, mostrar seus "
    "agendamentos, marcar ou cancelar um atendimento. Como posso ajudar?"
)
LOGIN_NECESSARIO = (
    "Para ver ou alterar agendamentos, você precisa entrar na sua conta."
)
SESSAO_EXPIRADA = "Sua sessão expirou. Entre novamente para continuar."
SEM_PETS = (
    "Não encontrei pets cadastrados na sua conta. Cadastre um pet em Meus pets "
    "e depois volte aqui."
)
SEM_AGENDAMENTOS = (
    "Não encontrei agendamentos na sua conta. Quer marcar um atendimento?"
)
SEM_HORARIOS = (
    "Não há horários livres para {servico} em {data}. Quer tentar outro dia?"
)
CONFIRMAR_CRIACAO = (
    "Confirma o agendamento de {pet} para {servico} em {data}, às {hora}{preco}? "
    "Responda SIM para confirmar ou NÃO para desistir."
)
CONFIRMAR_CANCELAMENTO = (
    "Confirma o cancelamento de {servico} para {pet} em {data}, às {hora}? "
    "Responda SIM para confirmar ou NÃO para desistir."
)
ACAO_DESCARTADA = (
    "Tudo bem, não fiz nenhuma alteração. Posso ajudar com mais alguma coisa?"
)
CONFIRMACAO_EXPIRADA = (
    "O pedido de confirmação expirou e nada foi alterado. Quer começar de novo?"
)
CANCELAMENTO_FORA_DO_PRAZO = (
    "Esse agendamento começa em menos de 2 horas e não pode mais ser cancelado "
    "pelo sistema. Para falar com um atendente, {canal}."
)
FORA_DE_ESCOPO = (
    "Esse assunto eu não consigo responder. Posso ajudar com serviços, preços, "
    "horários e agendamentos do PetCare Hub. Para falar com um atendente, {canal}."
)
FALHA_BACKEND = (
    "Não consegui consultar o sistema agora. Tente novamente em alguns instantes."
)
