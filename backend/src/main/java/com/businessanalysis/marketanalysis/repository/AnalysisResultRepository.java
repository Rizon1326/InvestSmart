package com.businessanalysis.marketanalysis.repository;

import com.businessanalysis.marketanalysis.model.AnalysisResult;
import com.businessanalysis.marketanalysis.model.UserInput;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface AnalysisResultRepository extends JpaRepository<AnalysisResult, Long> {
    
    Optional<AnalysisResult> findByUserInput(UserInput userInput);
    
    Optional<AnalysisResult> findByUserInputId(Long userInputId);
}