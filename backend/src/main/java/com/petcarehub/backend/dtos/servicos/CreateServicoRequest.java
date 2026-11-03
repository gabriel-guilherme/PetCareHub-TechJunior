package com.petcarehub.backend.dtos.servicos;

public record CreateServicoRequest(
    String nome,
    String descricao,
    Double preco
) {}