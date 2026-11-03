package com.petcarehub.backend.dtos.auth;

public record TutorResponse(
    Long id,
    String nome,
    String email,
    String telefone
) {}