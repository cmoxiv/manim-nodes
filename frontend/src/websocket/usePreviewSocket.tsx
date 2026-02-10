import { useEffect, useRef, useState } from 'react';
import ReconnectingWebSocket from 'reconnecting-websocket';
import { usePreviewStore } from '../store/usePreviewStore';
import { Graph } from '../types/graph';

export function usePreviewWebSocket() {
  const ws = useRef<ReconnectingWebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const { setRendering, setVideoUrl, setError, addLog, clearLog, reset, setGeneratedCode } = usePreviewStore();

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

          case 'progress':
            addLog(message.message);
            break;

          case 'complete':
            setRendering(false);
            setVideoUrl(message.video_url);
            setGeneratedCode(message.code || null);
            addLog('Render complete!');
            break;

          case 'error':
            setRendering(false);
            setError(message.message);
            if (message.code) setGeneratedCode(message.code);
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
  }, [setRendering, setVideoUrl, setError, addLog, setGeneratedCode]);

  const sendRenderRequest = (graph: Graph) => {
    if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
      setError('WebSocket not connected');
      return;
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
