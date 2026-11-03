package com.petcarehub.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import com.petcarehub.backend.entities.Servico;

public interface ServicoRepository extends JpaRepository<Servico, Long> {
}