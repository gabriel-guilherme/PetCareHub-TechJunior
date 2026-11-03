package com.petcarehub.backend.exceptions;

public class PetNaoEncontradoException extends RuntimeException {
    public PetNaoEncontradoException() {
        super("Pet não encontrado.");
    }
}