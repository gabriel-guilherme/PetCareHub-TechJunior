package com.petcarehub.backend.exceptions;

public class ExclusaoDePetComAgendamentoException extends RuntimeException {
    public ExclusaoDePetComAgendamentoException() {
        super("Não é possível excluir o pet, pois ele possui agendamentos associados.");
    }
}