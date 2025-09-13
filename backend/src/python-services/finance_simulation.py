import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging

class FinanceSimulationService:
    """
    Finance simulation service implementing Monte Carlo analysis and ROI calculations
    Based on the formulas from the context:
    - Revenue = Price × Quantity
    - Net Profit = Revenue – (Fixed + Variable + Logistics + Marketing)
    - ROI calculations with deterministic and probabilistic scenarios
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def calculate_deterministic_scenarios(self, user_input: dict, market_data: dict) -> dict:
        """Calculate best, expected, and worst case scenarios"""
        
        base_params = self._extract_base_parameters(user_input, market_data)
        
        # Scenario multipliers
        scenarios = {
            'best': {'demand': 1.3, 'price': 1.1, 'costs': 0.9},
            'expected': {'demand': 1.0, 'price': 1.0, 'costs': 1.0},
            'worst': {'demand': 0.7, 'price': 0.9, 'costs': 1.2}
        }
        
        results = {}
        
        for scenario_name, multipliers in scenarios.items():
            # Adjust parameters for scenario
            adjusted_params = base_params.copy()
            adjusted_params['monthly_demand'] *= multipliers['demand']
            adjusted_params['unit_price'] *= multipliers['price']
            adjusted_params['fixed_costs'] *= multipliers['costs']
            adjusted_params['variable_cost_per_unit'] *= multipliers['costs']
            
            # Calculate metrics
            monthly_revenue = adjusted_params['unit_price'] * adjusted_params['monthly_demand']
            monthly_variable_costs = adjusted_params['variable_cost_per_unit'] * adjusted_params['monthly_demand']
            monthly_logistics = adjusted_params['logistics_cost_per_unit'] * adjusted_params['monthly_demand']
            monthly_marketing = monthly_revenue * adjusted_params['marketing_rate']
            
            monthly_profit = monthly_revenue - (
                adjusted_params['fixed_costs'] +
                monthly_variable_costs +
                monthly_logistics +
                monthly_marketing
            )
            
            annual_profit = monthly_profit * 12
            roi_percentage = (annual_profit / adjusted_params['initial_investment']) * 100
            payback_months = adjusted_params['initial_investment'] / monthly_profit if monthly_profit > 0 else 999
            
            results[scenario_name] = {
                'monthly_revenue': monthly_revenue,
                'monthly_profit': monthly_profit,
                'annual_profit': annual_profit,
                'roi_percentage': roi_percentage,
                'payback_period_months': min(int(payback_months), 999),
                'break_even_units': self._calculate_break_even(adjusted_params),
                'margin_percentage': ((adjusted_params['unit_price'] - adjusted_params['variable_cost_per_unit']) / adjusted_params['unit_price']) * 100
            }
        
        return results
    
    def monte_carlo_simulation(self, user_input: dict, market_data: dict, iterations: int = 1000) -> dict:
        """Run Monte Carlo simulation with 1000 iterations for ROI probability distribution"""
        
        base_params = self._extract_base_parameters(user_input, market_data)
        
        # Define probability distributions for key variables
        simulation_results = {
            'monthly_revenue': [],
            'monthly_profit': [],
            'roi_percentage': [],
            'payback_months': []
        }
        
        for i in range(iterations):
            # Sample from distributions
            sampled_params = self._sample_parameters(base_params)
            
            # Calculate metrics for this iteration
            monthly_revenue = sampled_params['unit_price'] * sampled_params['monthly_demand']
            
            monthly_costs = (
                sampled_params['fixed_costs'] +
                (sampled_params['variable_cost_per_unit'] * sampled_params['monthly_demand']) +
                (sampled_params['logistics_cost_per_unit'] * sampled_params['monthly_demand']) +
                (monthly_revenue * sampled_params['marketing_rate'])
            )
            
            monthly_profit = monthly_revenue - monthly_costs
            annual_profit = monthly_profit * 12
            roi_percentage = (annual_profit / sampled_params['initial_investment']) * 100
            payback_months = sampled_params['initial_investment'] / monthly_profit if monthly_profit > 0 else 999
            
            # Store results
            simulation_results['monthly_revenue'].append(monthly_revenue)
            simulation_results['monthly_profit'].append(monthly_profit)
            simulation_results['roi_percentage'].append(roi_percentage)
            simulation_results['payback_months'].append(min(payback_months, 999))
        
        # Calculate statistics
        stats = {}
        for metric, values in simulation_results.items():
            values_array = np.array(values)
            stats[metric] = {
                'mean': float(np.mean(values_array)),
                'median': float(np.median(values_array)),
                'std_dev': float(np.std(values_array)),
                'min': float(np.min(values_array)),
                'max': float(np.max(values_array)),
                'percentile_5': float(np.percentile(values_array, 5)),
                'percentile_25': float(np.percentile(values_array, 25)),
                'percentile_75': float(np.percentile(values_array, 75)),
                'percentile_95': float(np.percentile(values_array, 95))
            }
        
        # Calculate probability of positive ROI
        positive_roi_count = sum(1 for roi in simulation_results['roi_percentage'] if roi > 0)
        probability_positive_roi = positive_roi_count / iterations
        
        # Calculate probability of meeting target income
        target_monthly_income = user_input.get('target_income', 0)
        target_met_count = sum(1 for profit in simulation_results['monthly_profit'] if profit >= target_monthly_income)
        probability_target_met = target_met_count / iterations
        
        return {
            'simulation_stats': stats,
            'probability_positive_roi': probability_positive_roi,
            'probability_target_met': probability_target_met,
            'iterations': iterations,
            'risk_metrics': {
                'value_at_risk_5': stats['monthly_profit']['percentile_5'],  # 5% VaR
                'expected_shortfall_5': np.mean([p for p in simulation_results['monthly_profit'] if p <= stats['monthly_profit']['percentile_5']])
            }
        }
    
    def supply_chain_cost_analysis(self, user_input: dict, market_data: dict) -> dict:
        """Analyze supply chain costs including logistics, inventory, and supplier factors"""
        
        location = user_input.get('location', 'Dhaka')
        business_type = user_input.get('business_interest', 'food')
        selling_channel = user_input.get('selling_channel', 'online')
        delivery_capability = user_input.get('delivery_capability', 'third-party')
        
        # Location-based cost factors (Bangladesh districts)
        location_factors = {
            'dhaka': 1.0, 'chittagong': 1.1, 'sylhet': 1.2, 'rajshahi': 1.15,
            'khulna': 1.1, 'barishal': 1.25, 'rangpur': 1.3, 'mymensingh': 1.2
        }
        
        location_factor = location_factors.get(location.lower(), 1.2)  # Default for other districts
        
        # Base costs (BDT)
        base_costs = {
            'procurement_per_unit': 100 * location_factor,
            'storage_cost_per_unit_per_month': 5 * location_factor,
            'transportation_per_unit': 15 * location_factor if delivery_capability == 'own' else 25 * location_factor,
            'handling_cost_per_unit': 8 * location_factor
        }
        
        # Business type adjustments
        business_multipliers = {
            'food': {'procurement': 1.0, 'storage': 1.5, 'transport': 1.2},  # Higher storage for perishables
            'retail': {'procurement': 1.2, 'storage': 1.0, 'transport': 1.0},
            'electronics': {'procurement': 1.5, 'storage': 0.8, 'transport': 1.1},
            'beauty': {'procurement': 1.1, 'storage': 0.9, 'transport': 1.0}
        }
        
        multiplier = business_multipliers.get(business_type.lower(), business_multipliers['retail'])
        
        # Adjust costs
        supply_chain_costs = {
            'procurement_cost_per_unit': base_costs['procurement_per_unit'] * multiplier['procurement'],
            'storage_cost_per_unit_per_month': base_costs['storage_cost_per_unit_per_month'] * multiplier['storage'],
            'transportation_cost_per_unit': base_costs['transportation_per_unit'] * multiplier['transport'],
            'handling_cost_per_unit': base_costs['handling_cost_per_unit']
        }
        
        # Supplier availability index (0-1 scale)
        supplier_availability = self._calculate_supplier_availability(location, business_type)
        
        # Inventory holding costs
        monthly_demand = self._estimate_monthly_demand(user_input, market_data)
        average_inventory = monthly_demand * 0.5  # Assuming economic order quantity
        monthly_inventory_cost = average_inventory * supply_chain_costs['storage_cost_per_unit_per_month']
        
        return {
            'supply_chain_costs': supply_chain_costs,
            'location_factor': location_factor,
            'supplier_availability_index': supplier_availability,
            'monthly_inventory_cost': monthly_inventory_cost,
            'total_cost_per_unit': sum([
                supply_chain_costs['procurement_cost_per_unit'],
                supply_chain_costs['storage_cost_per_unit_per_month'],
                supply_chain_costs['transportation_cost_per_unit'],
                supply_chain_costs['handling_cost_per_unit']
            ]),
            'recommendations': self._generate_supply_chain_recommendations(supply_chain_costs, supplier_availability)
        }
    
    def cash_flow_projection(self, user_input: dict, financial_metrics: dict, periods: int = 24) -> dict:
        """Generate monthly cash flow projections"""
        
        initial_investment = (user_input.get('capital_min', 0) + user_input.get('capital_max', 0)) / 2
        monthly_revenue = financial_metrics.get('monthly_revenue', 0)
        monthly_profit = financial_metrics.get('monthly_profit', 0)
        
        cash_flow_data = []
        cumulative_cash_flow = -initial_investment  # Start with negative investment
        
        for month in range(1, periods + 1):
            # Add seasonal variations
            seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * month / 12)
            
            # Add growth trend
            growth_factor = 1 + (month * 0.02)  # 2% monthly growth
            
            monthly_cf = monthly_profit * seasonal_factor * growth_factor
            cumulative_cash_flow += monthly_cf
            
            cash_flow_data.append({
                'month': month,
                'monthly_cash_flow': monthly_cf,
                'cumulative_cash_flow': cumulative_cash_flow,
                'revenue': monthly_revenue * seasonal_factor * growth_factor,
                'break_even': cumulative_cash_flow >= 0
            })
        
        # Find break-even month
        break_even_month = next((cf['month'] for cf in cash_flow_data if cf['break_even']), None)
        
        return {
            'cash_flow_projection': cash_flow_data,
            'break_even_month': break_even_month,
            'final_cumulative_cf': cumulative_cash_flow,
            'total_investment_recovered': cumulative_cash_flow >= 0
        }
    
    def _extract_base_parameters(self, user_input: dict, market_data: dict) -> dict:
        """Extract base parameters for calculations"""
        
        # Parse market data
        if isinstance(market_data, str):
            try:
                market_data = json.loads(market_data)
            except:
                market_data = {}
        
        # Extract or estimate key parameters
        avg_price_range = market_data.get('avg_price_range', [150, 300])
        unit_price = (avg_price_range[0] + avg_price_range[1]) / 2
        
        # Investment and demand estimation
        initial_investment = (user_input.get('capital_min', 0) + user_input.get('capital_max', 0)) / 2
        monthly_demand = self._estimate_monthly_demand(user_input, market_data)
        
        # Cost estimates
        variable_cost_per_unit = unit_price * 0.6  # 60% of selling price
        logistics_cost_per_unit = 25 if user_input.get('delivery_capability') == 'third-party' else 15
        fixed_costs = self._estimate_fixed_costs(user_input)
        
        return {
            'unit_price': unit_price,
            'monthly_demand': monthly_demand,
            'initial_investment': initial_investment,
            'fixed_costs': fixed_costs,
            'variable_cost_per_unit': variable_cost_per_unit,
            'logistics_cost_per_unit': logistics_cost_per_unit,
            'marketing_rate': 0.05  # 5% of revenue
        }
    
    def _sample_parameters(self, base_params: dict) -> dict:
        """Sample parameters from probability distributions for Monte Carlo"""
        
        sampled = base_params.copy()
        
        # Sample from normal distributions with appropriate standard deviations
        sampled['unit_price'] = max(0, np.random.normal(base_params['unit_price'], base_params['unit_price'] * 0.1))
        sampled['monthly_demand'] = max(0, np.random.normal(base_params['monthly_demand'], base_params['monthly_demand'] * 0.2))
        sampled['fixed_costs'] = max(0, np.random.normal(base_params['fixed_costs'], base_params['fixed_costs'] * 0.15))
        sampled['variable_cost_per_unit'] = max(0, np.random.normal(base_params['variable_cost_per_unit'], base_params['variable_cost_per_unit'] * 0.1))
        sampled['logistics_cost_per_unit'] = max(0, np.random.normal(base_params['logistics_cost_per_unit'], base_params['logistics_cost_per_unit'] * 0.2))
        
        return sampled
    
    def _estimate_monthly_demand(self, user_input: dict, market_data: dict) -> float:
        """Estimate monthly demand based on user input and market data"""
        
        base_demand = 1000  # Base monthly demand
        
        # Adjust for work type
        work_multiplier = 1.0 if user_input.get('work_type') == 'full-time' else 0.6
        
        # Adjust for capital (higher capital = higher demand potential)
        capital_avg = (user_input.get('capital_min', 0) + user_input.get('capital_max', 0)) / 2
        capital_multiplier = min(2.0, 1 + (capital_avg / 100000))  # Max 2x multiplier
        
        # Adjust for risk profile
        risk_multipliers = {'conservative': 0.8, 'balanced': 1.0, 'aggressive': 1.3}
        risk_multiplier = risk_multipliers.get(user_input.get('risk_profile', 'balanced'), 1.0)
        
        return base_demand * work_multiplier * capital_multiplier * risk_multiplier
    
    def _estimate_fixed_costs(self, user_input: dict) -> float:
        """Estimate monthly fixed costs"""
        
        base_fixed = 10000  # Base monthly fixed costs (BDT)
        
        # Adjust for selling channel
        channel_multiplier = 0.7 if user_input.get('selling_channel') == 'online' else 1.0
        
        # Adjust for location (Dhaka is more expensive)
        location_multipliers = {'dhaka': 1.2, 'chittagong': 1.0, 'sylhet': 0.9}
        location_multiplier = location_multipliers.get(user_input.get('location', '').lower(), 1.0)
        
        return base_fixed * channel_multiplier * location_multiplier
    
    def _calculate_break_even(self, params: dict) -> float:
        """Calculate break-even point in units"""
        
        contribution_per_unit = params['unit_price'] - params['variable_cost_per_unit'] - params['logistics_cost_per_unit']
        
        if contribution_per_unit <= 0:
            return float('inf')
        
        return params['fixed_costs'] / contribution_per_unit
    
    def _calculate_supplier_availability(self, location: str, business_type: str) -> float:
        """Calculate supplier availability index (0-1)"""
        
        # Base availability by location
        location_availability = {
            'dhaka': 0.9, 'chittagong': 0.8, 'sylhet': 0.7, 'rajshahi': 0.75,
            'khulna': 0.7, 'barishal': 0.6, 'rangpur': 0.65, 'mymensingh': 0.7
        }
        
        # Business type adjustments
        business_adjustments = {
            'food': 0.9,      # Good supplier network
            'retail': 0.85,   # Moderate supplier network
            'electronics': 0.7,  # Limited local suppliers
            'beauty': 0.8     # Growing supplier network
        }
        
        base_availability = location_availability.get(location.lower(), 0.6)
        business_factor = business_adjustments.get(business_type.lower(), 0.75)
        
        return base_availability * business_factor
    
    def _generate_supply_chain_recommendations(self, costs: dict, supplier_availability: float) -> list:
        """Generate supply chain optimization recommendations"""
        
        recommendations = []
        
        if supplier_availability < 0.7:
            recommendations.append("Consider diversifying supplier base to reduce dependency risk")
        
        if costs['transportation_cost_per_unit'] > 25:
            recommendations.append("Explore bulk shipping options to reduce per-unit transportation costs")
        
        if costs['storage_cost_per_unit_per_month'] > 8:
            recommendations.append("Implement just-in-time inventory management to reduce storage costs")
        
        recommendations.append("Negotiate volume discounts with suppliers for procurement cost optimization")
        
        return recommendations

# Example usage and testing
if __name__ == "__main__":
    finance_service = FinanceSimulationService()
    
    # Example user input
    sample_user_input = {
        'location': 'Dhaka',
        'business_interest': 'food',
        'capital_min': 50000,
        'capital_max': 100000,
        'risk_profile': 'balanced',
        'target_income': 25000,
        'work_type': 'full-time',
        'selling_channel': 'online',
        'delivery_capability': 'third-party'
    }
    
    sample_market_data = {
        'avg_price_range': [180, 320],
        'products': [{'demand_score': 8.0}]
    }
    
    # Run deterministic scenarios
    scenarios = finance_service.calculate_deterministic_scenarios(sample_user_input, sample_market_data)
    print("Deterministic Scenarios:", json.dumps(scenarios, indent=2))
    
    # Run Monte Carlo simulation
    mc_results = finance_service.monte_carlo_simulation(sample_user_input, sample_market_data, 100)  # Reduced iterations for demo
    print("Monte Carlo Results:", json.dumps(mc_results, indent=2, default=str))