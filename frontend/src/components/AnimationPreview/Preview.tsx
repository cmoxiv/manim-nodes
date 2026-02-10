import { useRef, useEffect } from 'react';
import { Play, Pause, RotateCcw, Download } from 'lucide-react';
import { usePreviewStore } from '../../store/usePreviewStore';
import { useGraphStore } from '../../store/useGraphStore';
import { usePreviewWebSocket } from '../../websocket/usePreviewSocket';

export default function AnimationPreview() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const {
    isRendering,
    videoUrl,
    error,
    isPlaying,
    setPlaying,
    setCurrentTime,
    setDuration,
  } = usePreviewStore();
  const graph = useGraphStore((state) => state.graph);
  const { sendRenderRequest, connected } = usePreviewWebSocket();

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleTimeUpdate = () => setCurrentTime(video.currentTime);
    const handleLoadedMetadata = () => setDuration(video.duration);
    const handleEnded = () => setPlaying(false);

    video.addEventListener('timeupdate', handleTimeUpdate);
    video.addEventListener('loadedmetadata', handleLoadedMetadata);
    video.addEventListener('ended', handleEnded);

    return () => {
      video.removeEventListener('timeupdate', handleTimeUpdate);
      video.removeEventListener('loadedmetadata', handleLoadedMetadata);
      video.removeEventListener('ended', handleEnded);
    };
  }, [setCurrentTime, setDuration, setPlaying]);

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

    // Sync current nodes/edges to the graph before rendering
    const { nodes, edges } = useGraphStore.getState();

    const graphNodes = nodes.map((node) => ({
      id: node.id,
      type: node.data.type,
      position: node.position,
      data: { ...node.data },
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

      {videoUrl && !isRendering && (
        <div className="p-4 border-t border-gray-700 flex items-center gap-4">
          <button
            onClick={handlePlayPause}
            className="p-2 bg-gray-700 hover:bg-gray-600 rounded transition-colors"
          >
            {isPlaying ? <Pause size={20} className="text-white" /> : <Play size={20} className="text-white" />}
          </button>

          <button
            onClick={handleRestart}
            className="p-2 bg-gray-700 hover:bg-gray-600 rounded transition-colors"
          >
            <RotateCcw size={20} className="text-white" />
          </button>

          <div className="flex-1"></div>

          <a
            href={videoUrl}
            download
            className="p-2 bg-gray-700 hover:bg-gray-600 rounded transition-colors"
          >
            <Download size={20} className="text-white" />
          </a>
        </div>
      )}
    </div>
  );
}
