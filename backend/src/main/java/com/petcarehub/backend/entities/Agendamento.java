package com.petcarehub.backend.entities;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

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
    @Column(nullable = false)
    private String dataHora;

    public Agendamento(Tutor tutor, Servico servico, Pet pet, String dataHora) {
        this.tutor = tutor;
        this.servico = servico;
        this.pet = pet;
        this.dataHora = dataHora;
    }
}