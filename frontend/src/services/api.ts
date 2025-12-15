import axios from 'axios';
import type { AgentResponse } from '../types';

const api = axios.create({
  baseURL: '', // same-origin; Vite proxy forwards /api and /static
  timeout: 120000, // increase timeout for long-running agent chains
});

export async function queryAgent(input: string): Promise<AgentResponse> {
  const { data } = await api.post<AgentResponse>('/api/agent/query', { input });
  return data;
}