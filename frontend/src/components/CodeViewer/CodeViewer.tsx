import { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { usePreviewStore } from '../../store/usePreviewStore';
import { useGraphStore } from '../../store/useGraphStore';

export default function CodeViewer() {
  const { generatedCode, isRendering } = usePreviewStore();
  const { graph } = useGraphStore();
  const [copySuccess, setCopySuccess] = useState(false);

  const handleCopy = async () => {
    if (!generatedCode) return;

    await navigator.clipboard.writeText(generatedCode);
    setCopySuccess(true);
    setTimeout(() => setCopySuccess(false), 2000);
  };

  const handleDownload = () => {
    if (!generatedCode) return;
    const filename = graph?.name
      ? `${graph.name.replace(/[^a-z0-9]/gi, '_')}_manim.py`
      : 'generated_scene.py';

    const blob = new Blob([generatedCode], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="h-full w-full flex flex-col bg-gray-900">
      <div className="p-4 border-b border-gray-700 flex items-center justify-between flex-shrink-0">
        <h3 className="text-lg font-semibold text-white">
          Generated MANIM Code
        </h3>
        {generatedCode && (
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
        )}
      </div>
      <div className="flex-1 overflow-auto min-h-0">
        {isRendering ? (
          <div className="flex items-center justify-center h-full text-gray-400">
            Generating code...
          </div>
        ) : generatedCode ? (
          <SyntaxHighlighter
            language="python"
            style={vscDarkPlus}
            showLineNumbers={true}
            customStyle={{
              margin: 0,
              padding: '1rem',
              background: 'transparent',
              fontSize: '0.875rem',
            }}
          >
            {generatedCode}
          </SyntaxHighlighter>
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            No code generated yet. Click "Render Preview" to generate code.
          </div>
        )}
      </div>
    </div>
  );
}
