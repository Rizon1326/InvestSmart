package com.businessanalysis.marketanalysis.service;

import com.businessanalysis.marketanalysis.model.UserInput;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;

@Service
public class GroqApiService {
    
    private final WebClient webClient;
    
    @Value("${groq.api.key:}")
    private String groqApiKey;
    
    @Value("${groq.api.url:https://api.groq.com/openai/v1/chat/completions}")
    private String groqApiUrl;
    
    public GroqApiService() {
        this.webClient = WebClient.builder().build();
    }
    
    public String analyzeWithGroq(String scrapedData, UserInput userInput) {
        if (groqApiKey.isEmpty()) {
            return createMockAnalysis(userInput);
        }
        
        try {
            GroqRequest request = createGroqRequest(scrapedData, userInput);
            
            String response = webClient.post()
                .uri(groqApiUrl)
                .header(HttpHeaders.AUTHORIZATION, "Bearer " + groqApiKey)
                .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .bodyValue(request)
                .retrieve()
                .bodyToMono(String.class)
                .block();
            
            return response != null ? response : createMockAnalysis(userInput);
        } catch (Exception e) {
            return createMockAnalysis(userInput);
        }
    }
    
    private GroqRequest createGroqRequest(String scrapedData, UserInput userInput) {
        String prompt = String.format(
            """
            Analyze the following market data for a business opportunity in %s:
            
            User Requirements:
            - Location: %s
            - Business Interest: %s
            - Capital Range: %.2f - %.2f BDT
            - Risk Profile: %s
            - Target Income: %.2f BDT (%s)
            - Work Type: %s
            - Selling Channel: %s
            
            Market Data:
            %s
            
            Please provide:
            1. Demand analysis and market opportunity assessment
            2. Pricing strategy recommendations
            3. Competition analysis
            4. Risk assessment
            5. Revenue potential evaluation
            6. Specific business recommendations
            
            Format your response as detailed business insights.
            """,
            userInput.getLocation(),
            userInput.getLocation(),
            userInput.getBusinessInterest(),
            userInput.getCapitalMin(),
            userInput.getCapitalMax(),
            userInput.getRiskProfile(),
            userInput.getTargetIncome(),
            userInput.getIncomePeriod(),
            userInput.getWorkType(),
            userInput.getSellingChannel(),
            scrapedData
        );
        
        return new GroqRequest("llama-3.1-8b-instant", prompt);
    }
    
    private String createMockAnalysis(UserInput userInput) {
        return String.format(
            """
            {
                "analysis": "Based on the market data for %s in %s, there are strong opportunities in the %s sector. The capital range of %.0f-%.0f BDT is suitable for starting a %s business.",
                "demand_score": 7.5,
                "market_opportunity": "High potential market with growing demand",
                "pricing_strategy": "Competitive pricing with 25-30%% margin recommended",
                "risk_level": "%s",
                "revenue_potential": "Monthly revenue potential of %.0f-%.0f BDT",
                "recommendations": [
                    "Focus on popular products with high demand scores",
                    "Leverage %s channel for maximum reach",
                    "Consider seasonal variations in demand",
                    "Maintain quality standards to build customer loyalty"
                ]
            }
            """,
            userInput.getBusinessInterest(),
            userInput.getLocation(),
            userInput.getBusinessInterest(),
            userInput.getCapitalMin(),
            userInput.getCapitalMax(),
            userInput.getBusinessInterest(),
            userInput.getRiskProfile().toLowerCase(),
            userInput.getTargetIncome() * 0.8,
            userInput.getTargetIncome() * 1.2,
            userInput.getSellingChannel()
        );
    }
    
    // Inner classes for request/response structure
    public static class GroqRequest {
        public String model;
        public GroqMessage[] messages;
        
        public GroqRequest(String model, String content) {
            this.model = model;
            this.messages = new GroqMessage[] {
                new GroqMessage("system", "You are an expert business analyst specializing in market analysis and business recommendations for Bangladesh market."),
                new GroqMessage("user", content)
            };
        }
    }
    
    public static class GroqMessage {
        public String role;
        public String content;
        
        public GroqMessage(String role, String content) {
            this.role = role;
            this.content = content;
        }
    }
}