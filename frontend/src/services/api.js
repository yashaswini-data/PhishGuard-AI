import axios from 'axios';

// Base API URL with sensible fallback
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  /**
   * Health check to confirm backend & ML model readiness
   */
  async checkHealth() {
    try {
      const response = await apiClient.get('/health');
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Unable to connect to PhishGuard API service.'
      };
    }
  },

  /**
   * Fetch model metadata, hyperparameter tuning info, and test evaluation metrics
   */
  async getModelInfo() {
    try {
      const response = await apiClient.get('/model-info');
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Failed to retrieve model specifications.'
      };
    }
  },

  /**
   * Submit an untrusted URL for real-time 30-feature risk assessment
   */
  async predictUrl(url) {
    try {
      const response = await apiClient.post('/predict', { url });
      return { success: true, data: response.data };
    } catch (error) {
      let errorMessage = 'Failed to analyze URL.';
      if (error.response?.data?.detail) {
        errorMessage = typeof error.response.data.detail === 'string'
          ? error.response.data.detail
          : JSON.stringify(error.response.data.detail);
      } else if (error.code === 'ECONNABORTED') {
        errorMessage = 'Analysis timed out. Please verify server connectivity.';
      } else if (!error.response) {
        errorMessage = 'Backend service is offline. Please ensure FastAPI server is running on port 8000.';
      }
      return { success: false, error: errorMessage };
    }
  }
};

export default api;
