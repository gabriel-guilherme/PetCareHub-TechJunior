package com.petcarehub.backend.repositories;

import java.util.Optional;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.petcarehub.backend.entities.Pet;

public interface PetRepository extends JpaRepository<Pet, Long> {
    List<Pet> findAllByTutor_Id(Long tutorId);
    Optional<Pet> findByIdAndTutor_Id(Long id, Long tutorId);
}