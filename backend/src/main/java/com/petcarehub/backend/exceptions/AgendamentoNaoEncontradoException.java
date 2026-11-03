package com.petcarehub.backend.exceptions;

public class AgendamentoNaoEncontradoException extends RuntimeException {
    public AgendamentoNaoEncontradoException() {
        super("Agendamento não encontrado.");
    }
}