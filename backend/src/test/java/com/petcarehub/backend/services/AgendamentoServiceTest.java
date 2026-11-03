package com.petcarehub.backend.services;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.time.Clock;
import java.time.DayOfWeek;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneId;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;

import com.petcarehub.backend.dtos.agendamentos.CreateAgendamentoRequest;
import com.petcarehub.backend.entities.Agendamento;
import com.petcarehub.backend.entities.Pet;
import com.petcarehub.backend.entities.Servico;
import com.petcarehub.backend.entities.StatusAgendamento;
import com.petcarehub.backend.entities.Tutor;
import com.petcarehub.backend.exceptions.AgendamentoConflitanteException;
import com.petcarehub.backend.exceptions.AgendamentoNaoEncontradoException;
import com.petcarehub.backend.exceptions.CancelamentoNaoPermitidoException;
import com.petcarehub.backend.exceptions.HorarioAgendamentoInvalidoException;
import com.petcarehub.backend.exceptions.PetNaoEncontradoException;
import com.petcarehub.backend.exceptions.ServicoNaoEncontradoException;
import com.petcarehub.backend.repositories.AgendamentoRepository;
import com.petcarehub.backend.repositories.PetRepository;
import com.petcarehub.backend.repositories.ServicoRepository;

class AgendamentoServiceTest {

    private AgendamentoRepository agendamentoRepository;
    private PetRepository petRepository;
    private ServicoRepository servicoRepository;
    private AgendamentoService agendamentoService;
    private Pet pet;
    private Servico servico;
    private Tutor tutor;
    private Clock clock;

    @BeforeEach
    void setUp() {
        agendamentoRepository = mock(AgendamentoRepository.class);
        petRepository = mock(PetRepository.class);
        servicoRepository = mock(ServicoRepository.class);
        clock = Clock.fixed(Instant.parse("2026-11-03T19:33:00Z"), ZoneId.of("America/Sao_Paulo"));
        agendamentoService = new AgendamentoService(
                agendamentoRepository, petRepository, servicoRepository, clock);

        tutor = mock(Tutor.class);
        when(tutor.getId()).thenReturn(10L);
        when(tutor.getNome()).thenReturn("Ana");
        pet = mock(Pet.class);
        when(pet.getNome()).thenReturn("Rex");
        when(pet.getTutor()).thenReturn(tutor);
        servico = mock(Servico.class);
        when(servico.getId()).thenReturn(20L);
        when(servico.getNome()).thenReturn("Banho");
        when(petRepository.findByIdAndTutor_Id(30L, 10L)).thenReturn(Optional.of(pet));
        when(servicoRepository.findById(20L)).thenReturn(Optional.of(servico));
        when(agendamentoRepository.save(any(Agendamento.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));
    }

    @Test
    void criaAgendamentoComPetServicoDataHoraFutura() {
        LocalDateTime dataHora = proximaOcorrencia(DayOfWeek.MONDAY).atTime(10, 30);
        when(agendamentoRepository.existsByServico_IdAndDataHoraAndStatus(
                20L, dataHora, StatusAgendamento.AGENDADO)).thenReturn(false);

        var response = agendamentoService.createAgendamento(request(dataHora), 10L);

        assertEquals("Rex", response.petNome());
        assertEquals("Banho", response.servicoNome());
        assertEquals(dataHora.toString(), response.dataHora());
        ArgumentCaptor<Agendamento> captor = ArgumentCaptor.forClass(Agendamento.class);
        verify(agendamentoRepository).save(captor.capture());
        assertSame(pet, captor.getValue().getPet());
        assertSame(servico, captor.getValue().getServico());
        assertSame(tutor, captor.getValue().getTutor());
        assertEquals(dataHora, captor.getValue().getDataHora());
    }

    @Test
    void rejeitaAgendamentoSemPetExistente() {
        when(petRepository.findByIdAndTutor_Id(30L, 10L)).thenReturn(Optional.empty());

        assertThrows(PetNaoEncontradoException.class,
                () -> agendamentoService.createAgendamento(request(futuraDataHora()), 10L));

        verify(agendamentoRepository, never()).save(any(Agendamento.class));
    }

    @Test
    void rejeitaAgendamentoSemIdDoPet() {
        assertThrows(PetNaoEncontradoException.class,
                () -> agendamentoService.createAgendamento(
                        new CreateAgendamentoRequest(20L, null, futuraDataHora().toString()), 10L));

        verify(agendamentoRepository, never()).save(any(Agendamento.class));
    }

    @Test
    void rejeitaAgendamentoSemServicoExistente() {
        when(servicoRepository.findById(20L)).thenReturn(Optional.empty());

        assertThrows(ServicoNaoEncontradoException.class,
                () -> agendamentoService.createAgendamento(request(futuraDataHora()), 10L));

        verify(agendamentoRepository, never()).save(any(Agendamento.class));
    }

    @Test
    void rejeitaAgendamentoSemIdDoServico() {
        assertThrows(ServicoNaoEncontradoException.class,
                () -> agendamentoService.createAgendamento(
                        new CreateAgendamentoRequest(null, 30L, futuraDataHora().toString()), 10L));

        verify(agendamentoRepository, never()).save(any(Agendamento.class));
    }

    @Test
    void rejeitaDataHoraAusenteOuMalFormatada() {
        assertThrows(HorarioAgendamentoInvalidoException.class,
                () -> agendamentoService.createAgendamento(new CreateAgendamentoRequest(20L, 30L, null), 10L));
        assertThrows(HorarioAgendamentoInvalidoException.class,
                () -> agendamentoService.createAgendamento(new CreateAgendamentoRequest(20L, 30L, " "), 10L));
        assertThrows(HorarioAgendamentoInvalidoException.class,
                () -> agendamentoService.createAgendamento(new CreateAgendamentoRequest(20L, 30L, "data inválida"), 10L));

        verify(agendamentoRepository, never()).save(any(Agendamento.class));
    }

    @Test
    void rejeitaAgendamentoNoPassado() {
        assertThrows(HorarioAgendamentoInvalidoException.class,
                () -> agendamentoService.createAgendamento(
                        request(LocalDateTime.now(clock).minusMinutes(30)), 10L));

        verify(agendamentoRepository, never()).save(any(Agendamento.class));
    }

    @Test
    void aceitaSegundaAteSabadoEntreOitoEDezesseteETrinta() {
        for (DayOfWeek dia : new DayOfWeek[] {
                DayOfWeek.MONDAY, DayOfWeek.TUESDAY, DayOfWeek.WEDNESDAY,
                DayOfWeek.THURSDAY, DayOfWeek.FRIDAY, DayOfWeek.SATURDAY
        }) {
            for (LocalTime horario : new LocalTime[] {
                    LocalTime.of(8, 0), LocalTime.of(10, 30), LocalTime.of(17, 30)
            }) {
                LocalDateTime dataHora = proximaOcorrencia(dia).atTime(horario);
                when(agendamentoRepository.existsByServico_IdAndDataHoraAndStatus(
                        20L, dataHora, StatusAgendamento.AGENDADO)).thenReturn(false);

                agendamentoService.createAgendamento(request(dataHora), 10L);
            }
        }

        verify(agendamentoRepository, times(18)).save(any(Agendamento.class));
    }

    @Test
    void rejeitaDomingoHorariosForaDoExpedienteEIntervalosInvalidos() {
        assertAgendamentoInvalido(proximaOcorrencia(DayOfWeek.SUNDAY).atTime(10, 0));
        assertAgendamentoInvalido(proximaOcorrencia(DayOfWeek.MONDAY).atTime(7, 30));
        assertAgendamentoInvalido(proximaOcorrencia(DayOfWeek.MONDAY).atTime(18, 0));
        assertAgendamentoInvalido(proximaOcorrencia(DayOfWeek.MONDAY).atTime(10, 15));
        assertAgendamentoInvalido(proximaOcorrencia(DayOfWeek.MONDAY).atTime(10, 0, 1));
    }

    @Test
    void rejeitaHorarioJaOcupadoPeloMesmoServico() {
        LocalDateTime dataHora = futuraDataHora();
        when(agendamentoRepository.existsByServico_IdAndDataHoraAndStatus(
                20L, dataHora, StatusAgendamento.AGENDADO)).thenReturn(true);

        assertThrows(AgendamentoConflitanteException.class,
                () -> agendamentoService.createAgendamento(request(dataHora), 10L));

        verify(agendamentoRepository, never()).save(any(Agendamento.class));
    }

    @Test
    void permiteCancelarAgendamentoComMaisDeDuasHorasDeAntecedencia() {
        Agendamento agendamento = agendamento(LocalDateTime.now(clock).plusHours(3));
        when(agendamentoRepository.findById(1L)).thenReturn(Optional.of(agendamento));
        when(agendamentoRepository.save(any(Agendamento.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        var response = agendamentoService.cancelarAgendamento(1L, 10L);

        assertEquals(StatusAgendamento.CANCELADO.name(), response.status());
        assertEquals(StatusAgendamento.CANCELADO, agendamento.getStatus());
    }

    @Test
    void permiteCancelarExatamenteDuasHorasAntes() {
        Agendamento agendamento = agendamento(LocalDateTime.now(clock).plusHours(2));
        when(agendamentoRepository.findById(1L)).thenReturn(Optional.of(agendamento));
        when(agendamentoRepository.save(any(Agendamento.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        var response = agendamentoService.cancelarAgendamento(1L, 10L);

        assertEquals(StatusAgendamento.CANCELADO.name(), response.status());
    }

    @Test
    void rejeitaCancelamentoComMenosDeDuasHorasDeAntecedencia() {
        Agendamento agendamento = agendamento(LocalDateTime.now(clock).plusHours(1));
        when(agendamentoRepository.findById(1L)).thenReturn(Optional.of(agendamento));

        assertThrows(CancelamentoNaoPermitidoException.class,
                () -> agendamentoService.cancelarAgendamento(1L, 10L));

        verify(agendamentoRepository, never()).save(any(Agendamento.class));
    }

    @Test
    void rejeitaCancelamentoDeAgendamentoConcluido() {
        Agendamento agendamento = agendamento(LocalDateTime.now(clock).plusHours(3));
        agendamento.setStatus(StatusAgendamento.CONCLUIDO);
        when(agendamentoRepository.findById(1L)).thenReturn(Optional.of(agendamento));

        assertThrows(CancelamentoNaoPermitidoException.class,
                () -> agendamentoService.cancelarAgendamento(1L, 10L));

        verify(agendamentoRepository, never()).save(any(Agendamento.class));
    }

    @Test
    void rejeitaCancelamentoDeAgendamentoInexistente() {
        when(agendamentoRepository.findById(1L)).thenReturn(Optional.empty());

        assertThrows(AgendamentoNaoEncontradoException.class,
                () -> agendamentoService.cancelarAgendamento(1L, 10L));
    }

    private void assertAgendamentoInvalido(LocalDateTime dataHora) {
        assertThrows(HorarioAgendamentoInvalidoException.class,
                () -> agendamentoService.createAgendamento(request(dataHora), 10L));
        verify(agendamentoRepository, never()).save(any(Agendamento.class));
    }

    private CreateAgendamentoRequest request(LocalDateTime dataHora) {
        return new CreateAgendamentoRequest(20L, 30L, dataHora.toString());
    }

    private LocalDateTime futuraDataHora() {
        return proximaOcorrencia(DayOfWeek.MONDAY).atTime(10, 0);
    }

    private LocalDate proximaOcorrencia(DayOfWeek dia) {
        LocalDate data = LocalDate.now(clock).plusDays(1);
        while (data.getDayOfWeek() != dia) {
            data = data.plusDays(1);
        }
        return data;
    }

    private Agendamento agendamento(LocalDateTime dataHora) {
        return new Agendamento(tutor, servico, pet, dataHora);
    }
}
