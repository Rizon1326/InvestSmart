package com.businessanalysis.marketanalysis.service;

import com.businessanalysis.marketanalysis.model.UserInput;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.beans.factory.annotation.Value;

@Service
public class ScrapingService {
    
    private final WebClient webClient;
    
    @Value("${python.scraping.service.url:http://localhost:5000}")
    private String pythonServiceUrl;
    
    public ScrapingService() {
        this.webClient = WebClient.builder().build();
    }
    
    public String scrapeMarketData(UserInput userInput) {
        try {
            // Call Python scraping service
            String response = webClient.post()
                .uri(pythonServiceUrl + "/scrape")
                .bodyValue(createScrapingRequest(userInput))
                .retrieve()
                .bodyToMono(String.class)
                .block();
            
            return response != null ? response : "{}";
        } catch (Exception e) {
            // Return mock data if scraping service is not available
            return createMockScrapedData(userInput);
        }
    }
    
    private Object createScrapingRequest(UserInput userInput) {
        return new ScrapingRequest(
            userInput.getLocation(),
            userInput.getBusinessInterest(),
            userInput.getSellingChannel()
        );
    }
    
    private String createMockScrapedData(UserInput userInput) {
        // Mock scraped data for development/testing
        return """
        {
            "products": [
                {
                    "name": "Popular Food Item",
                    "price": 250.0,
                    "demand_score": 8.5,
                    "competition_level": "medium",
                    "seasonal_trend": "stable"
                },
                {
                    "name": "Trending Product",
                    "price": 180.0,
                    "demand_score": 7.2,
                    "competition_level": "high",
                    "seasonal_trend": "growing"
                }
            ],
            "location": "%s",
            "business_type": "%s",
            "market_size": "large",
            "avg_price_range": [150.0, 300.0]
        }
        """.formatted(userInput.getLocation(), userInput.getBusinessInterest());
    }
    
    // Inner class for request structure
    public static class ScrapingRequest {
        public String location;
        public String businessInterest;
        public String sellingChannel;
        
        public ScrapingRequest(String location, String businessInterest, String sellingChannel) {
            this.location = location;
            this.businessInterest = businessInterest;
            this.sellingChannel = sellingChannel;
        }
    }
}