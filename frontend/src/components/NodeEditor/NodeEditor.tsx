import { useCallback, useState, useRef, useEffect } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  NodeTypes,
  useReactFlow,
  Connection,
  useStoreApi,
} from 'reactflow';
import { useGraphStore } from '../../store/useGraphStore';
import { useUIStore } from '../../store/useUIStore';
import CustomNode from './CustomNode';
import GroupFrameNode from './GroupFrameNode';
import ConnectionMenu from './ConnectionMenu';
import { apiClient } from '../../api/client';

// Line segment intersection test
function segmentsIntersect(
  ax: number, ay: number, bx: number, by: number,
  cx: number, cy: number, dx: number, dy: number,
): boolean {
  const det = (bx - ax) * (dy - cy) - (by - ay) * (dx - cx);
  if (Math.abs(det) < 1e-10) return false;
  const t = ((cx - ax) * (dy - cy) - (cy - ay) * (dx - cx)) / det;
  const u = ((cx - ax) * (by - ay) - (cy - ay) * (bx - ax)) / det;
  return t >= 0 && t <= 1 && u >= 0 && u <= 1;
}

const nodeTypes: NodeTypes = {
  custom: CustomNode,
  groupFrame: GroupFrameNode,
};

export default function NodeEditor() {
  const { nodes, edges, onNodesChange, onEdgesChange, onConnect, addNode, setGraph, setNodes, duplicateNodes } = useGraphStore();
  const setSelectedNode = useUIStore((state) => state.setSelectedNode);
  const setViewport = useUIStore((state) => state.setViewport);
  const reactFlowInstance = useReactFlow();
  const { screenToFlowPosition } = reactFlowInstance;
  const storeApi = useStoreApi();

  const [menuState, setMenuState] = useState<{
    visible: boolean;
    position: { x: number; y: number };
    sourceNode?: string;
    sourceHandle?: string;
    targetNode?: string;
    targetHandle?: string;
  }>({
    visible: false,
    position: { x: 0, y: 0 },
  });

  const [isDraggingFile, setIsDraggingFile] = useState(false);
  const [fileDropPrompt, setFileDropPrompt] = useState<{
    visible: boolean;
    position: { x: number; y: number };
    flowPosition: { x: number; y: number };
    graphData: any;
    fileName: string;
  } | null>(null);
  const connectingRef = useRef<Connection | null>(null);

  // Edge cutting state (screen = SVG overlay coords, client = for flow conversion)
  const [cuttingLine, setCuttingLine] = useState<{
    start: { x: number; y: number };
    end: { x: number; y: number };
    startClient: { x: number; y: number };
    endClient: { x: number; y: number };
  } | null>(null);
  const isCuttingRef = useRef(false);
  const wrapperRef = useRef<HTMLDivElement>(null);

  // Attach/detach nodes to/from group frames on drag stop
  const handleNodeDragStop = useCallback(
    (_event: any, draggedNode: any) => {
      if (draggedNode.type === 'groupFrame') return;

      const currentNodes = useGraphStore.getState().nodes;
      const frames = currentNodes.filter((n) => n.type === 'groupFrame');

      // Look up parentNode from Zustand store (draggedNode from the callback may lack it)
      const storeNode = currentNodes.find((n) => n.id === draggedNode.id);
      const currentParentId = storeNode?.parentNode;

      // Get absolute position of the dragged node
      let absX = draggedNode.position.x;
      let absY = draggedNode.position.y;
      if (currentParentId) {
        const parent = currentNodes.find((n) => n.id === currentParentId);
        if (parent) {
          absX += parent.position.x;
          absY += parent.position.y;
        }
      }

      const nodeW = draggedNode.width || 210;
      const nodeH = draggedNode.height || 60;
      const nodeCenterX = absX + nodeW / 2;
      const nodeCenterY = absY + nodeH / 2;

      // Find containing frame
      let targetFrame: any = null;
      for (const frame of frames) {
        const fw = frame.width || frame.data?.width || 400;
        const fh = frame.height || frame.data?.height || 300;
        if (
          nodeCenterX >= frame.position.x &&
          nodeCenterX <= frame.position.x + fw &&
          nodeCenterY >= frame.position.y &&
          nodeCenterY <= frame.position.y + fh
        ) {
          targetFrame = frame;
          break;
        }
      }

      const updated = currentNodes.map((n) => {
        if (n.id !== draggedNode.id) return n;

        if (targetFrame && n.parentNode !== targetFrame.id) {
          // Attach to frame (no extent constraint so nodes can be dragged out to detach)
          return {
            ...n,
            parentNode: targetFrame.id,
            extent: undefined,
            position: {
              x: absX - targetFrame.position.x,
              y: absY - targetFrame.position.y,
            },
          };
        }

        if (!targetFrame && n.parentNode) {
          // Detach from frame
          return {
            ...n,
            parentNode: undefined,
            extent: undefined,
            position: { x: absX, y: absY },
          };
        }

        return n;
      });

      setNodes(updated);
    },
    [setNodes]
  );

  const handleSelectionChange = useCallback(
    ({ nodes: selectedNodes }: { nodes: any[] }) => {
      if (selectedNodes.length === 1) {
        const nodeId = selectedNodes[0].id;
        setSelectedNode(nodeId);
        // Highlight edges connected to the selected node
        const { edges: currentEdges } = useGraphStore.getState();
        useGraphStore.setState({
          edges: currentEdges.map((edge) =>
            edge.source === nodeId || edge.target === nodeId
              ? { ...edge, style: { stroke: '#3b82f6', strokeWidth: 3 } }
              : edge.style?.stroke === '#3b82f6'
                ? { ...edge, style: { stroke: '#666', strokeWidth: 2 }, animated: false }
                : edge
          ),
        });
      } else {
        setSelectedNode(null);
        // Clear highlighted edges
        const { edges: currentEdges } = useGraphStore.getState();
        useGraphStore.setState({
          edges: currentEdges.map((edge) =>
            edge.style?.stroke === '#3b82f6'
              ? { ...edge, style: { stroke: '#666', strokeWidth: 2 }, animated: false }
              : edge
          ),
        });
      }
    },
    [setSelectedNode]
  );

  const handleConnectStart = useCallback(
    (_: any, params: { nodeId: string | null; handleId: string | null; handleType: 'source' | 'target' | null }) => {
      if (!params.nodeId || !params.handleType) return;

      connectingRef.current = {
        source: params.handleType === 'source' ? params.nodeId : '',
        target: params.handleType === 'target' ? params.nodeId : '',
        sourceHandle: params.handleType === 'source' ? params.handleId : null,
        targetHandle: params.handleType === 'target' ? params.handleId : null,
      };
    },
    []
  );

  const handleConnectEnd = useCallback(
    (event: any) => {
      // Check if mouse was released over a handle (successful connection)
      const targetIsHandle = event.target.classList.contains('react-flow__handle');
      const targetIsPane = event.target.classList.contains('react-flow__pane');

      // Only show menu if released in empty space (not on a handle)
      if (targetIsPane && !targetIsHandle && connectingRef.current) {
        const { source, sourceHandle, target, targetHandle } = connectingRef.current;

        // Show menu at cursor position
        setMenuState({
          visible: true,
          position: { x: event.clientX, y: event.clientY },
          sourceNode: source || undefined,
          sourceHandle: sourceHandle || undefined,
          targetNode: target || undefined,
          targetHandle: targetHandle || undefined,
        });
      }

      connectingRef.current = null;
    },
    []
  );

  const handleMenuSelect = useCallback(
    async (nodeType: string) => {
      if (!menuState.visible) return;

      try {
        // Fetch node definition
        const nodeDef = await apiClient.getNodeInfo(nodeType);

        // Calculate position (offset from menu position)
        const flowPosition = screenToFlowPosition({
          x: menuState.position.x - 75,
          y: menuState.position.y - 40,
        });

        // Auto-generate name
        const baseName = nodeType.toLowerCase().replace(/[^a-z0-9]/g, '_');
        const count = nodes.filter(n => n.data.type === nodeType).length;
        const autoName = `${baseName}_${count + 1}`;

        // Create new node
        const newNodeId = `${nodeType.toLowerCase()}_${crypto.randomUUID()}`;
        const newNode = {
          id: newNodeId,
          type: 'custom',
          position: flowPosition,
          data: {
            type: nodeType,
            category: nodeDef.category,
            inputs: nodeDef.inputs,
            outputs: nodeDef.outputs,
            name: autoName,
            ...Object.fromEntries(
              Object.entries(nodeDef.schema?.properties || {}).map(([key, prop]: [string, any]) => [
                key,
                prop.default ?? 0,
              ])
            ),
          },
        };

        addNode(newNode);

        // Create connection
        if (menuState.sourceNode) {
          // User dragged FROM a source handle - connect source to new node
          const targetHandle = Object.keys(nodeDef.inputs || {})[0] || 'default';
          onConnect({
            source: menuState.sourceNode,
            target: newNodeId,
            sourceHandle: menuState.sourceHandle || null,
            targetHandle: targetHandle,
          });
        } else if (menuState.targetNode) {
          // User dragged TO a target handle - connect new node to target
          const sourceHandle = Object.keys(nodeDef.outputs || {})[0] || 'default';
          onConnect({
            source: newNodeId,
            target: menuState.targetNode,
            sourceHandle: sourceHandle,
            targetHandle: menuState.targetHandle || null,
          });
        }
      } catch (error) {
        console.error('Failed to create node:', error);
      } finally {
        setMenuState({ visible: false, position: { x: 0, y: 0 } });
      }
    },
    [menuState, addNode, onConnect, screenToFlowPosition]
  );

  const handleMenuClose = useCallback(() => {
    setMenuState({ visible: false, position: { x: 0, y: 0 } });
  }, []);

  // Get source/target type for menu filtering
  const getHandleType = (nodeId?: string, handleId?: string): string | undefined => {
    if (!nodeId) return undefined;
    const node = nodes.find((n) => n.id === nodeId);
    if (!node) return undefined;

    if (menuState.sourceNode) {
      // Dragged from source - get output type
      return node.data.outputs?.[handleId || Object.keys(node.data.outputs || {})[0]];
    } else {
      // Dragged to target - get input type
      return node.data.inputs?.[handleId || Object.keys(node.data.inputs || {})[0]];
    }
  };

  const sourceType = getHandleType(menuState.sourceNode, menuState.sourceHandle || undefined);
  const targetType = getHandleType(menuState.targetNode, menuState.targetHandle || undefined);

  // Drag and drop file handling + node palette drag
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.types.includes('Files')) {
      setIsDraggingFile(true);
    }
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDraggingFile(false);
  }, []);

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDraggingFile(false);

    // Check for palette node drag
    const nodeData = e.dataTransfer.getData('application/manim-node');
    if (nodeData) {
      try {
        const nodeDef = JSON.parse(nodeData);
        const position = screenToFlowPosition({ x: e.clientX, y: e.clientY });

        // Handle frame node drop
        if (nodeDef.type === '__groupFrame') {
          const count = nodes.filter((n: any) => n.type === 'groupFrame').length;
          const newNode = {
            id: `frame-${crypto.randomUUID()}`,
            type: 'groupFrame',
            position,
            style: { width: 400, height: 300 },
            data: { label: `Frame ${count + 1}`, width: 400, height: 300 },
            zIndex: -1,
          };
          addNode(newNode as any);
          return;
        }

        // Get max order from existing nodes
        const maxOrder = nodes.reduce((max: number, node: any) => {
          const nodeOrder = node.data.order;
          return typeof nodeOrder === 'number' && nodeOrder > max ? nodeOrder : max;
        }, -1);

        const hasOrderField = nodeDef.schema?.properties?.order !== undefined;
        const nextOrder = hasOrderField ? maxOrder + 1 : 0;

        const baseName = nodeDef.type.toLowerCase().replace(/[^a-z0-9]/g, '_');
        const count = nodes.filter((n: any) => n.data.type === nodeDef.type).length;
        const autoName = `${baseName}_${count + 1}`;

        const defaultValues: Record<string, any> = {};
        if (nodeDef.schema?.properties) {
          Object.entries(nodeDef.schema.properties).forEach(([key, prop]: [string, any]) => {
            if (prop.default !== undefined) defaultValues[key] = prop.default;
          });
        }

        const newNode = {
          id: `node-${crypto.randomUUID()}`,
          type: 'custom',
          position,
          data: {
            type: nodeDef.type,
            category: nodeDef.category,
            inputs: nodeDef.inputs,
            outputs: nodeDef.outputs,
            name: autoName,
            ...defaultValues,
            ...(hasOrderField && { order: nextOrder }),
          },
        };
        addNode(newNode);
      } catch (error) {
        console.error('Failed to create node from drag:', error);
      }
      return;
    }

    // File drop handling — show prompt to open or import
    const files = Array.from(e.dataTransfer.files);
    const jsonFile = files.find(file => file.name.endsWith('.json'));

    if (!jsonFile) {
      console.warn('No JSON file found in drop');
      return;
    }

    try {
      const text = await jsonFile.text();
      const graphData = JSON.parse(text);

      if (!graphData.nodes || !graphData.edges) {
        alert('Invalid graph file: missing nodes or edges');
        return;
      }

      const flowPos = screenToFlowPosition({ x: e.clientX, y: e.clientY });
      setFileDropPrompt({
        visible: true,
        position: { x: e.clientX, y: e.clientY },
        flowPosition: flowPos,
        graphData,
        fileName: jsonFile.name,
      });
    } catch (error) {
      console.error('Failed to load graph file:', error);
      alert('Failed to load graph file. Please check the file format.');
    }
  }, [setGraph, screenToFlowPosition, addNode, nodes]);

  // File drop prompt handlers
  const handleFileDropOpen = useCallback(() => {
    if (!fileDropPrompt) return;
    setGraph(fileDropPrompt.graphData);
    setFileDropPrompt(null);
  }, [fileDropPrompt, setGraph]);

  const handleFileDropImport = useCallback(async () => {
    if (!fileDropPrompt) return;
    try {
      const nodeDef = await apiClient.getNodeInfo('ImportGraph');
      const baseName = 'importgraph';
      const count = nodes.filter((n: any) => n.data.type === 'ImportGraph').length;
      const autoName = `${baseName}_${count + 1}`;

      // Collect named objects from the dropped graph for expose fields
      const namedObjects = fileDropPrompt.graphData.nodes
        .filter((n: any) => n.data?.name)
        .map((n: any) => n.data.name);

      const newNode = {
        id: `node-${crypto.randomUUID()}`,
        type: 'custom',
        position: fileDropPrompt.flowPosition,
        data: {
          type: 'ImportGraph',
          category: nodeDef.category,
          inputs: nodeDef.inputs,
          outputs: nodeDef.outputs,
          name: autoName,
          graph_file: fileDropPrompt.fileName,
          expose_1: namedObjects[0] || 'none',
          expose_2: namedObjects[1] || 'none',
          expose_3: namedObjects[2] || 'none',
        },
      };
      addNode(newNode);
    } catch (error) {
      console.error('Failed to create ImportGraph node:', error);
    }
    setFileDropPrompt(null);
  }, [fileDropPrompt, addNode, nodes]);

  const handleFileDropClose = useCallback(() => {
    setFileDropPrompt(null);
  }, []);

  // Edge cutting with right-click drag
  const getRelativePos = useCallback((e: React.MouseEvent) => {
    const rect = wrapperRef.current?.getBoundingClientRect();
    return {
      x: e.clientX - (rect?.left || 0),
      y: e.clientY - (rect?.top || 0),
      clientX: e.clientX,
      clientY: e.clientY,
    };
  }, []);

  const handleEdgeCutStart = useCallback((e: React.MouseEvent) => {
    if (e.button !== 2) return; // Right button only
    e.preventDefault();
    isCuttingRef.current = true;
    const pos = getRelativePos(e);
    setCuttingLine({
      start: { x: pos.x, y: pos.y },
      end: { x: pos.x, y: pos.y },
      startClient: { x: pos.clientX, y: pos.clientY },
      endClient: { x: pos.clientX, y: pos.clientY },
    });
  }, [getRelativePos]);

  const handleEdgeCutMove = useCallback((e: React.MouseEvent) => {
    if (!isCuttingRef.current) return;
    const pos = getRelativePos(e);
    setCuttingLine((prev) =>
      prev
        ? { ...prev, end: { x: pos.x, y: pos.y }, endClient: { x: pos.clientX, y: pos.clientY } }
        : null
    );
  }, [getRelativePos]);

  const handleEdgeCutEnd = useCallback(() => {
    if (!isCuttingRef.current || !cuttingLine) {
      isCuttingRef.current = false;
      setCuttingLine(null);
      return;
    }
    isCuttingRef.current = false;

    // Convert cutting line to flow coordinates
    const cutStart = screenToFlowPosition(cuttingLine.startClient);
    const cutEnd = screenToFlowPosition(cuttingLine.endClient);

    // Find edges that intersect the cutting line
    const edgesToRemove: string[] = [];
    const nodeMap = new Map(nodes.map((n) => [n.id, n]));

    for (const edge of edges) {
      const sourceNode = nodeMap.get(edge.source);
      const targetNode = nodeMap.get(edge.target);
      if (!sourceNode || !targetNode) continue;

      // Approximate edge as straight line between node centers
      // (handles add slight offset but this is good enough for cutting)
      const sx = sourceNode.position.x + (sourceNode.width || 180) / 2;
      const sy = sourceNode.position.y + (sourceNode.height || 60) / 2;
      const tx = targetNode.position.x + (targetNode.width || 180) / 2;
      const ty = targetNode.position.y + (targetNode.height || 60) / 2;

      if (segmentsIntersect(
        cutStart.x, cutStart.y, cutEnd.x, cutEnd.y,
        sx, sy, tx, ty,
      )) {
        edgesToRemove.push(edge.id);
      }
    }

    if (edgesToRemove.length > 0) {
      onEdgesChange(edgesToRemove.map((id) => ({ type: 'remove', id })));
    }

    setCuttingLine(null);
  }, [cuttingLine, nodes, edges, onEdgesChange, screenToFlowPosition]);

  const handleContextMenu = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
  }, []);

  // Restore saved viewport on initial mount
  const hasRestoredViewport = useRef(false);
  useEffect(() => {
    if (hasRestoredViewport.current) return;
    hasRestoredViewport.current = true;
    const vp = useUIStore.getState().viewport;
    if (vp) {
      reactFlowInstance.setViewport(vp);
    } else {
      setTimeout(() => reactFlowInstance.fitView(), 0);
    }
  }, [reactFlowInstance]);

  // Keyboard shortcut: Cmd+D / Ctrl+D to duplicate selected nodes
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'd') {
        e.preventDefault();
        const selectedIds = storeApi.getState().nodeInternals
          ? Array.from(storeApi.getState().nodeInternals.values())
              .filter((n: any) => n.selected)
              .map((n: any) => n.id)
          : [];
        if (selectedIds.length > 0) {
          duplicateNodes(selectedIds);
        }
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [duplicateNodes, storeApi]);

  return (
    <>
      {/* Drop zone overlay */}
      {isDraggingFile && (
        <div className="absolute inset-0 z-50 bg-blue-500/20 border-4 border-dashed border-blue-400 flex items-center justify-center pointer-events-none">
          <div className="bg-gray-900 px-8 py-4 rounded-lg border-2 border-blue-400">
            <p className="text-2xl font-bold text-blue-400">Drop JSON file to load graph</p>
          </div>
        </div>
      )}

      <div
        ref={wrapperRef}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onMouseDown={handleEdgeCutStart}
        onMouseMove={handleEdgeCutMove}
        onMouseUp={handleEdgeCutEnd}
        onContextMenu={handleContextMenu}
        className="w-full h-full relative"
      >
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onConnectStart={handleConnectStart}
          onConnectEnd={handleConnectEnd}
          onNodeDragStop={handleNodeDragStop}
          onSelectionChange={handleSelectionChange}
          nodeTypes={nodeTypes}
          className="bg-gray-950"
          connectionRadius={40}
          snapToGrid={true}
          snapGrid={[15, 15]}
          connectionLineStyle={{ stroke: '#fff', strokeWidth: 2 }}
          defaultEdgeOptions={{
            animated: false,
            style: { stroke: '#666', strokeWidth: 2 },
          }}
          edgesUpdatable={true}
          edgesFocusable={true}
          onMoveEnd={(_, viewport) => setViewport(viewport)}

        >
        <Background color="#444" gap={15} />
        <Controls className="bg-gray-800 border-gray-700" />
        <MiniMap
          className="bg-gray-800 border border-gray-700"
          nodeColor="#4B5563"
          maskColor="rgba(0, 0, 0, 0.5)"
        />
      </ReactFlow>

        {/* Edge cutting line overlay */}
        {cuttingLine && (
          <svg
            className="absolute inset-0 pointer-events-none z-40"
            style={{ width: '100%', height: '100%' }}
          >
            <line
              x1={cuttingLine.start.x}
              y1={cuttingLine.start.y}
              x2={cuttingLine.end.x}
              y2={cuttingLine.end.y}
              stroke="#ef4444"
              strokeWidth={2}
              strokeDasharray="6 4"
            />
          </svg>
        )}
      </div>

      {/* Connection Menu */}
      {menuState.visible && (
        <ConnectionMenu
          position={menuState.position}
          sourceType={sourceType}
          targetType={targetType}
          onSelect={handleMenuSelect}
          onClose={handleMenuClose}
        />
      )}

      {/* File drop prompt */}
      {fileDropPrompt?.visible && (
        <>
          <div className="fixed inset-0 z-50" onClick={handleFileDropClose} />
          <div
            className="fixed z-50 bg-gray-800 border border-gray-600 rounded-lg shadow-xl py-1 min-w-[200px]"
            style={{ left: fileDropPrompt.position.x, top: fileDropPrompt.position.y }}
          >
            <div className="px-3 py-1.5 text-[11px] text-gray-400 truncate border-b border-gray-700">
              {fileDropPrompt.fileName}
            </div>
            <button
              onClick={handleFileDropOpen}
              className="w-full text-left px-3 py-2 text-sm text-white hover:bg-gray-700 transition-colors"
            >
              Open Graph
            </button>
            <button
              onClick={handleFileDropImport}
              className="w-full text-left px-3 py-2 text-sm text-white hover:bg-gray-700 transition-colors"
            >
              Import as Node
            </button>
          </div>
        </>
      )}
    </>
  );
}
