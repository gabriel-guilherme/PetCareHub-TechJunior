package com.petcarehub.backend.controllers;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.http.ResponseEntity;
import com.petcarehub.backend.services.AgendamentoService;
import java.util.List;
import com.petcarehub.backend.dtos.agendamentos.AgendamentoResponse;
import org.springframework.web.bind.annotation.RequestBody;
import com.petcarehub.backend.dtos.agendamentos.CreateAgendamentoRequest;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import com.petcarehub.backend.entities.StatusAgendamento;
import org.springframework.web.bind.annotation.RequestParam;

@RestController
@RequestMapping("/api/agendamentos")
public class AgendamentosController {
    private final AgendamentoService agendamentoService;

    public AgendamentosController(AgendamentoService agendamentoService) {
        this.agendamentoService = agendamentoService;
    }

    @PostMapping("/")
    public ResponseEntity<AgendamentoResponse> createAgendamento(@RequestBody CreateAgendamentoRequest request, @AuthenticationPrincipal Jwt jwt) {
        Long tutorId = Long.valueOf(jwt.getSubject());
        AgendamentoResponse agendamentoResponse = agendamentoService.createAgendamento(request, tutorId);
        return ResponseEntity.ok(agendamentoResponse);
    }

    @GetMapping("/")
    public ResponseEntity<List<AgendamentoResponse>> getAllAgendamentos(@AuthenticationPrincipal Jwt jwt, @RequestParam(required = false) StatusAgendamento status) {
        Long tutorId = Long.valueOf(jwt.getSubject());

        List<AgendamentoResponse> agendamentos =  agendamentoService.getAllAgendamentosByTutorId(tutorId, status);

        return ResponseEntity.ok(agendamentos);
    }

    @GetMapping("/{id}")
    public ResponseEntity<AgendamentoResponse> getAgendamentoById(@PathVariable Long id, @AuthenticationPrincipal Jwt jwt) {
        Long tutorId = Long.valueOf(jwt.getSubject());
        AgendamentoResponse agendamentoResponse = agendamentoService.getAgendamentoById(id, tutorId);
        return ResponseEntity.ok(agendamentoResponse);
    }

    @PatchMapping("/{id}/cancelar")
    public ResponseEntity<AgendamentoResponse> cancelarAgendamento(@PathVariable Long id, @AuthenticationPrincipal Jwt jwt) {
        Long tutorId = Long.valueOf(jwt.getSubject());
        AgendamentoResponse agendamentoResponse = agendamentoService.cancelarAgendamento(id, tutorId);
        return ResponseEntity.ok(agendamentoResponse);
    }
}