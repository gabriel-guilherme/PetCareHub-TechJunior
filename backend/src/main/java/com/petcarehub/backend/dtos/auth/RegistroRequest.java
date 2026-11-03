package com.petcarehub.backend.dtos.auth;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record RegistroRequest(
    @NotBlank @Size(max = 120) String nome,
    @NotBlank @Email @Size(max = 254) String email,
    @NotBlank @Size(max = 20) String telefone,
    @NotBlank String senha
) {}