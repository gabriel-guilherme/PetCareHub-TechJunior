package com.petcarehub.backend.services;

import org.springframework.stereotype.Service;

import java.util.List;

import com.petcarehub.backend.repositories.PetRepository;
import com.petcarehub.backend.repositories.TutorRepository;
import com.petcarehub.backend.entities.Pet;
import com.petcarehub.backend.entities.Tutor;
import com.petcarehub.backend.dtos.pets.CreatePetRequest;
import com.petcarehub.backend.dtos.pets.UpdatePetRequest;
import com.petcarehub.backend.dtos.pets.PetResponse;
import java.time.LocalDate;
import com.petcarehub.backend.exceptions.TutorNaoEncontradoException;
import com.petcarehub.backend.exceptions.PetNaoEncontradoException;

@Service
public class PetService {
    private final PetRepository petRepository;
    private final TutorRepository tutorRepository;

    public PetService(PetRepository petRepository, TutorRepository tutorRepository) {
        this.petRepository = petRepository;
        this.tutorRepository = tutorRepository;
    }

    public List<PetResponse> getAllPetsByTutorId(Long tutorId) {
        return petRepository.findAllByTutor_Id(tutorId).stream()
                .map(pet -> new PetResponse(pet.getId(), pet.getNome(), pet.getEspecie(), pet.getRaca(), pet.getDataNascimento().toString(), pet.getAnosDeIdade()))
                .toList();
    }

    public PetResponse createPet(CreatePetRequest request, Long tutorId) {
        Tutor tutor = tutorRepository.findById(tutorId)
                .orElseThrow(() -> new TutorNaoEncontradoException());

        LocalDate dataNascimento = LocalDate.parse(request.dataNascimento());
        String raca = request.raca() == null || request.raca().isBlank()
                ? "SRD (Sem raça definida)"
                : request.raca().trim();

        Pet pet = new Pet(
                request.nome(),
                request.especie(),
                raca,
                dataNascimento,
                tutor
        );

        Pet savedPet = petRepository.save(pet);
        return new PetResponse(savedPet.getId(), savedPet.getNome(), savedPet.getEspecie(), savedPet.getRaca(), savedPet.getDataNascimento().toString(), savedPet.getAnosDeIdade());
    }

    public PetResponse updatePet(UpdatePetRequest pet, Long id, Long tutorId) {
        Pet existingPet = petRepository.findByIdAndTutor_Id(id, tutorId)
                .orElseThrow(() -> new PetNaoEncontradoException());

        existingPet.setNome(pet.nome());
        existingPet.setEspecie(pet.especie());
        existingPet.setRaca(pet.raca());
        existingPet.setDataNascimento(LocalDate.parse(pet.dataNascimento()));

        Pet updatedPet = petRepository.save(existingPet);
        return new PetResponse(updatedPet.getId(), updatedPet.getNome(), updatedPet.getEspecie(), updatedPet.getRaca(), updatedPet.getDataNascimento().toString(), updatedPet.getAnosDeIdade());

    }

    public void deletePet(Long petId) {
        petRepository.deleteById(petId);
    }
}