import { useState, useCallback } from 'react';
import axios from 'axios';
import type { AgentResponse } from '../types';
import { queryAgent as apiQueryAgent } from '../services/api';

function extractChartUrlsFromText(text: string): string[] {
  const pattern = /\/static\/charts\/[^\s"')]+\.png/gi;
  const matches = text.match(pattern) || [];
  return Array.from(new Set(matches)).filter((u) => u.startsWith('/static/'));
}

function pickBestSummary(res: AgentResponse): string {
  const s = (res.summary ?? '').trim();
  const raw =
    typeof res.raw_result === 'string'
      ? res.raw_result
      : res.raw_result?.output ||
        res.raw_result?.final_answer ||
        res.raw_result?.message ||
        res.raw_result?.detail ||
        '';

  const looksGeneric =
    s.length < 120 ||
    /^i('?| a)m (fetching|analyzing)/i.test(s) ||
    /^ok,|^sure/i.test(s);

  return (looksGeneric ? raw : s) || raw || s || '';
}

const useStockAnalysis = () => {
  const [data, setData] = useState<AgentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const queryAgent = useCallback(async (input: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiQueryAgent(input);

      const rawText =
        typeof res.raw_result === 'string' ? res.raw_result : JSON.stringify(res.raw_result ?? res);

      const chartUrls =
        Array.isArray(res.chart_urls) && res.chart_urls.length > 0
          ? res.chart_urls
          : extractChartUrlsFromText(rawText);

      const mapped: AgentResponse = {
        summary: pickBestSummary(res),
        chart_urls: chartUrls,
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