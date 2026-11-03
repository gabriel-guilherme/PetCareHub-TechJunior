package com.petcarehub.backend.exceptions;

public class ServicoNaoEncontradoException extends RuntimeException {
    public ServicoNaoEncontradoException() {
        super("Serviço não encontrado.");
    }
}
