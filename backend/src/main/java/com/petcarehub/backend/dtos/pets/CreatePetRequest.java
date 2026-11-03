package com.petcarehub.backend.dtos.pets;

public record CreatePetRequest(
    String nome,
    String especie,
    String raca,
    String dataNascimento
) {}