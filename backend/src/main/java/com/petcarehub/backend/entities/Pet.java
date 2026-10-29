package com.petcarehub.backend.entities;

import java.time.LocalDate;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "pets")
@Getter
@NoArgsConstructor(access = lombok.AccessLevel.PROTECTED)

public class Pet {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long Id;

    @Setter
    @Column(nullable = false, length = 120)
    private String nome;

    @Setter
    @Column(nullable = false, length = 120)
    private String especie;

    @Setter
    @Column(length = 120)
    private String raca;

    @Setter
    @Column(name = "data_nascimento")
    private LocalDate dataNascimento;

    @Setter
    @ManyToOne(optional = false)
    @JoinColumn(name = "tutor_id", nullable = false)
    private Tutor tutor;

    @Setter
    @OneToMany(mappedBy = "pet")
    private List<Agendamento> agendamentos = new ArrayList<>();

    public Pet(String nome, String especie, String raca, LocalDate dataNascimento, Tutor tutor) {
        this.nome = nome;
        this.especie = especie;
        this.raca = raca;
        this.dataNascimento = dataNascimento;
        this.tutor = tutor;
    }

    public int getAnosDeIdade() {
        if (dataNascimento == null) {
            return 0;
        }
        LocalDate hoje = LocalDate.now();
        return hoje.getYear() - dataNascimento.getYear();
    }
}