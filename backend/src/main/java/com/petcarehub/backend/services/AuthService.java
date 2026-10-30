package com.petcarehub.backend.services;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.petcarehub.backend.dtos.auth.*;
import com.petcarehub.backend.entities.Tutor;
import com.petcarehub.backend.exceptions.EmailJaCadastradoException;
import com.petcarehub.backend.exceptions.CredenciaisInvalidasException;
import com.petcarehub.backend.repositories.TutorRepository;
import com.petcarehub.backend.services.JwtService.JwtToken;

@Service
public class AuthService {
    private final TutorRepository tutorRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    public AuthService(
            TutorRepository tutorRepository,
            PasswordEncoder passwordEncoder,
            JwtService jwtService) {
        this.tutorRepository = tutorRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
    }

    public TutorResponse registrarTutor(RegistroRequest request) {
        if (tutorRepository.existsByEmail(request.email())) {
            throw new EmailJaCadastradoException();
        }

        String senhaHash = passwordEncoder.encode(request.senha());

        Tutor tutor = new Tutor(
                request.nome(),
                request.email(),
                request.telefone(),
                senhaHash
        );

        Tutor tutorSalvo = tutorRepository.save(tutor);

        return new TutorResponse(
                tutorSalvo.getId(),
                tutorSalvo.getNome(),
                tutorSalvo.getEmail(),
                tutorSalvo.getTelefone()
        );
    }

    public LoginResponse autenticarTutor(LoginRequest request) {
        Tutor tutor = tutorRepository.findByEmail(request.email())
                .orElseThrow(CredenciaisInvalidasException::new);

        if (!passwordEncoder.matches(request.senha(), tutor.getSenhaHash())) {
            throw new CredenciaisInvalidasException();
        }

        JwtToken jwt = jwtService.gerarToken(tutor);

        return new LoginResponse(
                jwt.valor(),
                "Bearer",
                jwt.expiraEm()
        );
    }
}