import { useState } from 'react';
import { usePreviewStore } from '../../store/usePreviewStore';

export default function ErrorPanel() {
  const { error } = usePreviewStore();
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (!error) return;
    navigator.clipboard.writeText(error).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="h-full w-full flex flex-col bg-gray-900">
      <div className="p-4 border-b border-gray-700 flex-shrink-0">
        <h3 className="text-lg font-semibold text-white">Errors</h3>
      </div>
      <div className="flex-1 overflow-auto min-h-0">
        {error ? (
          <div className="p-4 h-full overflow-auto">
            <div className="bg-red-900/20 border-2 border-red-500 rounded-lg p-6">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0">
                  <svg className="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-semibold text-red-400">Render Error</h3>
                    <button
                      onClick={handleCopy}
                      className="px-2 py-1 text-xs rounded border border-gray-600 text-gray-400 hover:text-white hover:border-gray-400 transition-colors"
                    >
                      {copied ? 'Copied!' : 'Copy'}
                    </button>
                  </div>
                  <div className="text-gray-300 font-mono text-sm whitespace-pre-wrap bg-gray-900/50 p-4 rounded border border-red-700/50">
                    {error}
                  </div>
                  <div className="mt-4 text-sm text-gray-400">
                    <p className="font-semibold mb-2">Common fixes:</p>
                    <ul className="list-disc list-inside space-y-1">
                      <li>Ensure all shapes are connected to a Scene node</li>
                      <li>Verify all required inputs are connected</li>
                      <li>Check that node types are compatible</li>
                      <li>Make sure your graph has at least one Scene node</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            No errors
          </div>
        )}
      </div>
    </div>
  );
}
