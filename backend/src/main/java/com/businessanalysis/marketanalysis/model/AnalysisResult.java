package com.businessanalysis.marketanalysis.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "analysis_results")
public class AnalysisResult {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @OneToOne
    @JoinColumn(name = "user_input_id")
    private UserInput userInput;
    
    @Column(name = "fit_score")
    private Double fitScore;
    
    @Column(name = "suggested_price")
    private Double suggestedPrice;
    
    @Column(name = "expected_revenue")
    private Double expectedRevenue;
    
    @Column(name = "net_profit")
    private Double netProfit;
    
    @Column(name = "roi_percentage")
    private Double roiPercentage;
    
    @Column(name = "payback_period_months")
    private Integer paybackPeriodMonths;
    
    @Column(name = "demand_forecast", columnDefinition = "TEXT")
    private String demandForecast; // JSON string
    
    @Column(name = "recommendations", columnDefinition = "TEXT")
    private String recommendations; // JSON string
    
    @Column(name = "ai_analysis", columnDefinition = "TEXT")
    private String aiAnalysis;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    // Constructors
    public AnalysisResult() {
        this.createdAt = LocalDateTime.now();
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public UserInput getUserInput() { return userInput; }
    public void setUserInput(UserInput userInput) { this.userInput = userInput; }
    
    public Double getFitScore() { return fitScore; }
    public void setFitScore(Double fitScore) { this.fitScore = fitScore; }
    
    public Double getSuggestedPrice() { return suggestedPrice; }
    public void setSuggestedPrice(Double suggestedPrice) { this.suggestedPrice = suggestedPrice; }
    
    public Double getExpectedRevenue() { return expectedRevenue; }
    public void setExpectedRevenue(Double expectedRevenue) { this.expectedRevenue = expectedRevenue; }
    
    public Double getNetProfit() { return netProfit; }
    public void setNetProfit(Double netProfit) { this.netProfit = netProfit; }
    
    public Double getRoiPercentage() { return roiPercentage; }
    public void setRoiPercentage(Double roiPercentage) { this.roiPercentage = roiPercentage; }
    
    public Integer getPaybackPeriodMonths() { return paybackPeriodMonths; }
    public void setPaybackPeriodMonths(Integer paybackPeriodMonths) { this.paybackPeriodMonths = paybackPeriodMonths; }
    
    public String getDemandForecast() { return demandForecast; }
    public void setDemandForecast(String demandForecast) { this.demandForecast = demandForecast; }
    
    public String getRecommendations() { return recommendations; }
    public void setRecommendations(String recommendations) { this.recommendations = recommendations; }
    
    public String getAiAnalysis() { return aiAnalysis; }
    public void setAiAnalysis(String aiAnalysis) { this.aiAnalysis = aiAnalysis; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}