package com.petcarehub.backend.dtos.agendamentos;

public record CreateAgendamentoRequest(
    Long servicoId,
    Long petId,
    String dataHora
) {}