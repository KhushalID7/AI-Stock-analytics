import React, { useState } from 'react';

interface AnalysisResultsProps {
    summary: string;
    chartUrls: string[];
    rawResult?: any;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ summary, chartUrls, rawResult }) => {
    const [showRaw, setShowRaw] = useState(false);

    return (
        <div className="max-w-5xl mx-auto space-y-6">
            {/* Summary Section */}
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
                <h2 className="text-2xl font-bold mb-4 text-blue-400">Analysis Summary</h2>
                <div className="prose prose-invert max-w-none">
                    <p className="text-gray-200 whitespace-pre-wrap">{summary}</p>
                </div>
            </div>

            {/* Charts Section */}
            {chartUrls && chartUrls.length > 0 && (
                <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
                    <h2 className="text-2xl font-bold mb-4 text-blue-400">Charts</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {chartUrls.map((url, idx) => (
                            <div key={idx} className="bg-gray-700 rounded-lg p-4">
                                <img 
                                    src={url} 
                                    alt={`Chart ${idx + 1}`}
                                    className="w-full h-auto rounded"
                                />
                                <a 
                                    href={url} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="text-blue-400 hover:text-blue-300 text-sm mt-2 inline-block"
                                >
                                    Open in new tab →
                                </a>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Raw Data Section (Optional) */}
            {rawResult && (
                <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
                    <button
                        onClick={() => setShowRaw(!showRaw)}
                        className="text-xl font-bold mb-4 text-blue-400 hover:text-blue-300 flex items-center gap-2"
                    >
                        <span>{showRaw ? '▼' : '▶'}</span>
                        Raw Output
                    </button>
                    {showRaw && (
                        <pre className="bg-gray-900 p-4 rounded overflow-auto text-sm text-gray-300">
                            {JSON.stringify(rawResult, null, 2)}
                        </pre>
                    )}
                </div>
            )}
        </div>
    );
};

export default AnalysisResults;