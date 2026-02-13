import { Save, Download, FileText, Upload, FileDown, Layout, Code, Braces, AlertCircle, BookOpen, Terminal, Minimize2, Maximize2, Image, ChevronDown, FolderOpen } from 'lucide-react';
import { toPng, toSvg } from 'html-to-image';
import { getNodesBounds, getViewportForBounds } from 'reactflow';
import { useGraphStore } from '../../store/useGraphStore';
import { useUIStore } from '../../store/useUIStore';
import { usePreviewStore } from '../../store/usePreviewStore';
import { useState, useRef, useEffect } from 'react';
import { apiClient } from '../../api/client';

export default function TopBar() {
  const { graph, isDirty, isSaving, saveGraph, nodes, edges, setNodes, setEdges, renameGraph } = useGraphStore();
  const { mainView, setMainView, showDebugPanel, toggleDebugPanel, viewport, setViewport } = useUIStore();
  const error = usePreviewStore((state) => state.error);
  const generatedCode = usePreviewStore((state) => state.generatedCode);
  const [showExportDialog, setShowExportDialog] = useState(false);
  const [exportQuality, setExportQuality] = useState('1080p');
  const [exportFps, setExportFps] = useState(30);
  const [exportFormat, setExportFormat] = useState<'mp4' | 'gif'>('mp4');
  const [isExporting, setIsExporting] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [showDownloadMenu, setShowDownloadMenu] = useState(false);
  const downloadRef = useRef<HTMLDivElement>(null);
  const [isEditingName, setIsEditingName] = useState(false);
  const [editName, setEditName] = useState('');
  const nameInputRef = useRef<HTMLInputElement>(null);
  const [showExamplesMenu, setShowExamplesMenu] = useState(false);
  const [examplesList, setExamplesList] = useState<Array<{ id: string; name: string; description: string }>>([]);
  const examplesRef = useRef<HTMLDivElement>(null);

  // Close examples menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (examplesRef.current && !examplesRef.current.contains(event.target as Node)) {
        setShowExamplesMenu(false);
      }
    };
    if (showExamplesMenu) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showExamplesMenu]);

  // Close download menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (downloadRef.current && !downloadRef.current.contains(event.target as Node)) {
        setShowDownloadMenu(false);
      }
    };
    if (showDownloadMenu) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showDownloadMenu]);

  const handleShowExamples = async () => {
    if (showExamplesMenu) {
      setShowExamplesMenu(false);
      return;
    }
    try {
      const list = await apiClient.listExamples();
      setExamplesList(list);
      setShowExamplesMenu(true);
    } catch (err) {
      console.error('Failed to load examples:', err);
    }
  };

  const handleLoadExample = async (exampleId: string) => {
    try {
      const example = await apiClient.getExample(exampleId);
      const graphData = example.graph;

      // Fetch node definitions to get inputs/outputs/category (skip frame nodes)
      const uniqueTypes = [...new Set(
        graphData.nodes
          .filter((n: any) => n.type !== '__groupFrame')
          .map((n: any) => n.data.type)
      )] as string[];
      const nodeDefs: Record<string, any> = {};
      await Promise.all(
        uniqueTypes.map(async (t: string) => {
          nodeDefs[t] = await apiClient.getNodeInfo(t);
        })
      );

      const loadedNodes = graphData.nodes.map((n: any) => {
        if (n.type === '__groupFrame') {
          return {
            id: n.id,
            type: 'groupFrame',
            position: n.position,
            data: { ...n.data },
            ...(n.style && { style: n.style }),
            ...(n.zIndex !== undefined && { zIndex: n.zIndex }),
          };
        }
        const def = nodeDefs[n.data.type];
        return {
          id: n.id,
          type: 'custom',
          position: n.position,
          data: {
            ...n.data,
            category: def?.category,
            inputs: def?.inputs,
            outputs: def?.outputs,
          },
          ...(n.parentNode && { parentNode: n.parentNode }),

        };
      });

      const loadedEdges = graphData.edges.map((e: any) => ({
        id: e.id,
        source: e.source,
        target: e.target,
        sourceHandle: e.sourceHandle,
        targetHandle: e.targetHandle,
      }));

      setNodes(loadedNodes);
      setEdges(loadedEdges);
      if (graphData.name) renameGraph(graphData.name);
      setShowExamplesMenu(false);
    } catch (err) {
      console.error('Failed to load example:', err);
      alert('Failed to load example');
    }
  };

  const handleDownloadImage = async (format: 'png' | 'svg') => {
    const viewportEl = document.querySelector('.react-flow__viewport') as HTMLElement;
    if (!viewportEl || nodes.length === 0) return;

    const padding = 50;
    const nodesBounds = getNodesBounds(nodes);
    const imageWidth = nodesBounds.width + padding * 2;
    const imageHeight = nodesBounds.height + padding * 2;
    const viewport = getViewportForBounds(nodesBounds, imageWidth, imageHeight, 0.5, 2, padding);

    const dataFn = format === 'png' ? toPng : toSvg;
    try {
      const dataUrl = await dataFn(viewportEl, {
        backgroundColor: '#030712',
        width: imageWidth,
        height: imageHeight,
        style: {
          width: `${imageWidth}px`,
          height: `${imageHeight}px`,
          transform: `translate(${viewport.x}px, ${viewport.y}px) scale(${viewport.zoom})`,
        },
        filter: (node: HTMLElement) => {
          const classes = node.classList?.toString() || '';
          return !classes.includes('react-flow__minimap') && !classes.includes('react-flow__controls');
        },
      });
      const a = document.createElement('a');
      a.href = dataUrl;
      a.download = `${graph?.name || 'graph'}.${format}`;
      a.click();
    } catch (err) {
      console.error('Image export failed:', err);
    }
  };

  const handleSave = async () => {
    try {
      await saveGraph();
    } catch (error) {
      console.error('Save failed:', error);
      alert('Failed to save graph');
    }
  };

  const handleDownloadJSON = () => {
    const graphData = {
      name: graph?.name || 'untitled',
      nodes: nodes.map(n => ({
        id: n.id,
        type: n.type === 'groupFrame' ? '__groupFrame' : n.data.type,
        position: n.position,
        data: n.data,
        ...(n.parentNode && { parentNode: n.parentNode }),
        ...(n.style && { style: n.style }),
        ...(n.zIndex !== undefined && { zIndex: n.zIndex }),
      })),
      edges: edges.map(e => ({
        id: e.id,
        source: e.source,
        target: e.target,
        sourceHandle: e.sourceHandle,
        targetHandle: e.targetHandle,
      })),
      settings: {
        ...(viewport && { viewport }),
      },
    };

    const blob = new Blob([JSON.stringify(graphData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${graphData.name}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadPython = () => {
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

  const handleLoadJSON = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const graphData = JSON.parse(e.target?.result as string);

        // Convert to React Flow format
        const loadedNodes = graphData.nodes.map((n: any) => ({
          id: n.id,
          type: n.type === '__groupFrame' ? 'groupFrame' : 'custom',
          position: n.position,
          data: n.type === '__groupFrame' ? { ...n.data } : n.data,
          ...(n.parentNode && { parentNode: n.parentNode }),

          ...(n.style && { style: n.style }),
          ...(n.zIndex !== undefined && { zIndex: n.zIndex }),
        }));

        const loadedEdges = graphData.edges.map((e: any) => ({
          id: e.id,
          source: e.source,
          target: e.target,
          sourceHandle: e.sourceHandle,
          targetHandle: e.targetHandle,
        }));

        setNodes(loadedNodes);
        setEdges(loadedEdges);
        setViewport(graphData.settings?.viewport || null);

        alert(`Loaded graph: ${graphData.name}`);
      } catch (error) {
        console.error('Failed to load graph:', error);
        alert('Failed to load graph file');
      }
    };
    reader.readAsText(file);

    // Reset input so same file can be loaded again
    event.target.value = '';
  };

  const handleExport = async () => {
    if (!graph) {
      alert('No graph to export');
      return;
    }

    setIsExporting(true);
    try {
      // Convert graph to export format (same serialization as saveGraph)
      const exportData = {
        id: graph.id,
        name: graph.name,
        nodes: nodes.map(n => ({
          id: n.id,
          type: n.type === 'groupFrame' ? '__groupFrame' : n.data.type,
          position: n.position,
          data: { ...n.data },
          ...(n.parentNode && { parentNode: n.parentNode }),

          ...(n.style && { style: n.style }),
          ...(n.zIndex !== undefined && { zIndex: n.zIndex }),
        })),
        edges: edges.map(e => ({
          id: e.id,
          source: e.source,
          target: e.target,
          sourceHandle: e.sourceHandle,
          targetHandle: e.targetHandle,
        })),
        settings: graph.settings || {},
      };

      // Start export job
      const response = await fetch('/api/export', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          graph: exportData,
          quality: exportQuality,
          fps: exportFps,
          format: exportFormat,
        }),
      });

      if (!response.ok) {
        throw new Error('Export request failed');
      }

      const data = await response.json();
      alert(`Export started! Job ID: ${data.job_id}\nYou can check the export status in the exports directory.`);
      setShowExportDialog(false);
    } catch (error) {
      console.error('Export failed:', error);
      alert('Failed to start export. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="h-14 bg-gray-800 border-b border-gray-700 flex items-center px-4 gap-4">
      <div className="flex items-center gap-2">
        <FileText size={24} className="text-blue-500" />
        <h1 className="text-xl font-bold text-white">Manim Nodes</h1>
      </div>

      <div className="flex-1"></div>

      {/* View Toggle */}
      <div className="flex gap-1 bg-gray-700 rounded p-1">
        <button
          onClick={() => setMainView('canvas')}
          className={`flex items-center gap-2 px-3 py-1 rounded text-sm transition-colors ${
            mainView === 'canvas'
              ? 'bg-blue-600 text-white'
              : 'text-gray-300 hover:text-white'
          }`}
        >
          <Layout size={16} />
          Canvas
        </button>
        <button
          onClick={() => setMainView('code')}
          className={`flex items-center gap-2 px-3 py-1 rounded text-sm transition-colors ${
            mainView === 'code'
              ? 'bg-blue-600 text-white'
              : 'text-gray-300 hover:text-white'
          }`}
        >
          <Code size={16} />
          Code
        </button>
        <button
          onClick={() => setMainView('json')}
          className={`flex items-center gap-2 px-3 py-1 rounded text-sm transition-colors ${
            mainView === 'json'
              ? 'bg-blue-600 text-white'
              : 'text-gray-300 hover:text-white'
          }`}
        >
          <Braces size={16} />
          JSON
        </button>
        <button
          onClick={() => setMainView('error')}
          className={`flex items-center gap-2 px-3 py-1 rounded text-sm transition-colors ${
            mainView === 'error'
              ? 'bg-red-600 text-white'
              : error
                ? 'text-red-400 hover:text-red-300'
                : 'text-gray-300 hover:text-white'
          }`}
        >
          <AlertCircle size={16} />
          Errors
        </button>
        <button
          onClick={toggleDebugPanel}
          className={`flex items-center gap-2 px-3 py-1 rounded text-sm transition-colors ${
            showDebugPanel
              ? 'bg-purple-600 text-white'
              : 'text-gray-300 hover:text-white'
          }`}
        >
          <Terminal size={16} />
          Log
        </button>
      </div>

      <button
        onClick={() => {
          const allCollapsed = nodes.every((n) => n.type === 'groupFrame' || n.data.viewMode === 'collapsed');
          const newMode = allCollapsed ? 'normal' : 'collapsed';
          setNodes(nodes.map((n) => n.type === 'groupFrame' ? n : { ...n, data: { ...n.data, viewMode: newMode } }));
        }}
        className="flex items-center gap-1.5 px-2 py-1.5 bg-gray-700 hover:bg-gray-600 text-gray-300 hover:text-white text-sm rounded transition-colors"
        title={nodes.every((n) => n.type === 'groupFrame' || n.data.viewMode === 'collapsed') ? "Expand all nodes" : "Collapse all nodes"}
      >
        {nodes.every((n) => n.type === 'groupFrame' || n.data.viewMode === 'collapsed') ? <Maximize2 size={14} /> : <Minimize2 size={14} />}
      </button>

      {isEditingName ? (
        <input
          ref={nameInputRef}
          value={editName}
          onChange={(e) => setEditName(e.target.value)}
          onBlur={() => {
            const trimmed = editName.trim();
            if (trimmed) renameGraph(trimmed);
            setIsEditingName(false);
          }}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              const trimmed = editName.trim();
              if (trimmed) renameGraph(trimmed);
              setIsEditingName(false);
            } else if (e.key === 'Escape') {
              setIsEditingName(false);
            }
          }}
          className="text-sm text-white bg-gray-700 border border-blue-500 rounded px-2 py-0.5 outline-none w-48"
          autoFocus
        />
      ) : (
        <div
          className="text-sm text-gray-400 cursor-pointer hover:text-gray-200 transition-colors"
          onDoubleClick={() => {
            setEditName(graph?.name || 'Untitled');
            setIsEditingName(true);
          }}
          title="Double-click to rename"
        >
          {graph?.name || 'Untitled'}
          {isDirty && <span className="ml-2 text-yellow-500">•</span>}
        </div>
      )}

      <button
        onClick={handleSave}
        disabled={!isDirty || isSaving}
        className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white text-sm rounded transition-colors"
      >
        <Save size={16} />
        {isSaving ? 'Saving...' : 'Save'}
      </button>

      <button
        onClick={() => fileInputRef.current?.click()}
        className="flex items-center gap-2 px-3 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded transition-colors"
        title="Load from JSON"
      >
        <Upload size={16} />
        Load
      </button>

      <input
        ref={fileInputRef}
        type="file"
        accept=".json"
        onChange={handleLoadJSON}
        className="hidden"
      />

      <div className="relative" ref={examplesRef}>
        <button
          onClick={handleShowExamples}
          className="flex items-center gap-2 px-3 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded transition-colors"
          title="Load example graph"
        >
          <BookOpen size={16} />
          Examples
        </button>
        {showExamplesMenu && (
          <div className="absolute right-0 top-full mt-1 w-72 bg-gray-800 border border-gray-600 rounded-lg shadow-xl z-50 overflow-hidden">
            {examplesList.map((ex) => (
              <button
                key={ex.id}
                onClick={() => handleLoadExample(ex.id)}
                className="w-full text-left px-4 py-3 hover:bg-gray-700 transition-colors border-b border-gray-700 last:border-b-0"
              >
                <div className="text-sm font-medium text-white">{ex.name}</div>
                <div className="text-xs text-gray-400 mt-1">{ex.description}</div>
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="relative flex" ref={downloadRef}>
        <button
          onClick={handleDownloadJSON}
          className="flex items-center gap-1.5 px-3 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded-l transition-colors"
        >
          <FileDown size={16} />
          Download
        </button>
        <button
          onClick={() => setShowDownloadMenu(!showDownloadMenu)}
          className="flex items-center px-1.5 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded-r border-l border-gray-600 transition-colors"
        >
          <ChevronDown size={12} />
        </button>
        {showDownloadMenu && (
          <div className="absolute top-full left-0 mt-1 bg-gray-800 border border-gray-600 rounded shadow-lg z-50 min-w-[140px]">
            <button
              onClick={() => { handleDownloadJSON(); setShowDownloadMenu(false); }}
              className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-200 hover:bg-gray-700 transition-colors"
            >
              <Braces size={14} />
              JSON
            </button>
            <button
              onClick={() => { handleDownloadPython(); setShowDownloadMenu(false); }}
              className={`w-full flex items-center gap-2 px-3 py-2 text-sm transition-colors ${generatedCode ? 'text-gray-200 hover:bg-gray-700' : 'text-gray-500 cursor-not-allowed'}`}
              disabled={!generatedCode}
            >
              <Code size={14} />
              Python
            </button>
            <button
              onClick={() => { handleDownloadImage('png'); setShowDownloadMenu(false); }}
              className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-200 hover:bg-gray-700 transition-colors"
            >
              <Image size={14} />
              PNG
            </button>
            <button
              onClick={() => { handleDownloadImage('svg'); setShowDownloadMenu(false); }}
              className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-200 hover:bg-gray-700 transition-colors"
            >
              <Image size={14} />
              SVG
            </button>
          </div>
        )}
      </div>

      <button
        onClick={() => setShowExportDialog(true)}
        className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm rounded-l transition-colors"
      >
        <Download size={16} />
        Export Video
      </button>
      <a
        href="/api/export/latest/download"
        download
        className="flex items-center px-2 py-2 bg-green-600 hover:bg-green-700 text-white text-sm border-l border-green-500 transition-colors"
        title="Download latest export"
      >
        <FileDown size={16} />
      </a>
      <button
        onClick={async () => {
          const res = await fetch('/api/open-folder/exports', { method: 'POST' });
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
        className="flex items-center px-2 py-2 bg-green-600 hover:bg-green-700 text-white text-sm rounded-r border-l border-green-500 transition-colors"
        title="Open exports folder"
      >
        <FolderOpen size={16} />
      </button>

      {/* Export Dialog */}
      {showExportDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
             onClick={() => setShowExportDialog(false)}>
          <div className="bg-gray-800 rounded-lg p-6 max-w-md w-full"
               onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-semibold text-white mb-6">Export Animation</h2>

            {/* Quality selector */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Quality
              </label>
              <select
                value={exportQuality}
                onChange={(e) => setExportQuality(e.target.value)}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:outline-none focus:border-blue-500"
              >
                <option value="480p">480p (Low - Fastest)</option>
                <option value="720p">720p (Medium)</option>
                <option value="1080p">1080p (High)</option>
                <option value="1440p">1440p (2K)</option>
                <option value="2160p">2160p (4K)</option>
              </select>
            </div>

            {/* FPS selector */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Frame Rate (FPS)
              </label>
              <select
                value={exportFps}
                onChange={(e) => setExportFps(Number(e.target.value))}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:outline-none focus:border-blue-500"
              >
                <option value={15}>15 FPS</option>
                <option value={24}>24 FPS (Film)</option>
                <option value={30}>30 FPS (Standard)</option>
                <option value={60}>60 FPS (Smooth)</option>
              </select>
            </div>

            {/* Format selector */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Format
              </label>
              <select
                value={exportFormat}
                onChange={(e) => setExportFormat(e.target.value as 'mp4' | 'gif')}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white focus:outline-none focus:border-blue-500"
              >
                <option value="mp4">MP4 (Video)</option>
                <option value="gif">GIF (Animated Image)</option>
              </select>
            </div>

            {/* Info text */}
            <p className="text-sm text-gray-400 mb-6">
              {exportFormat === 'gif'
                ? 'Export will generate an animated GIF. File sizes may be large for long animations.'
                : 'Export will generate a high-quality MP4 video. This may take several minutes depending on complexity and quality settings.'}
            </p>

            {/* Action buttons */}
            <div className="flex gap-3">
              <button
                onClick={() => setShowExportDialog(false)}
                disabled={isExporting}
                className="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 disabled:bg-gray-800 disabled:cursor-not-allowed text-white rounded transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleExport}
                disabled={isExporting}
                className="flex-1 px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded transition-colors"
              >
                {isExporting ? 'Exporting...' : 'Export'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
