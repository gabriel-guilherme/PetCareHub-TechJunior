package com.petcarehub.backend.entities;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.PrePersist;
import jakarta.persistence.Table;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "tutores")
@Getter
@NoArgsConstructor(access = lombok.AccessLevel.PROTECTED)

public class Tutor {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Setter
    @NotBlank
    @Column(nullable = false, length = 120)
    private String nome;

    @Setter
    @Email
    @Column(nullable = false, unique = true, length = 254)
    private String email;

    @Setter
    @NotBlank
    @Column(length = 20)
    private String telefone;

    @Setter
    @NotBlank
    @Column(name = "senha_hash", nullable = false)
    private String senhaHash;

    @Setter
    @NotNull
    @Column(name = "criado_em", nullable = false, updatable = false)
    private Instant criadoEm;

    @OneToMany(mappedBy = "tutor")
    private List<Pet> pets = new ArrayList<>();

    public Tutor(String nome, String email, String telefone, String senhaHash) {
        this.nome = nome;
        this.email = email;
        this.telefone = telefone;
        this.senhaHash = senhaHash;
    }

    @PrePersist
    protected void aoCriar() {
        if (criadoEm == null) {
            criadoEm = Instant.now();
        }
    }
}