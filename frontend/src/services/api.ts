import axios from 'axios';
import type { AgentResponse } from '../types';

const api = axios.create({
  baseURL: '', // same-origin; Vite proxy forwards /api and /static
  timeout: 60000,
});

export async function queryAgent(input: string): Promise<AgentResponse> {
  const { data } = await api.post<AgentResponse>('/api/agent/query', { input });
  return data;
}