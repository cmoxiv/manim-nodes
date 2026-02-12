import { useRef, useEffect } from 'react';
import { X, Terminal, Bug } from 'lucide-react';
import { usePreviewStore } from '../../store/usePreviewStore';
import { useUIStore } from '../../store/useUIStore';

type Tab = 'log' | 'debug';

export default function DebugPanel() {
  const { log, debugLog, error } = usePreviewStore();
  const toggleDebugPanel = useUIStore((s) => s.toggleDebugPanel);
  const logEndRef = useRef<HTMLDivElement>(null);
  const activeTab: Tab = debugLog.length > 0 ? 'debug' : 'log';

  // Auto-scroll to bottom when new log entries arrive
  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [log, debugLog]);

  const entries = activeTab === 'debug' ? debugLog : log;

  return (
    <div className="bg-gray-900 border-t border-gray-700 flex flex-col" style={{ height: '200px' }}>
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-1.5 bg-gray-800 border-b border-gray-700 flex-shrink-0">
        <div className="flex items-center gap-3">
          <span className="text-sm font-medium text-gray-300 flex items-center gap-1.5">
            <Terminal size={14} />
            Render Log
          </span>
          {debugLog.length > 0 && (
            <span className="text-xs px-1.5 py-0.5 rounded bg-purple-600/30 text-purple-300 flex items-center gap-1">
              <Bug size={12} />
              {debugLog.length} debug
            </span>
          )}
          {error && (
            <span className="text-xs px-1.5 py-0.5 rounded bg-red-600/30 text-red-300">
              Error
            </span>
          )}
        </div>
        <button
          onClick={toggleDebugPanel}
          className="text-gray-400 hover:text-white p-0.5"
          title="Close debug panel"
        >
          <X size={14} />
        </button>
      </div>

      {/* Log content */}
      <div className="flex-1 overflow-y-auto font-mono text-xs p-2 space-y-0.5 min-h-0">
        {entries.length === 0 ? (
          <div className="text-gray-500 text-center py-4">
            No output yet. Render a graph to see logs.
          </div>
        ) : (
          entries.map((entry, i) => (
            <div
              key={i}
              className={`px-1 py-0.5 rounded ${
                entry.startsWith('Error')
                  ? 'text-red-400 bg-red-900/20'
                  : entry.startsWith('Render complete')
                    ? 'text-green-400'
                    : activeTab === 'debug'
                      ? 'text-purple-300'
                      : 'text-gray-400'
              }`}
            >
              <span className="text-gray-600 mr-2 select-none">{String(i + 1).padStart(3)}</span>
              {entry}
            </div>
          ))
        )}
        <div ref={logEndRef} />
      </div>
    </div>
  );
}
