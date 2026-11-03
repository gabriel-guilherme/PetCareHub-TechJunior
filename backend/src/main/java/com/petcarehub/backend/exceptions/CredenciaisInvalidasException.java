package com.petcarehub.backend.exceptions;

public class CredenciaisInvalidasException extends RuntimeException {
    public CredenciaisInvalidasException() {
        super("Credenciais inválidas. Por favor, verifique seu e-mail e senha.");
    }
}