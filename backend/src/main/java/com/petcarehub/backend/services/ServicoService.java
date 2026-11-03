package com.petcarehub.backend.services;

import org.springframework.stereotype.Service;
import com.petcarehub.backend.repositories.ServicoRepository;
import com.petcarehub.backend.entities.Servico;
import com.petcarehub.backend.dtos.servicos.ServicoResponse;
import com.petcarehub.backend.dtos.servicos.CreateServicoRequest;

import java.util.List;

@Service
public class ServicoService {
    private final ServicoRepository servicoRepository;

    public ServicoService(ServicoRepository servicoRepository) {
        this.servicoRepository = servicoRepository;
    }

    public List<Servico> getAllServicos() {
        return servicoRepository.findAll();
    }

    public ServicoResponse createServico(CreateServicoRequest servico) {
        Servico newServico = new Servico(servico.nome(), servico.descricao(), servico.preco());
        Servico savedServico = servicoRepository.save(newServico);
        return new ServicoResponse(savedServico.getId(), savedServico.getNome(), savedServico.getDescricao(), savedServico.getPreco());
    }

    public void deleteServico(Long id) {
        servicoRepository.deleteById(id);
    }

    
}