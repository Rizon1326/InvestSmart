import React from 'react';
import {
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Box,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import {
  TrendingUp,
  AccountBalance,
  ShowChart,
  Timeline,
  Lightbulb,
  Warning,
  CheckCircle
} from '@mui/icons-material';
import { AnalysisResult, ForecastData, RecommendationData } from '../types/types';
import DemandForecastChart from './charts/DemandForecastChart';
import ROIChart from './charts/ROIChart';
import BreakEvenChart from './charts/BreakEvenChart';

interface Props {
  result: AnalysisResult;
}

const AnalysisResults: React.FC<Props> = ({ result }) => {
  // Parse JSON strings
  const forecastData: { forecast: ForecastData[] } = JSON.parse(result.demandForecast || '{"forecast": []}');
  const recommendations: RecommendationData = JSON.parse(result.recommendations || '{"top_recommendations": [], "risk_mitigation": [], "growth_opportunities": []}');
  const aiAnalysis = JSON.parse(result.aiAnalysis || '{}');

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-BD', {
      style: 'currency',
      currency: 'BDT',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const formatPercentage = (value: number) => {
    return `${value.toFixed(1)}%`;
  };

  const getFitScoreColor = (score: number) => {
    if (score >= 8) return 'success';
    if (score >= 6) return 'warning';
    return 'error';
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h4" component="h2" gutterBottom align="center">
        📊 Market Analysis Results
      </Typography>

      {/* KPI Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <ShowChart color="primary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h6" color="text.secondary">
                Fit Score
              </Typography>
              <Typography variant="h4" component="div">
                {result.fitScore.toFixed(1)}/10
              </Typography>
              <Chip 
                label={result.fitScore >= 7 ? 'Good Fit' : result.fitScore >= 5 ? 'Moderate' : 'Poor Fit'} 
                color={getFitScoreColor(result.fitScore)}
                size="small"
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <AccountBalance color="primary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h6" color="text.secondary">
                Expected Revenue
              </Typography>
              <Typography variant="h4" component="div">
                {formatCurrency(result.expectedRevenue)}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                per month
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <TrendingUp color="primary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h6" color="text.secondary">
                ROI
              </Typography>
              <Typography variant="h4" component="div">
                {formatPercentage(result.roiPercentage)}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                annual return
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <Timeline color="primary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h6" color="text.secondary">
                Payback Period
              </Typography>
              <Typography variant="h4" component="div">
                {result.paybackPeriodMonths}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                months
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts Section */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              📈 Demand Forecast (12 Months)
            </Typography>
            <DemandForecastChart data={forecastData.forecast} />
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              💰 ROI Analysis
            </Typography>
            <ROIChart 
              expectedRevenue={result.expectedRevenue}
              netProfit={result.netProfit}
              roiPercentage={result.roiPercentage}
            />
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              ⚖️ Break-Even Analysis
            </Typography>
            <BreakEvenChart
              suggestedPrice={result.suggestedPrice}
              expectedRevenue={result.expectedRevenue}
              netProfit={result.netProfit}
            />
          </Paper>
        </Grid>
      </Grid>

      {/* Recommendations Section */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              <Lightbulb sx={{ mr: 1, verticalAlign: 'middle' }} />
              Top Recommendations
            </Typography>
            <List>
              {recommendations.top_recommendations.map((rec, index) => (
                <ListItem key={index} sx={{ px: 0 }}>
                  <ListItemIcon>
                    <CheckCircle color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {rec.title}
                        <Chip 
                          label={rec.priority} 
                          color={getPriorityColor(rec.priority)}
                          size="small"
                        />
                      </Box>
                    }
                    secondary={rec.description}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              <Warning sx={{ mr: 1, verticalAlign: 'middle' }} />
              Risk Mitigation
            </Typography>
            <List>
              {recommendations.risk_mitigation.map((item, index) => (
                <ListItem key={index} sx={{ px: 0 }}>
                  <ListItemIcon>
                    <Warning color="warning" />
                  </ListItemIcon>
                  <ListItemText primary={item} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              <TrendingUp sx={{ mr: 1, verticalAlign: 'middle' }} />
              Growth Opportunities
            </Typography>
            <List>
              {recommendations.growth_opportunities.map((item, index) => (
                <ListItem key={index} sx={{ px: 0 }}>
                  <ListItemIcon>
                    <TrendingUp color="success" />
                  </ListItemIcon>
                  <ListItemText primary={item} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* AI Analysis Summary */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          🤖 AI Analysis Summary
        </Typography>
        <Typography variant="body1" paragraph>
          {typeof aiAnalysis === 'string' ? aiAnalysis : aiAnalysis.analysis || 'AI analysis completed successfully.'}
        </Typography>
        
        {aiAnalysis.market_opportunity && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" color="primary">
              Market Opportunity:
            </Typography>
            <Typography variant="body2">
              {aiAnalysis.market_opportunity}
            </Typography>
          </Box>
        )}

        {aiAnalysis.pricing_strategy && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" color="primary">
              Pricing Strategy:
            </Typography>
            <Typography variant="body2">
              {aiAnalysis.pricing_strategy}
            </Typography>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default AnalysisResults;