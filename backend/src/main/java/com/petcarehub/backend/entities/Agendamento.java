package com.petcarehub.backend.entities;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import jakarta.validation.constraints.NotNull;

@Entity
@Table(name = "agendamentos")
@Getter
@NoArgsConstructor(access = lombok.AccessLevel.PROTECTED)

public class Agendamento {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Setter
    @ManyToOne
    @JoinColumn(name = "tutor_id", nullable = false)
    private Tutor tutor;

    @Setter
    @ManyToOne
    @JoinColumn(name = "servico_id", nullable = false)
    private Servico servico;

    @Setter
    @ManyToOne
    @JoinColumn(name = "pet_id", nullable = false)
    private Pet pet;

    @Setter
    @NotNull
    @Column(nullable = false)
    private String dataHora;

    public Agendamento(Tutor tutor, Servico servico, Pet pet, String dataHora) {
        this.tutor = tutor;
        this.servico = servico;
        this.pet = pet;
        this.dataHora = dataHora;
    }
}