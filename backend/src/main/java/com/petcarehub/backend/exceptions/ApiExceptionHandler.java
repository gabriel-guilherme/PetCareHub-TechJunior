package com.petcarehub.backend.exceptions;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ApiExceptionHandler {

    @ExceptionHandler(EmailJaCadastradoException.class)
    public ResponseEntity<Void> tratarEmailJaCadastrado(
            EmailJaCadastradoException exception) {
        return ResponseEntity.status(HttpStatus.CONFLICT).build();
    }

    @ExceptionHandler(CredenciaisInvalidasException.class)
    public ResponseEntity<Void> tratarCredenciaisInvalidas(
            CredenciaisInvalidasException exception) {
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
    }

    @ExceptionHandler(TutorNaoEncontradoException.class)
    public ResponseEntity<Void> tratarTutorNaoEncontrado(
            TutorNaoEncontradoException exception) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @ExceptionHandler(PetNaoEncontradoException.class)
    public ResponseEntity<Void> tratarPetNaoEncontrado(
            PetNaoEncontradoException exception) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @ExceptionHandler(ServicoNaoEncontradoException.class)
    public ResponseEntity<Void> tratarServicoNaoEncontrado(
            ServicoNaoEncontradoException exception) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @ExceptionHandler(AgendamentoNaoEncontradoException.class)
    public ResponseEntity<Void> tratarAgendamentoNaoEncontrado(
            AgendamentoNaoEncontradoException exception) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @ExceptionHandler(CancelamentoNaoPermitidoException.class)
    public ResponseEntity<Void> tratarCancelamentoNaoPermitido(
            CancelamentoNaoPermitidoException exception) {
        return ResponseEntity.status(HttpStatus.CONFLICT).build();
    }

    @ExceptionHandler(HorarioAgendamentoInvalidoException.class)
    public ResponseEntity<Void> tratarHorarioAgendamentoInvalido(
            HorarioAgendamentoInvalidoException exception) {
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
    }

    @ExceptionHandler(AgendamentoConflitanteException.class)
    public ResponseEntity<Void> tratarAgendamentoConflitante(
            AgendamentoConflitanteException exception) {
        return ResponseEntity.status(HttpStatus.CONFLICT).build();
    }
}