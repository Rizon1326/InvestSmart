package com.businessanalysis.marketanalysis.controller;

import com.businessanalysis.marketanalysis.model.UserInput;
import com.businessanalysis.marketanalysis.model.AnalysisResult;
import com.businessanalysis.marketanalysis.service.MarketAnalysisService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/market-analysis")
@CrossOrigin(origins = "*")
public class MarketAnalysisController {
    
    @Autowired
    private MarketAnalysisService marketAnalysisService;
    
    @PostMapping("/analyze")
    public ResponseEntity<AnalysisResult> analyzeMarket(@Valid @RequestBody UserInput userInput) {
        try {
            AnalysisResult result = marketAnalysisService.performAnalysis(userInput);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }
    
    @GetMapping("/result/{id}")
    public ResponseEntity<AnalysisResult> getAnalysisResult(@PathVariable Long id) {
        try {
            AnalysisResult result = marketAnalysisService.getAnalysisResult(id);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    @GetMapping("/health")
    public ResponseEntity<String> healthCheck() {
        return ResponseEntity.ok("Market Analysis API is running");
    }
}