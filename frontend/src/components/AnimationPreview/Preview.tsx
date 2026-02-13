import { useRef, useEffect } from 'react';
import { Play, Pause, RotateCcw, Download, X, FolderOpen } from 'lucide-react';
import { usePreviewStore } from '../../store/usePreviewStore';
import { useGraphStore } from '../../store/useGraphStore';
import { usePreviewWebSocket } from '../../websocket/usePreviewSocket';


export default function AnimationPreview() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const {
    isRendering,
    videoUrl,
    error,
    debugLog,
    isPlaying,
    setPlaying,
  } = usePreviewStore();
  const graph = useGraphStore((state) => state.graph);
  const { sendRenderRequest, connected } = usePreviewWebSocket();

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleEnded = () => setPlaying(false);
    video.addEventListener('ended', handleEnded);
    return () => video.removeEventListener('ended', handleEnded);
  }, [setPlaying]);

  const handlePlayPause = () => {
    if (!videoRef.current) return;
    if (isPlaying) {
      videoRef.current.pause();
      setPlaying(false);
    } else {
      videoRef.current.play();
      setPlaying(true);
    }
  };

  const handleRestart = () => {
    if (!videoRef.current) return;
    videoRef.current.currentTime = 0;
    videoRef.current.play();
    setPlaying(true);
  };

  const handleRender = () => {
    if (!graph || !connected) return;

    const { nodes, edges } = useGraphStore.getState();

    const graphNodes = nodes.map((node) => ({
      id: node.id,
      type: node.type === 'groupFrame' ? '__groupFrame' : node.data.type,
      position: node.position,
      data: { ...node.data },
      ...(node.parentNode && { parentNode: node.parentNode }),
      ...(node.style && { style: node.style }),
      ...(node.zIndex !== undefined && { zIndex: node.zIndex }),
    }));

    const graphEdges = edges.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      sourceHandle: edge.sourceHandle,
      targetHandle: edge.targetHandle,
    }));

    const updatedGraph = {
      ...graph,
      nodes: graphNodes,
      edges: graphEdges,
    };

    sendRenderRequest(updatedGraph);
  };

  return (
    <div className="h-full flex flex-col bg-gray-900">
      <div className="p-4 border-b border-gray-700 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-white">Preview</h2>
        <button
          onClick={handleRender}
          disabled={isRendering || !connected}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white text-sm rounded transition-colors"
        >
          {isRendering ? 'Rendering...' : 'Render Preview'}
        </button>
      </div>

      {debugLog.length > 0 && (
        <div className="border-b border-gray-700 bg-gray-950 max-h-32 overflow-y-auto">
          <div className="flex items-center justify-between px-3 py-1 border-b border-gray-800">
            <span className="text-xs font-semibold text-yellow-400">Debug Output</span>
            <button
              onClick={() => usePreviewStore.getState().clearLog()}
              className="p-0.5 hover:bg-gray-800 rounded"
            >
              <X size={12} className="text-gray-500" />
            </button>
          </div>
          <div className="px-3 py-1 space-y-0.5">
            {debugLog.map((msg, i) => (
              <div key={i} className="text-xs font-mono text-yellow-300">{msg}</div>
            ))}
          </div>
        </div>
      )}

      {/* Controls bar - above the video */}
      {videoUrl && !isRendering && (
        <div className="px-3 py-2 border-b border-gray-700 flex items-center gap-2">
          <button
            onClick={handlePlayPause}
            className="p-1.5 bg-gray-700 hover:bg-gray-600 rounded transition-colors"
            title={isPlaying ? 'Pause' : 'Play'}
          >
            {isPlaying ? <Pause size={16} className="text-white" /> : <Play size={16} className="text-white" />}
          </button>
          <button
            onClick={handleRestart}
            className="p-1.5 bg-gray-700 hover:bg-gray-600 rounded transition-colors"
            title="Restart"
          >
            <RotateCcw size={16} className="text-white" />
          </button>
          <div className="flex-1" />
          <a
            href={videoUrl}
            download
            className="p-1.5 bg-gray-700 hover:bg-gray-600 rounded transition-colors"
            title="Download video"
          >
            <Download size={16} className="text-white" />
          </a>
          <button
            onClick={async () => {
              const res = await fetch('/api/open-folder/previews', { method: 'POST' });
              const data = await res.json();
              if (data.path && !data.native) {
                try {
                  await fetch('http://127.0.0.1:8001', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path: data.path }),
                  });
                } catch {
                  await navigator.clipboard.writeText(data.path);
                  alert(`Could not open folder (is folder-opener running?).\nPath copied to clipboard:\n${data.path}`);
                }
              }
            }}
            className="p-1.5 bg-gray-700 hover:bg-gray-600 rounded transition-colors"
            title="Open previews folder"
          >
            <FolderOpen size={16} className="text-white" />
          </button>
        </div>
      )}

      <div className="flex-1 flex items-center justify-center bg-black">
        {isRendering && (
          <div className="text-white text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
            <p>Rendering animation...</p>
          </div>
        )}

        {error && (
          <div className="text-red-400 text-center p-4">
            <p className="font-semibold mb-2">Render Error</p>
            <p className="text-sm">{error}</p>
          </div>
        )}

        {!isRendering && !error && videoUrl && (
          <video
            ref={videoRef}
            src={videoUrl}
            className="max-w-full max-h-full"
            controls={false}
          />
        )}

        {!isRendering && !error && !videoUrl && (
          <div className="text-gray-500 text-center">
            <p>Click "Render Preview" to see your animation</p>
          </div>
        )}
      </div>
    </div>
  );
}
