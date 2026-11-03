package com.petcarehub.backend.services;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.time.LocalDateTime;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.petcarehub.backend.entities.Pet;
import com.petcarehub.backend.entities.StatusAgendamento;
import com.petcarehub.backend.exceptions.ExclusaoDePetComAgendamentoException;
import com.petcarehub.backend.repositories.AgendamentoRepository;
import com.petcarehub.backend.repositories.PetRepository;
import com.petcarehub.backend.repositories.TutorRepository;

class PetServiceTest {

    private PetRepository petRepository;
    private AgendamentoRepository agendamentoRepository;
    private PetService petService;

    @BeforeEach
    void setUp() {
        petRepository = mock(PetRepository.class);
        TutorRepository tutorRepository = mock(TutorRepository.class);
        agendamentoRepository = mock(AgendamentoRepository.class);
        petService = new PetService(petRepository, tutorRepository, agendamentoRepository);
        when(petRepository.findByIdAndTutor_Id(1L, 2L)).thenReturn(Optional.of(mock(Pet.class)));
        when(agendamentoRepository.existsByPet_IdAndDataHoraAfterAndStatus(
                eq(1L), any(LocalDateTime.class), eq(StatusAgendamento.AGENDADO))).thenReturn(false);
    }

    @Test
    void naoDeletaPetComAgendamentoFuturoAgendado() {
        when(agendamentoRepository.existsByPet_IdAndDataHoraAfterAndStatus(
                eq(1L), any(LocalDateTime.class), eq(StatusAgendamento.AGENDADO))).thenReturn(true);

        assertThrows(ExclusaoDePetComAgendamentoException.class,
                () -> petService.deletePet(1L, 2L));

        verify(petRepository, never()).deleteById(1L);
    }

    @Test
    void deletaPetSemAgendamentoFuturoAgendado() {
        petService.deletePet(1L, 2L);

        verify(agendamentoRepository).existsByPet_IdAndDataHoraAfterAndStatus(
                eq(1L), any(LocalDateTime.class), eq(StatusAgendamento.AGENDADO));
        verify(petRepository).deleteById(1L);
    }
}
