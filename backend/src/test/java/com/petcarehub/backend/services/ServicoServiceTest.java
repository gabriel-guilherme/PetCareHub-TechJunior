package com.petcarehub.backend.services;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.petcarehub.backend.entities.Agendamento;
import com.petcarehub.backend.entities.Servico;
import com.petcarehub.backend.entities.StatusAgendamento;
import com.petcarehub.backend.exceptions.ServicoNaoEncontradoException;
import com.petcarehub.backend.repositories.AgendamentoRepository;
import com.petcarehub.backend.repositories.ServicoRepository;

class ServicoServiceTest {

    private ServicoRepository servicoRepository;
    private AgendamentoRepository agendamentoRepository;
    private ServicoService servicoService;

    @BeforeEach
    void setUp() {
        servicoRepository = mock(ServicoRepository.class);
        agendamentoRepository = mock(AgendamentoRepository.class);
        servicoService = new ServicoService(servicoRepository, agendamentoRepository);
    }

    @Test
    void retornaSlotsDeMeiaHoraEExcluiOsJaAgendados() {
        LocalDate data = proximoDiaDeAtendimento();
        Agendamento agendamento = mock(Agendamento.class);
        when(servicoRepository.findById(1L)).thenReturn(Optional.of(mock(Servico.class)));
        when(agendamentoRepository
                .findAllByServico_IdAndDataHoraGreaterThanEqualAndDataHoraLessThanAndStatus(
                        eq(1L), any(LocalDateTime.class), any(LocalDateTime.class),
                        eq(StatusAgendamento.AGENDADO)))
                .thenReturn(List.of(agendamento));
        when(agendamento.getDataHora()).thenReturn(data.atTime(9, 30));

        List<String> horarios = servicoService.getHorariosLivres(1L, data);

        assertEquals(19, horarios.size());
        assertEquals("08:00", horarios.get(0));
        assertEquals("17:30", horarios.get(horarios.size() - 1));
        assertFalse(horarios.contains("09:30"));
    }

    @Test
    void naoRetornaHorariosParaDataPassadaOuDomingo() {
        when(servicoRepository.findById(1L)).thenReturn(Optional.of(mock(Servico.class)));
        LocalDate domingo = LocalDate.now().with(DayOfWeek.SUNDAY).plusWeeks(1);

        assertEquals(List.of(), servicoService.getHorariosLivres(1L, LocalDate.of(2000, 1, 1)));
        assertEquals(List.of(), servicoService.getHorariosLivres(1L, domingo));
        verifyNoInteractions(agendamentoRepository);
    }

    @Test
    void falhaComServicoInexistente() {
        when(servicoRepository.findById(1L)).thenReturn(Optional.empty());

        assertThrows(ServicoNaoEncontradoException.class,
                () -> servicoService.getHorariosLivres(1L, proximoDiaDeAtendimento()));
    }

    private LocalDate proximoDiaDeAtendimento() {
        LocalDate data = LocalDate.now().plusDays(1);
        while (data.getDayOfWeek() == DayOfWeek.SUNDAY) {
            data = data.plusDays(1);
        }
        return data;
    }
}
