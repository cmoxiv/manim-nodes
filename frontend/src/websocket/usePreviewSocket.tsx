import { useEffect, useRef, useState } from 'react';
import ReconnectingWebSocket from 'reconnecting-websocket';
import { usePreviewStore } from '../store/usePreviewStore';
import { useGraphStore } from '../store/useGraphStore';
import { Graph } from '../types/graph';

export function usePreviewWebSocket() {
  const ws = useRef<ReconnectingWebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const { setRendering, setVideoUrl, setError, addLog, addDebugLog, clearLog, reset, setGeneratedCode } = usePreviewStore();
  const updateNodeData = useGraphStore((s) => s.updateNodeData);
  const markErrorEdges = useGraphStore((s) => s.markErrorEdges);
  const clearErrorEdges = useGraphStore((s) => s.clearErrorEdges);

  useEffect(() => {
    // Determine WebSocket URL
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.hostname;
    const port = window.location.port || '8000';
    const wsUrl = `${protocol}//${host}:${port}/ws/preview`;

    // Create WebSocket connection
    ws.current = new ReconnectingWebSocket(wsUrl);

    ws.current.addEventListener('open', () => {
      console.log('WebSocket connected');
      setConnected(true);
    });

    ws.current.addEventListener('close', () => {
      console.log('WebSocket disconnected');
      setConnected(false);
    });

    ws.current.addEventListener('message', (event) => {
      try {
        const message = JSON.parse(event.data);

        switch (message.type) {
          case 'status':
            addLog(message.message);
            break;

          case 'progress': {
            const debugMatch = message.message.match(/^\[DEBUG:([^\]]+)\] (.*)$/);
            if (debugMatch) {
              const [, nodeId, debugMsg] = debugMatch;
              addDebugLog(debugMsg);
              updateNodeData(nodeId, { debugOutput: debugMsg });
            } else if (message.message.startsWith('[DEBUG] ')) {
              addDebugLog(message.message.slice(8));
            } else {
              addLog(message.message);
            }
            break;
          }

          case 'complete':
            setRendering(false);
            setVideoUrl(message.video_url);
            setGeneratedCode(message.code || null);
            addLog('Render complete!');
            break;

          case 'error':
            setRendering(false);
            setError(message.message, message.node_id || null);
            if (message.code) setGeneratedCode(message.code);
            if (message.node_id) {
              updateNodeData(message.node_id, { error: message.message });
              markErrorEdges(message.node_id);
            }
            addLog(`Error: ${message.message}`);
            break;

          case 'pong':
            // Keepalive response
            break;

          default:
            console.warn('Unknown message type:', message.type);
        }
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    });

    ws.current.addEventListener('error', (error) => {
      console.error('WebSocket error:', error);
    });

    // Keepalive ping every 30 seconds
    const pingInterval = setInterval(() => {
      if (ws.current?.readyState === WebSocket.OPEN) {
        ws.current.send(JSON.stringify({ type: 'ping' }));
      }
    }, 30000);

    return () => {
      clearInterval(pingInterval);
      ws.current?.close();
    };
  }, [setRendering, setVideoUrl, setError, addLog, addDebugLog, setGeneratedCode, updateNodeData, markErrorEdges]);

  const sendRenderRequest = (graph: Graph) => {
    if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
      setError('WebSocket not connected');
      return;
    }

    // Clear error highlights and debug output from all nodes and edges
    clearErrorEdges();
    const nodes = useGraphStore.getState().nodes;
    for (const node of nodes) {
      if (node.data.error || node.data.debugOutput) {
        updateNodeData(node.id, { error: undefined, debugOutput: undefined });
      }
    }

    // Reset preview state
    reset();
    clearLog();
    setRendering(true);

    // Send render request
    ws.current.send(
      JSON.stringify({
        type: 'render',
        graph,
      })
    );
  };

  return {
    sendRenderRequest,
    connected,
  };
}
