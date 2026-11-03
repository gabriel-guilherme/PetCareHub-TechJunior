package com.petcarehub.backend.services;

import org.springframework.stereotype.Service;
import com.petcarehub.backend.repositories.ServicoRepository;
import com.petcarehub.backend.repositories.AgendamentoRepository;
import com.petcarehub.backend.entities.Servico;
import com.petcarehub.backend.entities.Agendamento;
import com.petcarehub.backend.entities.StatusAgendamento;
import com.petcarehub.backend.dtos.servicos.ServicoResponse;
import com.petcarehub.backend.dtos.servicos.CreateServicoRequest;
import com.petcarehub.backend.exceptions.ServicoNaoEncontradoException;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

@Service
public class ServicoService {
    private final ServicoRepository servicoRepository;
    private final AgendamentoRepository agendamentoRepository;

    public ServicoService(ServicoRepository servicoRepository, AgendamentoRepository agendamentoRepository) {
        this.servicoRepository = servicoRepository;
        this.agendamentoRepository = agendamentoRepository;
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

    public List<String> getHorariosLivres(Long servicoId, LocalDate data) {
        servicoRepository.findById(servicoId)
                .orElseThrow(ServicoNaoEncontradoException::new);

        LocalDateTime agora = LocalDateTime.now();
        LocalDate hoje = agora.toLocalDate();
        if (data.isBefore(hoje) || data.getDayOfWeek() == DayOfWeek.SUNDAY) {
            return List.of();
        }

        LocalDateTime inicioDoDia = data.atStartOfDay();
        LocalDateTime inicioDoProximoDia = data.plusDays(1).atStartOfDay();
        Set<LocalTime> horariosOcupados = agendamentoRepository
                .findAllByServico_IdAndDataHoraGreaterThanEqualAndDataHoraLessThanAndStatus(
                        servicoId,
                        inicioDoDia,
                        inicioDoProximoDia,
                        StatusAgendamento.AGENDADO)
                .stream()
                .map(Agendamento::getDataHora)
                .map(LocalDateTime::toLocalTime)
                .collect(Collectors.toSet());

        return java.util.stream.Stream.iterate(LocalTime.of(8, 0), horario -> horario.plusMinutes(30))
                .takeWhile(horario -> horario.isBefore(LocalTime.of(18, 0)))
                .filter(horario -> !horariosOcupados.contains(horario))
                .filter(horario -> !data.equals(hoje) || data.atTime(horario).isAfter(agora))
                .map(LocalTime::toString)
                .toList();
    }
}