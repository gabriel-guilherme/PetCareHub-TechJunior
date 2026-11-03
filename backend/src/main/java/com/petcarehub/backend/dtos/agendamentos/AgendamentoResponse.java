package com.petcarehub.backend.dtos.agendamentos;

public record AgendamentoResponse(
    Long id,
    String tutorNome,
    String petNome,
    String servicoNome,
    String dataHora,
    String status
) {}