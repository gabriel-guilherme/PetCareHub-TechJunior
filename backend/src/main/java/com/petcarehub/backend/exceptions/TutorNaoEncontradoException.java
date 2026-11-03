package com.petcarehub.backend.exceptions;

public class TutorNaoEncontradoException extends RuntimeException {
    public TutorNaoEncontradoException() {
        super("Tutor não encontrado.");
    }
}