package com.petcarehub.backend.dtos.pets;

public record UpdatePetRequest(
    String nome,
    String especie,
    String raca,
    String dataNascimento
) {}