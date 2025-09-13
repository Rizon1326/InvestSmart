import React, { useState } from 'react';
import {
  Paper,
  TextField,
  Button,
  Grid,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Stepper,
  Step,
  StepLabel
} from '@mui/material';
import { UserInput, AnalysisResult } from '../types/types';
import { apiService } from '../services/apiService';

const districts = [
  'Dhaka', 'Chittagong', 'Sylhet', 'Rajshahi', 'Khulna', 'Barishal', 'Rangpur', 'Mymensingh'
];

const businessInterests = [
  'Food & Restaurant', 'Retail & Fashion', 'Electronics', 'Beauty & Personal Care', 
  'Agriculture', 'E-commerce', 'Services', 'Healthcare'
];

const steps = ['Basic Info', 'Financial Details', 'Preferences'];

interface Props {
  onAnalysisStart: () => void;
  onAnalysisComplete: (result: AnalysisResult) => void;
  onError: (error: string) => void;
}

const UserInputForm: React.FC<Props> = ({ onAnalysisStart, onAnalysisComplete, onError }) => {
  const [activeStep, setActiveStep] = useState(0);
  const [formData, setFormData] = useState<UserInput>({
    location: '',
    businessInterest: '',
    capitalMin: 0,
    capitalMax: 0,
    riskProfile: '',
    targetIncome: 0,
    incomePeriod: 'monthly',
    workType: '',
    sellingChannel: '',
    seasonalPreference: '',
    deliveryCapability: ''
  });

  const handleInputChange = (field: keyof UserInput) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> | any
  ) => {
    const value = event.target.value;
    setFormData(prev => ({
      ...prev,
      [field]: field.includes('capital') || field === 'targetIncome' ? Number(value) : value
    }));
  };

  const handleNext = () => {
    setActiveStep(prev => prev + 1);
  };

  const handleBack = () => {
    setActiveStep(prev => prev - 1);
  };

  const handleSubmit = async () => {
    try {
      onAnalysisStart();
      const result = await apiService.analyzeMarket(formData);
      onAnalysisComplete(result);
    } catch (error) {
      onError('Failed to analyze market data. Please try again.');
    }
  };

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Location (District)</InputLabel>
                <Select
                  value={formData.location}
                  onChange={handleInputChange('location')}
                  label="Location (District)"
                >
                  {districts.map(district => (
                    <MenuItem key={district} value={district}>{district}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Business Interest</InputLabel>
                <Select
                  value={formData.businessInterest}
                  onChange={handleInputChange('businessInterest')}
                  label="Business Interest"
                >
                  {businessInterests.map(business => (
                    <MenuItem key={business} value={business}>{business}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Work Type</InputLabel>
                <Select
                  value={formData.workType}
                  onChange={handleInputChange('workType')}
                  label="Work Type"
                >
                  <MenuItem value="full-time">Full-time</MenuItem>
                  <MenuItem value="part-time">Part-time</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Selling Channel</InputLabel>
                <Select
                  value={formData.sellingChannel}
                  onChange={handleInputChange('sellingChannel')}
                  label="Selling Channel"
                >
                  <MenuItem value="online">Online</MenuItem>
                  <MenuItem value="offline">Offline</MenuItem>
                  <MenuItem value="both">Both</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        );
      
      case 1:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Minimum Capital (BDT)"
                type="number"
                value={formData.capitalMin}
                onChange={handleInputChange('capitalMin')}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Maximum Capital (BDT)"
                type="number"
                value={formData.capitalMax}
                onChange={handleInputChange('capitalMax')}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Target Income (BDT)"
                type="number"
                value={formData.targetIncome}
                onChange={handleInputChange('targetIncome')}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Income Period</InputLabel>
                <Select
                  value={formData.incomePeriod}
                  onChange={handleInputChange('incomePeriod')}
                  label="Income Period"
                >
                  <MenuItem value="monthly">Monthly</MenuItem>
                  <MenuItem value="yearly">Yearly</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Risk Profile</InputLabel>
                <Select
                  value={formData.riskProfile}
                  onChange={handleInputChange('riskProfile')}
                  label="Risk Profile"
                >
                  <MenuItem value="conservative">Conservative (Low Risk)</MenuItem>
                  <MenuItem value="balanced">Balanced (Moderate Risk)</MenuItem>
                  <MenuItem value="aggressive">Aggressive (High Risk)</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        );
      
      case 2:
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Delivery Capability</InputLabel>
                <Select
                  value={formData.deliveryCapability}
                  onChange={handleInputChange('deliveryCapability')}
                  label="Delivery Capability"
                >
                  <MenuItem value="own">Own Delivery</MenuItem>
                  <MenuItem value="third-party">Third-party Delivery</MenuItem>
                  <MenuItem value="both">Both</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Seasonal Preference (Optional)"
                value={formData.seasonalPreference}
                onChange={handleInputChange('seasonalPreference')}
                placeholder="e.g., Ramadan, Eid, Winter"
              />
            </Grid>
          </Grid>
        );
      
      default:
        return 'Unknown step';
    }
  };

  const isStepValid = (step: number) => {
    switch (step) {
      case 0:
        return formData.location && formData.businessInterest && formData.workType && formData.sellingChannel;
      case 1:
        return formData.capitalMin > 0 && formData.capitalMax > 0 && formData.targetIncome > 0 && formData.riskProfile;
      case 2:
        return formData.deliveryCapability;
      default:
        return false;
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Business Analysis Input Form
      </Typography>
      
      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      <Box sx={{ mb: 4 }}>
        {renderStepContent(activeStep)}
      </Box>

      <Box sx={{ display: 'flex', flexDirection: 'row', pt: 2 }}>
        <Button
          color="inherit"
          disabled={activeStep === 0}
          onClick={handleBack}
          sx={{ mr: 1 }}
        >
          Back
        </Button>
        <Box sx={{ flex: '1 1 auto' }} />
        {activeStep === steps.length - 1 ? (
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={!isStepValid(activeStep)}
            size="large"
          >
            Analyze Market
          </Button>
        ) : (
          <Button
            variant="contained"
            onClick={handleNext}
            disabled={!isStepValid(activeStep)}
          >
            Next
          </Button>
        )}
      </Box>
    </Paper>
  );
};

export default UserInputForm;