package com.petcarehub.backend.exceptions;

public class HorarioAgendamentoInvalidoException extends RuntimeException {
    public HorarioAgendamentoInvalidoException() {
        super("Horário de agendamento inválido.");
    }
}