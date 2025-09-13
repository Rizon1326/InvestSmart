package com.businessanalysis.marketanalysis.service;

import com.businessanalysis.marketanalysis.model.UserInput;
import com.businessanalysis.marketanalysis.model.AnalysisResult;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

import java.util.Random;

@Service
public class BusinessAnalysisService {
    
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final Random random = new Random();
    
    public AnalysisResult calculateBusinessMetrics(UserInput userInput, String scrapedData, String aiAnalysis) {
        AnalysisResult result = new AnalysisResult();
        result.setUserInput(userInput);
        result.setAiAnalysis(aiAnalysis);
        
        try {
            // Parse scraped data
            JsonNode scrapedJson = objectMapper.readTree(scrapedData);
            
            // Calculate fit score (demand_score * margin_score * feasibility_score)
            double fitScore = calculateFitScore(userInput, scrapedJson);
            result.setFitScore(fitScore);
            
            // Calculate suggested price (procurement_cost + margin - competition_adjustment)
            double suggestedPrice = calculateSuggestedPrice(userInput, scrapedJson);
            result.setSuggestedPrice(suggestedPrice);
            
            // Calculate financial metrics
            FinancialMetrics metrics = calculateFinancialMetrics(userInput, suggestedPrice, fitScore);
            result.setExpectedRevenue(metrics.expectedRevenue);
            result.setNetProfit(metrics.netProfit);
            result.setRoiPercentage(metrics.roiPercentage);
            result.setPaybackPeriodMonths(metrics.paybackPeriodMonths);
            
            // Generate demand forecast
            String demandForecast = generateDemandForecast(userInput, scrapedJson);
            result.setDemandForecast(demandForecast);
            
            // Generate recommendations
            String recommendations = generateRecommendations(userInput, metrics, fitScore);
            result.setRecommendations(recommendations);
            
        } catch (Exception e) {
            // Set default values if parsing fails
            setDefaultMetrics(result, userInput);
        }
        
        return result;
    }
    
    private double calculateFitScore(UserInput userInput, JsonNode scrapedData) {
        // Fit score = demand_score * margin_score * feasibility_score
        double demandScore = extractDemandScore(scrapedData);
        double marginScore = calculateMarginScore(userInput, scrapedData);
        double feasibilityScore = calculateFeasibilityScore(userInput);
        
        return (demandScore * marginScore * feasibilityScore) / 100.0; // Normalize to 0-10 scale
    }
    
    private double calculateSuggestedPrice(UserInput userInput, JsonNode scrapedData) {
        // suggested_price = procurement_cost + margin - competition_adjustment
        double procurementCost = estimateProcurementCost(userInput, scrapedData);
        double margin = procurementCost * getMarginMultiplier(userInput.getRiskProfile());
        double competitionAdjustment = calculateCompetitionAdjustment(scrapedData);
        
        return procurementCost + margin - competitionAdjustment;
    }
    
    private FinancialMetrics calculateFinancialMetrics(UserInput userInput, double suggestedPrice, double fitScore) {
        FinancialMetrics metrics = new FinancialMetrics();
        
        // Estimate monthly sales volume based on fit score and market conditions
        int monthlySalesVolume = (int) (fitScore * 100 * getVolumeMultiplier(userInput.getWorkType()));
        
        // Revenue = Price × Quantity
        metrics.expectedRevenue = suggestedPrice * monthlySalesVolume;
        
        // Calculate costs
        double fixedCosts = estimateFixedCosts(userInput);
        double variableCosts = monthlySalesVolume * (suggestedPrice * 0.6); // 60% of price as variable cost
        double logisticsCosts = monthlySalesVolume * getLogisticsCost(userInput.getDeliveryCapability());
        double marketingCosts = metrics.expectedRevenue * 0.05; // 5% of revenue
        
        // Net Profit = Revenue – (Fixed + Variable + Logistics + Marketing)
        metrics.netProfit = metrics.expectedRevenue - (fixedCosts + variableCosts + logisticsCosts + marketingCosts);
        
        // ROI calculation
        double initialInvestment = (userInput.getCapitalMin() + userInput.getCapitalMax()) / 2;
        metrics.roiPercentage = (metrics.netProfit * 12) / initialInvestment * 100; // Annual ROI
        
        // Payback period
        if (metrics.netProfit > 0) {
            metrics.paybackPeriodMonths = (int) Math.ceil(initialInvestment / metrics.netProfit);
        } else {
            metrics.paybackPeriodMonths = 999; // Indicates no payback
        }
        
        return metrics;
    }
    
    private String generateDemandForecast(UserInput userInput, JsonNode scrapedData) {
        // Generate forecast data (simplified Prophet-like forecast)
        StringBuilder forecast = new StringBuilder("{\"forecast\": [");
        
        for (int i = 1; i <= 12; i++) {
            double baseValue = 1000 + (random.nextGaussian() * 100);
            double seasonalEffect = Math.sin(i * Math.PI / 6) * 200; // Seasonal variation
            double trendEffect = i * 50; // Growth trend
            
            double forecastValue = Math.max(0, baseValue + seasonalEffect + trendEffect);
            
            if (i > 1) forecast.append(",");
            forecast.append(String.format(
                "{\"month\": %d, \"demand\": %.0f, \"confidence_lower\": %.0f, \"confidence_upper\": %.0f}",
                i, forecastValue, forecastValue * 0.8, forecastValue * 1.2
            ));
        }
        
        forecast.append("]}");
        return forecast.toString();
    }
    
    private String generateRecommendations(UserInput userInput, FinancialMetrics metrics, double fitScore) {
        return String.format("""
        {
            "top_recommendations": [
                {
                    "title": "Optimize Product Mix",
                    "description": "Focus on high-demand products with fit score above %.1f",
                    "priority": "high"
                },
                {
                    "title": "Strategic Pricing",
                    "description": "Maintain %.0f%% margin while staying competitive",
                    "priority": "medium"
                },
                {
                    "title": "Market Entry Strategy",
                    "description": "Start with %s channel in %s market",
                    "priority": "high"
                }
            ],
            "risk_mitigation": [
                "Diversify product portfolio",
                "Monitor competitor pricing regularly",
                "Build strong supplier relationships"
            ],
            "growth_opportunities": [
                "Expand to adjacent markets",
                "Consider seasonal product variations",
                "Leverage digital marketing channels"
            ]
        }
        """,
        fitScore,
        getMarginMultiplier(userInput.getRiskProfile()) * 100,
        userInput.getSellingChannel(),
        userInput.getLocation()
        );
    }
    
    // Helper methods
    private double extractDemandScore(JsonNode scrapedData) {
        try {
            return scrapedData.path("products").get(0).path("demand_score").asDouble(7.0);
        } catch (Exception e) {
            return 7.0; // Default demand score
        }
    }
    
    private double calculateMarginScore(UserInput userInput, JsonNode scrapedData) {
        // Higher margin potential = higher score
        return switch (userInput.getRiskProfile().toLowerCase()) {
            case "conservative" -> 6.0;
            case "balanced" -> 7.5;
            case "aggressive" -> 9.0;
            default -> 7.0;
        };
    }
    
    private double calculateFeasibilityScore(UserInput userInput) {
        double capitalScore = Math.min(10.0, userInput.getCapitalMin() / 10000.0); // Normalize capital
        double workTypeScore = "full-time".equals(userInput.getWorkType()) ? 9.0 : 7.0;
        return (capitalScore + workTypeScore) / 2.0;
    }
    
    private double estimateProcurementCost(UserInput userInput, JsonNode scrapedData) {
        try {
            JsonNode priceRange = scrapedData.path("avg_price_range");
            return priceRange.get(0).asDouble(100.0) * 0.7; // 70% of market price
        } catch (Exception e) {
            return 100.0; // Default procurement cost
        }
    }
    
    private double getMarginMultiplier(String riskProfile) {
        return switch (riskProfile.toLowerCase()) {
            case "conservative" -> 0.20; // 20% margin
            case "balanced" -> 0.30; // 30% margin
            case "aggressive" -> 0.40; // 40% margin
            default -> 0.25;
        };
    }
    
    private double calculateCompetitionAdjustment(JsonNode scrapedData) {
        try {
            String competitionLevel = scrapedData.path("products").get(0).path("competition_level").asText("medium");
            return switch (competitionLevel.toLowerCase()) {
                case "low" -> 0.0;
                case "medium" -> 10.0;
                case "high" -> 25.0;
                default -> 15.0;
            };
        } catch (Exception e) {
            return 15.0;
        }
    }
    
    private double getVolumeMultiplier(String workType) {
        return "full-time".equals(workType) ? 1.0 : 0.6;
    }
    
    private double estimateFixedCosts(UserInput userInput) {
        double baseCost = "online".equals(userInput.getSellingChannel()) ? 5000.0 : 10000.0;
        return baseCost + (userInput.getCapitalMin() * 0.1); // 10% of min capital as fixed costs
    }
    
    private double getLogisticsCost(String deliveryCapability) {
        return "own".equals(deliveryCapability) ? 15.0 : 25.0; // Per unit logistics cost
    }
    
    private void setDefaultMetrics(AnalysisResult result, UserInput userInput) {
        result.setFitScore(7.0);
        result.setSuggestedPrice(200.0);
        result.setExpectedRevenue(50000.0);
        result.setNetProfit(15000.0);
        result.setRoiPercentage(25.0);
        result.setPaybackPeriodMonths(8);
        result.setDemandForecast("{\"forecast\": [{\"month\": 1, \"demand\": 1000}]}");
        result.setRecommendations("{\"recommendations\": [\"Focus on market research\", \"Start with small investment\"]}");
    }
    
    // Inner class for financial metrics
    private static class FinancialMetrics {
        public double expectedRevenue;
        public double netProfit;
        public double roiPercentage;
        public int paybackPeriodMonths;
    }
}