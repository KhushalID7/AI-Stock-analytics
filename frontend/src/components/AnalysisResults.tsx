import React, { useMemo, useState } from 'react';

function escapeHtml(s: string) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function toPrettyHtml(text: string): string {
  let html = escapeHtml(text);

  // Linkify chart paths and URLs
  html = html.replace(
    /(^|[\s(])((?:\/)?static\/charts\/[^\s"')]+\.png)/gi,
    (_m, p1, p2) =>
      `${p1}<a class="text-blue-400 underline" target="_blank" rel="noopener" href="${
        p2.startsWith('/') ? p2 : '/' + p2
      }">${p2}</a>`
  );
  html = html.replace(
    /(https?:\/\/[^\s)]+)(?=\)|\s|$)/gi,
    (m) => `<a class="text-blue-400 underline" target="_blank" rel="noopener" href="${m}">${m}</a>`
  );

  // Simple markdown: headings, bold, italics, code fences
  html = html.replace(/^#{1,6}\s?(.*)$/gim, '<span class="block font-semibold text-gray-100 mt-2 mb-1">$1</span>');
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  html = html.replace(/`([^`]+)`/g, '<code class="bg-gray-900 px-1 rounded">$1</code>');
  html = html.replace(/```([\s\S]*?)```/g, '<pre class="bg-gray-900 p-3 rounded overflow-auto">$1</pre>');

  // Lists (bulleted)
  html = html.replace(/^\s*[-*]\s+(.*)$/gim, '<li>$1</li>');
  html = html.replace(/(<li>[\s\S]*?<\/li>)/gim, '<ul class="list-disc ml-5">$1</ul>');

  // Keep line breaks
  html = html.replace(/\n/g, '<br />');

  return html; // IMPORTANT: return the HTML
}

interface AnalysisResultsProps {
  summary: string;
  chartUrls: string[];
  rawResult?: any;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ summary, chartUrls, rawResult }) => {
  const [showRaw, setShowRaw] = useState(false);
  const summaryHtml = useMemo(() => toPrettyHtml(summary || 'No summary returned.'), [summary]);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(summary || '');
    } catch { /* ignore */ }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="bg-[#1f2937] rounded-xl p-6 shadow-lg border border-gray-700">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-2xl font-bold text-blue-300">Analysis Summary</h2>
          <button
            onClick={copyToClipboard}
            className="px-3 py-1.5 text-sm rounded-md bg-gray-700 hover:bg-gray-600 text-gray-200 transition"
            title="Copy summary"
          >
            Copy
          </button>
        </div>
        <div
          className="text-gray-100 leading-relaxed whitespace-pre-wrap prose prose-invert max-w-none"
          dangerouslySetInnerHTML={{ __html: summaryHtml }}
        />
      </div>

      {chartUrls && chartUrls.length > 0 && (
        <div className="bg-[#1f2937] rounded-xl p-6 shadow-lg border border-gray-700">
          <h3 className="text-xl font-semibold mb-4 text-blue-200">Charts</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {chartUrls.map((url, idx) => {
              const fixed = url.startsWith('/static/') ? url : `/static/${url.replace(/^\/?static\//, '')}`;
              return (
                <figure key={idx} className="rounded-lg overflow-hidden bg-gray-900 border border-gray-700">
                  <img src={fixed} alt={`Chart ${idx + 1}`} className="w-full h-auto object-contain" />
                  <figcaption className="px-3 py-2 text-xs text-gray-400 border-t border-gray-800">{fixed}</figcaption>
                </figure>
              );
            })}
          </div>
        </div>
      )}

      {rawResult && (
        <div className="bg-[#1f2937] rounded-xl p-4 shadow-lg border border-gray-700">
          <button
            onClick={() => setShowRaw((s) => !s)}
            className="w-full text-left text-blue-300 hover:text-blue-200 font-medium"
          >
            {showRaw ? '▼ Raw Output' : '▶ Raw Output'}
          </button>
          {showRaw && (
            <pre className="mt-3 bg-gray-900 text-gray-200 p-3 rounded-md overflow-auto max-h-96 text-sm leading-relaxed">
              {typeof rawResult === 'string' ? rawResult : JSON.stringify(rawResult, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  );
};

export default AnalysisResults;