import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import UserInputForm from './components/UserInputForm';
import AnalysisResults from './components/AnalysisResults';
import { AnalysisResult } from './types/types';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalysisComplete = (result: AnalysisResult) => {
    setAnalysisResult(result);
    setLoading(false);
    setError(null);
  };

  const handleAnalysisStart = () => {
    setLoading(true);
    setError(null);
    setAnalysisResult(null);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setLoading(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              📊 Business Analysis Platform
            </Typography>
          </Toolbar>
        </AppBar>
        
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          <Routes>
            <Route path="/" element={
              <>
                <UserInputForm
                  onAnalysisStart={handleAnalysisStart}
                  onAnalysisComplete={handleAnalysisComplete}
                  onError={handleError}
                />
                
                {loading && (
                  <div className="loading">
                    <Typography>Analyzing market data...</Typography>
                  </div>
                )}
                
                {error && (
                  <div className="error">
                    <Typography color="error">{error}</Typography>
                  </div>
                )}
                
                {analysisResult && (
                  <AnalysisResults result={analysisResult} />
                )}
              </>
            } />
          </Routes>
        </Container>
      </Router>
    </ThemeProvider>
  );
}

export default App;