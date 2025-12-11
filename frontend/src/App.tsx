import React from 'react';
import StockInput from './components/StockInput';
import AnalysisResults from './components/AnalysisResults';
import useStockAnalysis from './hooks/useStockAnalysis';

const App: React.FC = () => {
  const { data, loading, error, queryAgent } = useStockAnalysis();

  const handleSubmit = async (query: string) => {
    await queryAgent(query);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-gray-100">
      <div className="max-w-5xl mx-auto px-4 py-10 space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold">AI Stock Analytics</h1>
          <p className="text-gray-400">Powered by AI Agent with Real-time Data</p>
        </div>

        <StockInput onSubmit={handleSubmit} loading={loading} />

        {error && (
          <div className="bg-red-900/70 text-red-100 border border-red-700 rounded-lg p-4">
            <strong>Error:</strong> {error}
          </div>
        )}

        {data && (
          <AnalysisResults
            summary={data.summary || 'No summary returned.'}
            chartUrls={data.chart_urls ?? []}
            rawResult={data.raw_result}
          />
        )}
      </div>
    </div>
  );
};

export default App;