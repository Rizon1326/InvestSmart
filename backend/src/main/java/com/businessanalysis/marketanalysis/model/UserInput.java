package com.businessanalysis.marketanalysis.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "user_inputs")
public class UserInput {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotBlank(message = "Location is required")
    @Column(name = "location")
    private String location;
    
    @NotBlank(message = "Business interest is required")
    @Column(name = "business_interest")
    private String businessInterest;
    
    @DecimalMin(value = "0.0", message = "Minimum capital must be positive")
    @Column(name = "capital_min")
    private Double capitalMin;
    
    @DecimalMin(value = "0.0", message = "Maximum capital must be positive")
    @Column(name = "capital_max")
    private Double capitalMax;
    
    @NotBlank(message = "Risk profile is required")
    @Column(name = "risk_profile")
    private String riskProfile;
    
    @DecimalMin(value = "0.0", message = "Target income must be positive")
    @Column(name = "target_income")
    private Double targetIncome;
    
    @NotBlank(message = "Income period is required")
    @Column(name = "income_period")
    private String incomePeriod; // monthly / yearly
    
    @NotBlank(message = "Work type is required")
    @Column(name = "work_type")
    private String workType; // full-time / part-time
    
    @NotBlank(message = "Selling channel is required")
    @Column(name = "selling_channel")
    private String sellingChannel; // online / offline
    
    @Column(name = "seasonal_preference")
    private String seasonalPreference;
    
    @NotBlank(message = "Delivery capability is required")
    @Column(name = "delivery_capability")
    private String deliveryCapability; // own / third-party
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    // Constructors
    public UserInput() {}
    
    public UserInput(String location, String businessInterest, Double capitalMin, 
                    Double capitalMax, String riskProfile, Double targetIncome,
                    String incomePeriod, String workType, String sellingChannel,
                    String seasonalPreference, String deliveryCapability) {
        this.location = location;
        this.businessInterest = businessInterest;
        this.capitalMin = capitalMin;
        this.capitalMax = capitalMax;
        this.riskProfile = riskProfile;
        this.targetIncome = targetIncome;
        this.incomePeriod = incomePeriod;
        this.workType = workType;
        this.sellingChannel = sellingChannel;
        this.seasonalPreference = seasonalPreference;
        this.deliveryCapability = deliveryCapability;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }
    
    public String getBusinessInterest() { return businessInterest; }
    public void setBusinessInterest(String businessInterest) { this.businessInterest = businessInterest; }
    
    public Double getCapitalMin() { return capitalMin; }
    public void setCapitalMin(Double capitalMin) { this.capitalMin = capitalMin; }
    
    public Double getCapitalMax() { return capitalMax; }
    public void setCapitalMax(Double capitalMax) { this.capitalMax = capitalMax; }
    
    public String getRiskProfile() { return riskProfile; }
    public void setRiskProfile(String riskProfile) { this.riskProfile = riskProfile; }
    
    public Double getTargetIncome() { return targetIncome; }
    public void setTargetIncome(Double targetIncome) { this.targetIncome = targetIncome; }
    
    public String getIncomePeriod() { return incomePeriod; }
    public void setIncomePeriod(String incomePeriod) { this.incomePeriod = incomePeriod; }
    
    public String getWorkType() { return workType; }
    public void setWorkType(String workType) { this.workType = workType; }
    
    public String getSellingChannel() { return sellingChannel; }
    public void setSellingChannel(String sellingChannel) { this.sellingChannel = sellingChannel; }
    
    public String getSeasonalPreference() { return seasonalPreference; }
    public void setSeasonalPreference(String seasonalPreference) { this.seasonalPreference = seasonalPreference; }
    
    public String getDeliveryCapability() { return deliveryCapability; }
    public void setDeliveryCapability(String deliveryCapability) { this.deliveryCapability = deliveryCapability; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}