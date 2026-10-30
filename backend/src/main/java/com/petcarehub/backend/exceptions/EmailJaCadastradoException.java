package com.petcarehub.backend.exceptions;

public class EmailJaCadastradoException extends RuntimeException {
    public EmailJaCadastradoException() {
        super("Já existe um tutor cadastrado com este e-mail.");
    }
}