package com.petcarehub.backend.entities;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "pets")
@Getter
@NoArgsConstructor(access = lombok.AccessLevel.PROTECTED)

public class Pet {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long Id;

    @Setter
    @NotBlank
    @Column(nullable = false, length = 120)
    private String nome;

    @Setter
    @NotBlank
    @Column(nullable = false, length = 120)
    private String especie;

    @Setter
    @NotBlank
    @Column(length = 120)
    private String raca;

    @Setter
    @NotNull
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