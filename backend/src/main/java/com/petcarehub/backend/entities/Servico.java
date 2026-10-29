package com.petcarehub.backend.entities;

// import
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "servicos")
@Getter
@NoArgsConstructor(access = lombok.AccessLevel.PROTECTED)

public class Servico {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Setter
    @Column(nullable = false, length = 120)
    private String nome;

    @Setter
    @Column(length = 500)
    private String descricao;

    @Setter
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