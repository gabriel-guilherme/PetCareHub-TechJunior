package com.petcarehub.backend.exceptions;

public class CancelamentoNaoPermitidoException extends RuntimeException {
    public CancelamentoNaoPermitidoException() {
        super("Cancelamento não permitido.");
    }
}