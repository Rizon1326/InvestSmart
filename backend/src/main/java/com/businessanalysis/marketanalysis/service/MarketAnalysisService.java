package com.businessanalysis.marketanalysis.service;

import com.businessanalysis.marketanalysis.model.UserInput;
import com.businessanalysis.marketanalysis.model.AnalysisResult;
import com.businessanalysis.marketanalysis.repository.UserInputRepository;
import com.businessanalysis.marketanalysis.repository.AnalysisResultRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class MarketAnalysisService {
    
    @Autowired
    private UserInputRepository userInputRepository;
    
    @Autowired
    private AnalysisResultRepository analysisResultRepository;
    
    @Autowired
    private ScrapingService scrapingService;
    
    @Autowired
    private GroqApiService groqApiService;
    
    @Autowired
    private BusinessAnalysisService businessAnalysisService;
    
    public AnalysisResult performAnalysis(UserInput userInput) {
        // Save user input
        UserInput savedInput = userInputRepository.save(userInput);
        
        // Step 1: Trigger scraping service
        String scrapedData = scrapingService.scrapeMarketData(userInput);
        
        // Step 2: Get AI analysis from Groq
        String aiAnalysis = groqApiService.analyzeWithGroq(scrapedData, userInput);
        
        // Step 3: Perform business analysis calculations
        AnalysisResult result = businessAnalysisService.calculateBusinessMetrics(
            savedInput, scrapedData, aiAnalysis);
        
        // Save and return results
        return analysisResultRepository.save(result);
    }
    
    public AnalysisResult getAnalysisResult(Long userInputId) {
        return analysisResultRepository.findByUserInputId(userInputId)
            .orElseThrow(() -> new RuntimeException("Analysis result not found"));
    }
}