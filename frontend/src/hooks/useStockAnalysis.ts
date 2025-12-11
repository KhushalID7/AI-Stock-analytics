import { useState, useCallback } from 'react';
import axios from 'axios';
import type { AgentResponse } from '../types';
import { queryAgent as apiQueryAgent } from '../services/api';

const useStockAnalysis = () => {
  const [data, setData] = useState<AgentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const queryAgent = useCallback(async (input: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiQueryAgent(input);

      const fallbackSummary =
        (typeof res.raw_result === 'string' && res.raw_result) ||
        res.raw_result?.output ||
        res.raw_result?.message ||
        res.raw_result?.detail ||
        '';

      const mapped: AgentResponse = {
        summary: (res.summary || fallbackSummary || '').toString(),
        chart_urls: res.chart_urls ?? [],
        raw_result: res.raw_result ?? res,
      };

      setData(mapped);
      return mapped;
    } catch (err) {
      let message = 'Network Error';
      if (axios.isAxiosError(err)) {
        const resp = err.response;
        if (resp?.data) {
          message =
            resp.data.detail ||
            resp.data.error ||
            resp.data.message ||
            JSON.stringify(resp.data);
        } else if (err.message) {
          message = err.message;
        }
      }
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { data, loading, error, queryAgent };
};

export default useStockAnalysis;