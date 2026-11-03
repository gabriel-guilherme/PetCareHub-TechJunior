package com.petcarehub.backend.controllers;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import com.petcarehub.backend.services.PetService;
import com.petcarehub.backend.dtos.pets.CreatePetRequest;
import com.petcarehub.backend.dtos.pets.UpdatePetRequest;
import com.petcarehub.backend.dtos.pets.PetResponse;
import org.springframework.security.oauth2.jwt.Jwt;

import jakarta.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/api/pets")
public class PetsController {
    private final PetService petService;

    public PetsController(PetService petService) {
        this.petService = petService;
    }

    @PostMapping("/")
    public ResponseEntity<PetResponse> createPet(@Valid @RequestBody CreatePetRequest request, @AuthenticationPrincipal Jwt jwt) {
        Long tutorId = Long.valueOf(jwt.getSubject());
        PetResponse createdPet = petService.createPet(request, tutorId);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdPet);
    }

    @GetMapping("/")
    public ResponseEntity<List<PetResponse>> getAllTutorsPets(@AuthenticationPrincipal Jwt jwt) {
        Long tutorId = Long.valueOf(jwt.getSubject());
        List<PetResponse> pets = petService.getAllPetsByTutorId(tutorId);
        return ResponseEntity.ok(pets);
    }

    @PutMapping("/{id}")
    public ResponseEntity<PetResponse> updatePet(@Valid @RequestBody UpdatePetRequest request, @PathVariable Long id, @AuthenticationPrincipal Jwt jwt) {
        Long tutorId = Long.valueOf(jwt.getSubject());
        PetResponse updatedPet = petService.updatePet(request, id, tutorId); // Implement the logic to update a pet
        return ResponseEntity.ok(updatedPet);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<String> deletePet(@PathVariable Long id) {
        petService.deletePet(id); // Implement the logic to delete a pet
        return ResponseEntity.noContent().build();
    }
}