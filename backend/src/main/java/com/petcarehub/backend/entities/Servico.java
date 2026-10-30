package com.petcarehub.backend.entities;

// import
import java.util.ArrayList;
import java.util.List;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "servicos")
@Getter
@NoArgsConstructor(access = lombok.AccessLevel.PROTECTED)

public class Servico {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Setter
    @NotBlank
    @Column(nullable = false, length = 120)
    private String nome;

    @Setter
    @Column(length = 500)
    private String descricao;

    @Setter
    @NotNull
    @Column(nullable = false)
    private Double preco;

    @OneToMany(mappedBy = "servico")
    private List<Agendamento> agendamentos = new ArrayList<>();

    public Servico(String nome, String descricao, Double preco) {
        this.nome = nome;
        this.descricao = descricao;
        this.preco = preco;
    }
}