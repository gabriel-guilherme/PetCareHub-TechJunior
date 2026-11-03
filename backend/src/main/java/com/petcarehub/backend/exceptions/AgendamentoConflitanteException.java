package com.petcarehub.backend.exceptions;

public class AgendamentoConflitanteException extends RuntimeException {
    public AgendamentoConflitanteException() {
        super("Agendamento conflitante.");
    }
}