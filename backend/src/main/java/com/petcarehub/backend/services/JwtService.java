package com.petcarehub.backend.services;

import java.time.Duration;
import java.time.Instant;

import org.springframework.security.oauth2.jose.jws.MacAlgorithm;
import org.springframework.security.oauth2.jwt.JwtClaimsSet;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.JwtEncoderParameters;
import org.springframework.security.oauth2.jwt.JwsHeader;
import org.springframework.stereotype.Service;

import com.petcarehub.backend.entities.Tutor;

@Service
public class JwtService {
    private final JwtEncoder jwtEncoder;
    private final Duration validade = Duration.ofMinutes(60);

    public JwtService(JwtEncoder jwtEncoder) {
        this.jwtEncoder = jwtEncoder;
    }

    public JwtToken gerarToken(Tutor tutor) {
        Instant agora = Instant.now();
        Instant expiraEm = agora.plus(validade);

        JwtClaimsSet claims = JwtClaimsSet.builder()
                .issuer("petcarehub")
                .issuedAt(agora)
                .expiresAt(expiraEm)
                .subject(tutor.getId().toString())
                .build();

        JwsHeader header = JwsHeader.with(MacAlgorithm.HS256).build();

        String valor = jwtEncoder
                .encode(JwtEncoderParameters.from(header, claims))
                .getTokenValue();

        return new JwtToken(valor, expiraEm);
    }

    public record JwtToken(String valor, Instant expiraEm) {}
}