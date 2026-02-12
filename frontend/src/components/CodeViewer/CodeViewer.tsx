import { useState, useEffect, useRef } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { usePreviewStore } from '../../store/usePreviewStore';
import { useGraphStore } from '../../store/useGraphStore';
import { useUIStore } from '../../store/useUIStore';

export default function CodeViewer() {
  const { generatedCode, isRendering } = usePreviewStore();
  const { graph } = useGraphStore();
  const scrollToNodeId = useUIStore((state) => state.scrollToNodeId);
  const setScrollToNodeId = useUIStore((state) => state.setScrollToNodeId);
  const [copySuccess, setCopySuccess] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!scrollToNodeId || !generatedCode || !scrollRef.current) return;

    // Find the line with this node ID
    const lines = generatedCode.split('\n');
    const lineIndex = lines.findIndex((line) => line.includes(`ID: ${scrollToNodeId}`));
    if (lineIndex === -1) {
      setScrollToNodeId(null);
      return;
    }

    // Scroll to the line — each line is roughly 21px tall
    requestAnimationFrame(() => {
      if (!scrollRef.current) return;
      const lineHeight = 21;
      scrollRef.current.scrollTop = Math.max(0, lineIndex * lineHeight - 100);
      setScrollToNodeId(null);
    });
  }, [scrollToNodeId, generatedCode, setScrollToNodeId]);

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
    <div className="h-full w-full flex flex-col bg-gray-900 overflow-hidden max-w-full">
      <div className="p-4 border-b border-gray-700 flex items-center justify-between flex-shrink-0">
        <h3 className="text-lg font-semibold text-white">
          Generated MANIM Code
        </h3>
        <div className="flex gap-2 flex-shrink-0 ml-2">
          <button
            onClick={handleCopy}
            disabled={!generatedCode}
            className="px-3 py-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded text-sm transition-colors whitespace-nowrap"
          >
            {copySuccess ? 'Copied!' : 'Copy'}
          </button>
          <button
            onClick={handleDownload}
            disabled={!generatedCode}
            className="px-3 py-1 bg-green-600 hover:bg-green-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded text-sm transition-colors whitespace-nowrap"
          >
            Download
          </button>
        </div>
      </div>
      <div ref={scrollRef} className="flex-1 overflow-auto min-h-0 min-w-0 max-w-full">
        {isRendering ? (
          <div className="flex items-center justify-center h-full text-gray-400">
            Generating code...
          </div>
        ) : generatedCode ? (
          <SyntaxHighlighter
            language="python"
            style={vscDarkPlus}
            showLineNumbers={true}
            lineNumberStyle={{ userSelect: 'none' }}
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
