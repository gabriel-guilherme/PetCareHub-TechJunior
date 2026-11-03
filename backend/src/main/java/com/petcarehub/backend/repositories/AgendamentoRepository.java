package com.petcarehub.backend.repositories;

import java.util.List;
import java.time.LocalDateTime;

import org.springframework.data.jpa.repository.JpaRepository;

import com.petcarehub.backend.entities.Agendamento;
import com.petcarehub.backend.entities.StatusAgendamento;

public interface AgendamentoRepository extends JpaRepository<Agendamento, Long> {
    List<Agendamento> findAllByTutor_Id(Long tutorId);
    List<Agendamento> findAllByTutor_IdAndStatus(Long tutorId, StatusAgendamento status);
    List<Agendamento> findAllByServico_IdAndDataHoraGreaterThanEqualAndDataHoraLessThanAndStatus(Long servicoId, LocalDateTime inicio, LocalDateTime fim, StatusAgendamento status);
    boolean existsByServico_IdAndDataHoraAndStatus(Long servicoId, LocalDateTime dataHora, StatusAgendamento status);
    boolean existsByPet_Id(Long petId);
}