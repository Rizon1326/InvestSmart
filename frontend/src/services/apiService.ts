import axios from 'axios';
import { UserInput, AnalysisResult } from '../types/types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('Making API request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Market analysis endpoint
  analyzeMarket: async (userInput: UserInput): Promise<AnalysisResult> => {
    try {
      const response = await api.post<AnalysisResult>('/market-analysis/analyze', userInput);
      return response.data;
    } catch (error) {
      console.error('Market analysis failed:', error);
      throw new Error('Failed to analyze market data');
    }
  },

  // Get analysis result by ID
  getAnalysisResult: async (id: number): Promise<AnalysisResult> => {
    try {
      const response = await api.get<AnalysisResult>(`/market-analysis/result/${id}`);
      return response.data;
    } catch (error) {
      console.error('Failed to get analysis result:', error);
      throw new Error('Failed to retrieve analysis result');
    }
  },

  // Health check
  healthCheck: async (): Promise<string> => {
    try {
      const response = await api.get<string>('/market-analysis/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw new Error('API health check failed');
    }
  },

  // Mock analysis for development/testing
  mockAnalyzeMarket: async (userInput: UserInput): Promise<AnalysisResult> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    return {
      id: Date.now(),
      userInput,
      fitScore: 7.5 + Math.random() * 2,
      suggestedPrice: 200 + Math.random() * 100,
      expectedRevenue: 45000 + Math.random() * 20000,
      netProfit: 15000 + Math.random() * 10000,
      roiPercentage: 20 + Math.random() * 15,
      paybackPeriodMonths: Math.floor(6 + Math.random() * 12),
      demandForecast: JSON.stringify({
        forecast: Array.from({ length: 12 }, (_, i) => ({
          month: i + 1,
          demand: 1000 + Math.random() * 500 + (i * 50),
          confidence_lower: (1000 + Math.random() * 500 + (i * 50)) * 0.8,
          confidence_upper: (1000 + Math.random() * 500 + (i * 50)) * 1.2
        }))
      }),
      recommendations: JSON.stringify({
        top_recommendations: [
          {
            title: "Optimize Product Mix",
            description: `Focus on high-demand products in ${userInput.businessInterest}`,
            priority: "high"
          },
          {
            title: "Strategic Pricing",
            description: "Maintain competitive pricing with 25-30% margin",
            priority: "medium"
          },
          {
            title: "Market Entry Strategy", 
            description: `Start with ${userInput.sellingChannel} channel in ${userInput.location}`,
            priority: "high"
          }
        ],
        risk_mitigation: [
          "Diversify product portfolio",
          "Monitor competitor pricing regularly",
          "Build strong supplier relationships"
        ],
        growth_opportunities: [
          "Expand to adjacent markets",
          "Consider seasonal product variations",
          "Leverage digital marketing channels"
        ]
      }),
      aiAnalysis: JSON.stringify({
        analysis: `Based on market analysis for ${userInput.businessInterest} in ${userInput.location}, there are strong opportunities with your capital range of ${userInput.capitalMin}-${userInput.capitalMax} BDT.`,
        demand_score: 8.2,
        market_opportunity: "High potential market with growing demand",
        pricing_strategy: "Competitive pricing with 25-30% margin recommended",
        risk_level: userInput.riskProfile,
        revenue_potential: `Monthly revenue potential of ${userInput.targetIncome * 0.8}-${userInput.targetIncome * 1.2} BDT`
      }),
      createdAt: new Date().toISOString()
    };
  }
};

// Use mock service in development if API is not available
const shouldUseMock = process.env.NODE_ENV === 'development' && !process.env.REACT_APP_USE_REAL_API;

if (shouldUseMock) {
  // Override with mock service in development
  apiService.analyzeMarket = apiService.mockAnalyzeMarket;
}