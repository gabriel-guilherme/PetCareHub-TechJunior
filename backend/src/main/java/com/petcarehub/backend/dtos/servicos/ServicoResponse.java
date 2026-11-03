package com.petcarehub.backend.dtos.servicos;

public record ServicoResponse(
    Long id,
    String nome,
    String descricao,
    Double preco
) {}