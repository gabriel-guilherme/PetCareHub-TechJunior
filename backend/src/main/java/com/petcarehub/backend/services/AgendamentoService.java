package com.petcarehub.backend.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.petcarehub.backend.repositories.AgendamentoRepository;
import com.petcarehub.backend.repositories.PetRepository;
import com.petcarehub.backend.repositories.ServicoRepository;
import com.petcarehub.backend.entities.Agendamento;
import com.petcarehub.backend.entities.Pet;
import com.petcarehub.backend.entities.Servico;
import com.petcarehub.backend.entities.StatusAgendamento;
import com.petcarehub.backend.dtos.agendamentos.CreateAgendamentoRequest;
import com.petcarehub.backend.dtos.agendamentos.AgendamentoResponse;
import com.petcarehub.backend.exceptions.PetNaoEncontradoException;
import com.petcarehub.backend.exceptions.ServicoNaoEncontradoException;
import com.petcarehub.backend.exceptions.AgendamentoNaoEncontradoException;
import com.petcarehub.backend.exceptions.CancelamentoNaoPermitidoException;
import com.petcarehub.backend.exceptions.HorarioAgendamentoInvalidoException;
import com.petcarehub.backend.exceptions.AgendamentoConflitanteException;

import java.util.List;
import java.time.Clock;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.DayOfWeek;
import java.time.format.DateTimeParseException;

@Service
public class AgendamentoService {
    private final AgendamentoRepository agendamentoRepository;
    private final PetRepository petRepository;
    private final ServicoRepository servicoRepository;
    private final Clock clock;

    @Autowired
    public AgendamentoService(
            AgendamentoRepository agendamentoRepository,
            PetRepository petRepository,
            ServicoRepository servicoRepository) {
        this(agendamentoRepository, petRepository, servicoRepository, Clock.systemDefaultZone());
    }

    AgendamentoService(
            AgendamentoRepository agendamentoRepository,
            PetRepository petRepository,
            ServicoRepository servicoRepository,
            Clock clock) {
        this.agendamentoRepository = agendamentoRepository;
        this.petRepository = petRepository;
        this.servicoRepository = servicoRepository;
        this.clock = clock;
    }

    @Transactional
    public AgendamentoResponse createAgendamento(CreateAgendamentoRequest request, Long tutorId) {
        if (request.petId() == null) {
            throw new PetNaoEncontradoException();
        }
        Pet pet = petRepository.findByIdAndTutor_Id(request.petId(), tutorId)
                .orElseThrow(() -> new PetNaoEncontradoException());

        if (request.servicoId() == null) {
            throw new ServicoNaoEncontradoException();
        }
        Servico servico = servicoRepository.findById(request.servicoId())
                .orElseThrow(() -> new ServicoNaoEncontradoException());

        LocalDateTime dataHora;
        try {
            if (request.dataHora() == null || request.dataHora().isBlank()) {
                throw new HorarioAgendamentoInvalidoException();
            }
            dataHora = LocalDateTime.parse(request.dataHora());
        } catch (DateTimeParseException exception) {
            throw new HorarioAgendamentoInvalidoException();
        }

        LocalTime horario = dataHora.toLocalTime();

        boolean foraDoExpediente =
                horario.isBefore(LocalTime.of(8, 0))
                || horario.isAfter(LocalTime.of(17, 30));

        boolean domingo = dataHora.getDayOfWeek() == DayOfWeek.SUNDAY;

        boolean minutoInvalido =
                horario.getMinute() != 0 && horario.getMinute() != 30;

        boolean temSegundosOuNanos =
                horario.getSecond() != 0 || horario.getNano() != 0;

        boolean dataHoraInvalida = !dataHora.isAfter(LocalDateTime.now(clock));

        if (domingo || foraDoExpediente || minutoInvalido || temSegundosOuNanos || dataHoraInvalida) {
            throw new HorarioAgendamentoInvalidoException();
        }

        boolean horarioOcupado =
                agendamentoRepository.existsByServico_IdAndDataHoraAndStatus(servico.getId(), dataHora, StatusAgendamento.AGENDADO);

        if (horarioOcupado) {
                throw new AgendamentoConflitanteException();
        }

        Agendamento agendamento = new Agendamento(pet.getTutor(), servico, pet, dataHora);
        Agendamento savedAgendamento = agendamentoRepository.save(agendamento);

        return new AgendamentoResponse(
                savedAgendamento.getId(),
                savedAgendamento.getTutor().getNome(),
                savedAgendamento.getPet().getNome(),
                savedAgendamento.getServico().getNome(),
                savedAgendamento.getDataHora().toString(),
                savedAgendamento.getStatus().name()
        );
    }

    public List<AgendamentoResponse> getAllAgendamentosByTutorId(Long tutorId, StatusAgendamento status) {
        List<Agendamento> agendamentos = status == null
            ? agendamentoRepository.findAllByTutor_Id(tutorId)
            : agendamentoRepository.findAllByTutor_IdAndStatus(tutorId, status);

        return agendamentos.stream()
            .map(agendamento -> new AgendamentoResponse(
                agendamento.getId(),
                agendamento.getTutor().getNome(),
                agendamento.getPet().getNome(),
                agendamento.getServico().getNome(),
                agendamento.getDataHora().toString(),
                agendamento.getStatus().name()
            ))
            .toList();
    }

    public AgendamentoResponse getAgendamentoById(Long id, Long tutorId) {
        Agendamento agendamento = agendamentoRepository.findById(id)
                .filter(a -> a.getTutor().getId().equals(tutorId))
                .orElseThrow(() -> new AgendamentoNaoEncontradoException());

        return new AgendamentoResponse(
                agendamento.getId(),
                agendamento.getTutor().getNome(),
                agendamento.getPet().getNome(),
                agendamento.getServico().getNome(),
                agendamento.getDataHora().toString(),
                agendamento.getStatus().name()
        );
    }

    public AgendamentoResponse cancelarAgendamento(Long id, Long tutorId) {
        Agendamento agendamento = agendamentoRepository.findById(id)
                .filter(a -> a.getTutor().getId().equals(tutorId))
                .orElseThrow(() -> new AgendamentoNaoEncontradoException());
        
        if (agendamento.getStatus() == StatusAgendamento.CONCLUIDO) {
            throw new CancelamentoNaoPermitidoException();
        }

        if (agendamento.getDataHora().isBefore(LocalDateTime.now(clock).plusHours(2))) {
            throw new CancelamentoNaoPermitidoException();
        }

        agendamento.setStatus(StatusAgendamento.CANCELADO);
        Agendamento updatedAgendamento = agendamentoRepository.save(agendamento);

        return new AgendamentoResponse(
                updatedAgendamento.getId(),
                updatedAgendamento.getTutor().getNome(),
                updatedAgendamento.getPet().getNome(),
                updatedAgendamento.getServico().getNome(),
                updatedAgendamento.getDataHora().toString(),
                updatedAgendamento.getStatus().name()
        );
    }
}