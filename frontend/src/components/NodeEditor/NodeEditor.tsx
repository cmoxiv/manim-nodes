import { useCallback, useState, useRef } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  NodeTypes,
  useReactFlow,
  Connection,
} from 'reactflow';
import { useGraphStore } from '../../store/useGraphStore';
import { useUIStore } from '../../store/useUIStore';
import CustomNode from './CustomNode';
import ConnectionMenu from './ConnectionMenu';
import { apiClient } from '../../api/client';

const nodeTypes: NodeTypes = {
  custom: CustomNode,
};

export default function NodeEditor() {
  const { nodes, edges, onNodesChange, onEdgesChange, onConnect, addNode, setGraph } = useGraphStore();
  const setSelectedNode = useUIStore((state) => state.setSelectedNode);
  const { screenToFlowPosition } = useReactFlow();

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
  const connectingRef = useRef<Connection | null>(null);

  const handleSelectionChange = useCallback(
    ({ nodes: selectedNodes }: { nodes: any[] }) => {
      if (selectedNodes.length === 1) {
        setSelectedNode(selectedNodes[0].id);
      } else {
        setSelectedNode(null);
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

  // Drag and drop file handling
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

    const files = Array.from(e.dataTransfer.files);
    const jsonFile = files.find(file => file.name.endsWith('.json'));

    if (!jsonFile) {
      console.warn('No JSON file found in drop');
      return;
    }

    try {
      const text = await jsonFile.text();
      const graphData = JSON.parse(text);

      // Validate that it's a graph object
      if (!graphData.nodes || !graphData.edges) {
        alert('Invalid graph file: missing nodes or edges');
        return;
      }

      // Load the graph
      setGraph(graphData);
    } catch (error) {
      console.error('Failed to load graph file:', error);
      alert('Failed to load graph file. Please check the file format.');
    }
  }, [setGraph]);

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
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className="w-full h-full"
      >
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onConnectStart={handleConnectStart}
          onConnectEnd={handleConnectEnd}
          onSelectionChange={handleSelectionChange}
          nodeTypes={nodeTypes}
          fitView
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
        >
        <Background color="#444" gap={16} />
        <Controls className="bg-gray-800 border-gray-700" />
        <MiniMap
          className="bg-gray-800 border border-gray-700"
          nodeColor="#4B5563"
          maskColor="rgba(0, 0, 0, 0.5)"
        />
      </ReactFlow>
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
    </>
  );
}
