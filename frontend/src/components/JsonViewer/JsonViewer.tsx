import { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useGraphStore } from '../../store/useGraphStore';

export default function JsonViewer() {
  const { graph, nodes, edges } = useGraphStore();
  const [copySuccess, setCopySuccess] = useState(false);

  const graphData = {
    name: graph?.name || 'untitled',
    nodes: nodes.map(n => ({
      id: n.id,
      type: n.data.type,
      position: n.position,
      data: n.data,
    })),
    edges: edges.map(e => ({
      id: e.id,
      source: e.source,
      target: e.target,
      sourceHandle: e.sourceHandle,
      targetHandle: e.targetHandle,
    })),
  };

  const jsonString = JSON.stringify(graphData, null, 2);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(jsonString);
    setCopySuccess(true);
    setTimeout(() => setCopySuccess(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${graphData.name}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="h-full w-full flex flex-col bg-gray-900">
      <div className="p-4 border-b border-gray-700 flex items-center justify-between flex-shrink-0">
        <h3 className="text-lg font-semibold text-white">Graph JSON</h3>
        <div className="flex gap-2">
          <button
            onClick={handleCopy}
            className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm transition-colors"
          >
            {copySuccess ? 'Copied!' : 'Copy'}
          </button>
          <button
            onClick={handleDownload}
            className="px-3 py-1 bg-green-600 hover:bg-green-700 text-white rounded text-sm transition-colors"
          >
            Download
          </button>
        </div>
      </div>
      <div className="flex-1 overflow-auto min-h-0">
        <SyntaxHighlighter
          language="json"
          style={vscDarkPlus}
          showLineNumbers={true}
          customStyle={{
            margin: 0,
            padding: '1rem',
            background: 'transparent',
            fontSize: '0.875rem',
          }}
        >
          {jsonString}
        </SyntaxHighlighter>
      </div>
    </div>
  );
}
