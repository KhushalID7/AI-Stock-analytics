import React, { useState } from 'react';

interface StockInputProps {
  onSubmit: (query: string) => void;
  loading?: boolean;
}

const StockInput: React.FC<StockInputProps> = ({ onSubmit, loading = false }) => {
  const [query, setQuery] = useState('');

  const presetQueries = [
    'Show me AAPL stock prices for the last 3 months',
    'Calculate moving averages for MSFT',
    'Generate a chart for TSLA stock with Bollinger Bands'
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query.trim());
    }
  };

  const handlePreset = (preset: string) => {
    setQuery(preset);
  };

  return (
    <div className="w-full max-w-3xl mx-auto mb-6">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about stock analysis (e.g., 'Show me AAPL prices and moving averages for last 6 months')"
          className="w-full border border-gray-600 bg-gray-800 text-white rounded-lg p-4 min-h-[120px] focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
          required
        />
        
        <div className="flex flex-wrap gap-2">
          {presetQueries.map((preset, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handlePreset(preset)}
              className="text-sm px-3 py-1 bg-gray-700 hover:bg-gray-600 text-gray-300 rounded-md transition-colors"
              disabled={loading}
            >
              {preset}
            </button>
          ))}
        </div>

        <button 
          type="submit" 
          className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg p-3 font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          disabled={loading}
        >
          {loading ? 'Analyzing...' : 'Analyze Stock'}
        </button>
      </form>
    </div>
  );
};

export default StockInput;