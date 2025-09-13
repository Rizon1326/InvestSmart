export interface UserInput {
  location: string;
  businessInterest: string;
  capitalMin: number;
  capitalMax: number;
  riskProfile: string;
  targetIncome: number;
  incomePeriod: string;
  workType: string;
  sellingChannel: string;
  seasonalPreference?: string;
  deliveryCapability: string;
}

export interface AnalysisResult {
  id: number;
  userInput: UserInput;
  fitScore: number;
  suggestedPrice: number;
  expectedRevenue: number;
  netProfit: number;
  roiPercentage: number;
  paybackPeriodMonths: number;
  demandForecast: string; // JSON string
  recommendations: string; // JSON string
  aiAnalysis: string;
  createdAt: string;
}

export interface ForecastData {
  month: number;
  demand: number;
  confidence_lower: number;
  confidence_upper: number;
}

export interface RecommendationData {
  top_recommendations: Recommendation[];
  risk_mitigation: string[];
  growth_opportunities: string[];
}

export interface Recommendation {
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
}

export interface ChartDataPoint {
  month: string;
  value: number;
  lower?: number;
  upper?: number;
}

export interface KPIMetric {
  label: string;
  value: string | number;
  unit?: string;
  trend?: 'up' | 'down' | 'stable';
}

export interface ScenarioData {
  best: FinancialMetrics;
  expected: FinancialMetrics;
  worst: FinancialMetrics;
}

export interface FinancialMetrics {
  monthly_revenue: number;
  monthly_profit: number;
  annual_profit: number;
  roi_percentage: number;
  payback_period_months: number;
  break_even_units: number;
  margin_percentage: number;
}

export interface MonteCarloResults {
  simulation_stats: {
    [key: string]: {
      mean: number;
      median: number;
      std_dev: number;
      min: number;
      max: number;
      percentile_5: number;
      percentile_25: number;
      percentile_75: number;
      percentile_95: number;
    };
  };
  probability_positive_roi: number;
  probability_target_met: number;
  iterations: number;
  risk_metrics: {
    value_at_risk_5: number;
    expected_shortfall_5: number;
  };
}