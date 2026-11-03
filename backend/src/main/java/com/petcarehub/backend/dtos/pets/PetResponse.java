package com.petcarehub.backend.dtos.pets;

public record PetResponse(
    Long id,
    String nome,
    String especie,
    String raca,
    String dataNascimento,
    int idade
) {}