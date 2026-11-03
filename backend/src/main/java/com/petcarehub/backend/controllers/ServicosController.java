package com.petcarehub.backend.controllers;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.http.ResponseEntity;
import com.petcarehub.backend.services.ServicoService;
import java.util.List;
import com.petcarehub.backend.entities.Servico;
import com.petcarehub.backend.dtos.servicos.ServicoResponse;
import org.springframework.web.bind.annotation.RequestBody;
import com.petcarehub.backend.dtos.servicos.CreateServicoRequest;

@RestController
@RequestMapping("/api/servicos")
public class ServicosController {
    private final ServicoService servicoService;

    public ServicosController(ServicoService servicoService) {
        this.servicoService = servicoService;
    }

    @GetMapping("/")
    public ResponseEntity<List<ServicoResponse>> getAllServicos() {
        List<Servico> servicos = servicoService.getAllServicos();
        List<ServicoResponse> response = servicos.stream()
                .map(servico -> new ServicoResponse(servico.getId(), servico.getNome(), servico.getDescricao(), servico.getPreco()))
                .toList();
        return ResponseEntity.ok(response);
    }

    @PostMapping("/")
    public ResponseEntity<ServicoResponse> createServico(@RequestBody CreateServicoRequest servico) {
        ServicoResponse response = servicoService.createServico(servico);
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteServico(@PathVariable Long id) {
        servicoService.deleteServico(id);
        return ResponseEntity.noContent().build();
    }
}