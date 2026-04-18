import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
});

export async function predictLoan(formData) {
  const response = await apiClient.post('/api/v1/predict', formData);
  return response.data;
}

export async function getHealth() {
  const response = await apiClient.get('/health');
  return response.data;
}

export async function getPipelineStatus() {
  const response = await apiClient.get('/api/v1/pipeline/status');
  return response.data;
}

export default apiClient;
