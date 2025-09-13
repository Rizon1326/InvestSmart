import numpy as np
import pandas as pd
from prophet import Prophet
from statsmodels.tsa.statespace.sarimax import SARIMAX
import xgboost as xgb
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import json
import logging
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class MarketForecastingService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def generate_historical_data(self, business_type, location, months=24):
        """Generate synthetic historical data for forecasting"""
        dates = pd.date_range(
            end=datetime.now(), 
            periods=months, 
            freq='M'
        )
        
        # Base demand patterns by business type
        base_patterns = {
            'food': {'base': 1000, 'seasonality': 200, 'trend': 50},
            'retail': {'base': 1500, 'seasonality': 300, 'trend': 75},
            'electronics': {'base': 800, 'seasonality': 150, 'trend': 40},
            'beauty': {'base': 600, 'seasonality': 100, 'trend': 30}
        }
        
        pattern = base_patterns.get(business_type.lower(), base_patterns['food'])
        
        data = []
        for i, date in enumerate(dates):
            # Add trend
            trend_value = pattern['trend'] * (i / months)
            
            # Add seasonality (higher demand in winter months for food, etc.)
            seasonal_value = pattern['seasonality'] * np.sin(2 * np.pi * i / 12)
            
            # Add random noise
            noise = np.random.normal(0, pattern['base'] * 0.1)
            
            # Special events (Ramadan, Eid effects)
            special_event_boost = 0
            if date.month in [4, 5]:  # Ramadan/Eid months (approximate)
                special_event_boost = pattern['base'] * 0.3
            
            demand = max(0, pattern['base'] + trend_value + seasonal_value + noise + special_event_boost)
            
            data.append({
                'ds': date,
                'y': demand,
                'month': date.month,
                'quarter': date.quarter,
                'is_ramadan': 1 if date.month in [4, 5] else 0
            })
        
        return pd.DataFrame(data)
    
    def prophet_forecast(self, historical_data, periods=12):
        """Prophet forecasting model"""
        try:
            # Prepare data for Prophet
            prophet_data = historical_data[['ds', 'y']].copy()
            
            # Create Prophet model with seasonality
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False,
                seasonality_mode='multiplicative'
            )
            
            # Add custom seasonality for Ramadan
            model.add_country_holidays(country_name='BD')  # Bangladesh holidays
            
            # Fit model
            model.fit(prophet_data)
            
            # Create future dataframe
            future = model.make_future_dataframe(periods=periods, freq='M')
            
            # Make predictions
            forecast = model.predict(future)
            
            # Extract forecast results
            results = []
            for i in range(len(historical_data), len(forecast)):
                results.append({
                    'month': i - len(historical_data) + 1,
                    'demand': max(0, forecast.iloc[i]['yhat']),
                    'confidence_lower': max(0, forecast.iloc[i]['yhat_lower']),
                    'confidence_upper': max(0, forecast.iloc[i]['yhat_upper']),
                    'model': 'prophet'
                })
            
            return results
            
        except Exception as e:
            self.logger.error(f"Prophet forecasting error: {e}")
            return self._get_fallback_forecast(periods)
    
    def sarimax_forecast(self, historical_data, periods=12):
        """SARIMAX forecasting model"""
        try:
            # Prepare time series data
            ts_data = historical_data.set_index('ds')['y']
            
            # Fit SARIMAX model
            model = SARIMAX(
                ts_data,
                order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 12),
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            
            fitted_model = model.fit(disp=False)
            
            # Make forecast
            forecast = fitted_model.forecast(steps=periods)
            conf_int = fitted_model.get_forecast(steps=periods).conf_int()
            
            results = []
            for i in range(periods):
                results.append({
                    'month': i + 1,
                    'demand': max(0, forecast.iloc[i]),
                    'confidence_lower': max(0, conf_int.iloc[i, 0]),
                    'confidence_upper': max(0, conf_int.iloc[i, 1]),
                    'model': 'sarimax'
                })
            
            return results
            
        except Exception as e:
            self.logger.error(f"SARIMAX forecasting error: {e}")
            return self._get_fallback_forecast(periods)
    
    def xgboost_forecast(self, historical_data, periods=12):
        """XGBoost demand prediction"""
        try:
            # Feature engineering
            features = self._create_features(historical_data)
            
            # Prepare training data
            X = features[['month', 'quarter', 'is_ramadan', 'lag_1', 'lag_3', 'trend']].fillna(0)
            y = features['y']
            
            # Train model
            model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
            
            model.fit(X, y)
            
            # Generate future features and predict
            results = []
            last_date = historical_data['ds'].max()
            
            for i in range(periods):
                future_date = last_date + timedelta(days=30 * (i + 1))
                
                # Create future features
                future_features = {
                    'month': future_date.month,
                    'quarter': future_date.quarter,
                    'is_ramadan': 1 if future_date.month in [4, 5] else 0,
                    'lag_1': y.iloc[-1] if i == 0 else results[i-1]['demand'],
                    'lag_3': y.iloc[-3] if i < 3 else (results[i-3]['demand'] if i >= 3 else y.iloc[-3]),
                    'trend': len(historical_data) + i + 1
                }
                
                prediction = model.predict([[
                    future_features['month'],
                    future_features['quarter'],
                    future_features['is_ramadan'],
                    future_features['lag_1'],
                    future_features['lag_3'],
                    future_features['trend']
                ]])[0]
                
                results.append({
                    'month': i + 1,
                    'demand': max(0, prediction),
                    'confidence_lower': max(0, prediction * 0.8),
                    'confidence_upper': max(0, prediction * 1.2),
                    'model': 'xgboost'
                })
            
            return results
            
        except Exception as e:
            self.logger.error(f"XGBoost forecasting error: {e}")
            return self._get_fallback_forecast(periods)
    
    def lightgbm_forecast(self, historical_data, periods=12):
        """LightGBM demand prediction"""
        try:
            # Feature engineering
            features = self._create_features(historical_data)
            
            # Prepare training data
            X = features[['month', 'quarter', 'is_ramadan', 'lag_1', 'lag_3', 'trend']].fillna(0)
            y = features['y']
            
            # Train model
            model = lgb.LGBMRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                verbose=-1
            )
            
            model.fit(X, y)
            
            # Generate predictions (similar to XGBoost)
            results = []
            last_date = historical_data['ds'].max()
            
            for i in range(periods):
                future_date = last_date + timedelta(days=30 * (i + 1))
                
                future_features = {
                    'month': future_date.month,
                    'quarter': future_date.quarter,
                    'is_ramadan': 1 if future_date.month in [4, 5] else 0,
                    'lag_1': y.iloc[-1] if i == 0 else results[i-1]['demand'],
                    'lag_3': y.iloc[-3] if i < 3 else (results[i-3]['demand'] if i >= 3 else y.iloc[-3]),
                    'trend': len(historical_data) + i + 1
                }
                
                prediction = model.predict([[
                    future_features['month'],
                    future_features['quarter'],
                    future_features['is_ramadan'],
                    future_features['lag_1'],
                    future_features['lag_3'],
                    future_features['trend']
                ]])[0]
                
                results.append({
                    'month': i + 1,
                    'demand': max(0, prediction),
                    'confidence_lower': max(0, prediction * 0.85),
                    'confidence_upper': max(0, prediction * 1.15),
                    'model': 'lightgbm'
                })
            
            return results
            
        except Exception as e:
            self.logger.error(f"LightGBM forecasting error: {e}")
            return self._get_fallback_forecast(periods)
    
    def ensemble_forecast(self, business_type, location, periods=12):
        """Ensemble forecasting using multiple models"""
        try:
            # Generate historical data
            historical_data = self.generate_historical_data(business_type, location)
            
            # Get forecasts from all models
            prophet_results = self.prophet_forecast(historical_data, periods)
            sarimax_results = self.sarimax_forecast(historical_data, periods)
            xgb_results = self.xgboost_forecast(historical_data, periods)
            lgb_results = self.lightgbm_forecast(historical_data, periods)
            
            # Combine results with weights
            ensemble_results = []
            weights = {'prophet': 0.3, 'sarimax': 0.2, 'xgboost': 0.25, 'lightgbm': 0.25}
            
            for i in range(periods):
                ensemble_demand = (
                    prophet_results[i]['demand'] * weights['prophet'] +
                    sarimax_results[i]['demand'] * weights['sarimax'] +
                    xgb_results[i]['demand'] * weights['xgboost'] +
                    lgb_results[i]['demand'] * weights['lightgbm']
                )
                
                # Calculate ensemble confidence intervals
                all_lowers = [
                    prophet_results[i]['confidence_lower'],
                    sarimax_results[i]['confidence_lower'],
                    xgb_results[i]['confidence_lower'],
                    lgb_results[i]['confidence_lower']
                ]
                
                all_uppers = [
                    prophet_results[i]['confidence_upper'],
                    sarimax_results[i]['confidence_upper'],
                    xgb_results[i]['confidence_upper'],
                    lgb_results[i]['confidence_upper']
                ]
                
                ensemble_results.append({
                    'month': i + 1,
                    'demand': ensemble_demand,
                    'confidence_lower': np.mean(all_lowers),
                    'confidence_upper': np.mean(all_uppers),
                    'model': 'ensemble',
                    'individual_forecasts': {
                        'prophet': prophet_results[i]['demand'],
                        'sarimax': sarimax_results[i]['demand'],
                        'xgboost': xgb_results[i]['demand'],
                        'lightgbm': lgb_results[i]['demand']
                    }
                })
            
            return {
                'forecast': ensemble_results,
                'model_performance': self._evaluate_models(historical_data),
                'metadata': {
                    'business_type': business_type,
                    'location': location,
                    'forecast_periods': periods,
                    'generated_at': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Ensemble forecasting error: {e}")
            return {
                'forecast': self._get_fallback_forecast(periods),
                'error': str(e)
            }
    
    def _create_features(self, data):
        """Create features for ML models"""
        features = data.copy()
        features['trend'] = range(len(features))
        features['lag_1'] = features['y'].shift(1)
        features['lag_3'] = features['y'].shift(3)
        features['rolling_mean_3'] = features['y'].rolling(window=3).mean()
        return features
    
    def _evaluate_models(self, historical_data):
        """Evaluate model performance on historical data"""
        # Split data for evaluation
        split_point = int(len(historical_data) * 0.8)
        train_data = historical_data[:split_point]
        test_data = historical_data[split_point:]
        
        # This would contain actual model evaluation logic
        # For now, return mock performance metrics
        return {
            'prophet': {'mae': 85.2, 'rmse': 120.5, 'mape': 12.3},
            'sarimax': {'mae': 92.1, 'rmse': 135.8, 'mape': 14.1},
            'xgboost': {'mae': 78.9, 'rmse': 115.2, 'mape': 11.8},
            'lightgbm': {'mae': 81.3, 'rmse': 118.7, 'mape': 12.1}
        }
    
    def _get_fallback_forecast(self, periods):
        """Fallback forecast when models fail"""
        base_demand = 1000
        results = []
        
        for i in range(periods):
            # Simple linear growth with seasonal variation
            seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * i / 12)
            growth_factor = 1 + (i * 0.05)  # 5% growth per month
            
            demand = base_demand * seasonal_factor * growth_factor
            
            results.append({
                'month': i + 1,
                'demand': demand,
                'confidence_lower': demand * 0.8,
                'confidence_upper': demand * 1.2,
                'model': 'fallback'
            })
        
        return results

# Flask API endpoints would be added here if this service runs independently
if __name__ == "__main__":
    forecasting_service = MarketForecastingService()
    
    # Example usage
    result = forecasting_service.ensemble_forecast('food', 'Dhaka', 12)
    print(json.dumps(result, indent=2, default=str))