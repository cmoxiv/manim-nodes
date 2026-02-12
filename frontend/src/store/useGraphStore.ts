import { create } from 'zustand';
import { Node, Edge, Connection, addEdge, applyNodeChanges, applyEdgeChanges } from 'reactflow';
import { Graph, NodeData, EdgeData } from '../types/graph';
import { apiClient } from '../api/client';
import { useUIStore } from './useUIStore';

interface GraphStore {
  // State
  graph: Graph | null;
  nodes: Node[];
  edges: Edge[];
  isDirty: boolean;
  isSaving: boolean;

  // Actions
  setGraph: (graph: Graph) => void;
  setNodes: (nodes: Node[]) => void;
  setEdges: (edges: Edge[]) => void;
  createNewGraph: () => void;
  loadGraph: (id: string) => Promise<void>;
  saveGraph: () => Promise<void>;
  addNode: (node: Node) => void;
  updateNodeData: (id: string, data: any) => void;
  markErrorEdges: (nodeId: string | null) => void;
  clearErrorEdges: () => void;
  deleteNode: (id: string) => void;
  duplicateNodes: (ids: string[]) => void;
  onNodesChange: (changes: any) => void;
  onEdgesChange: (changes: any) => void;
  onConnect: (connection: Connection) => void;
  clearGraph: () => void;
  renameGraph: (name: string) => void;
}

export const useGraphStore = create<GraphStore>((set, get) => ({
  graph: null,
  nodes: [],
  edges: [],
  isDirty: false,
  isSaving: false,

  setGraph: (graph) => {
    // Convert graph nodes/edges to React Flow format
    const nodes: Node[] = graph.nodes.map((node: any) => ({
      id: node.id,
      type: node.type === '__groupFrame' ? 'groupFrame' : 'custom',
      position: node.position,
      data: node.type === '__groupFrame'
        ? { ...node.data }
        : { ...node.data, type: node.type },
      ...(node.parentNode && { parentNode: node.parentNode }),
      ...(node.style && { style: node.style }),
      ...(node.zIndex !== undefined && { zIndex: node.zIndex }),
    }));

    const edges: Edge[] = graph.edges.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      sourceHandle: edge.sourceHandle,
      targetHandle: edge.targetHandle,
    }));

    // Restore viewport from graph settings, or clear so fitView runs on mount
    const savedViewport = graph.settings?.viewport;
    useUIStore.getState().setViewport(savedViewport || null);

    set({ graph, nodes, edges, isDirty: false });
  },

  setNodes: (nodes) => {
    set({ nodes, isDirty: true });
  },

  setEdges: (edges) => {
    set({ edges, isDirty: true });
  },

  createNewGraph: () => {
    const newGraph: Graph = {
      id: `graph-${crypto.randomUUID()}`,
      name: 'Untitled Animation',
      nodes: [],
      edges: [],
      settings: {
        resolution: '1080p',
        fps: 30,
        background_color: '#000000',
      },
    };

    useUIStore.getState().setViewport(null);

    set({
      graph: newGraph,
      nodes: [],
      edges: [],
      isDirty: false,
    });
  },

  loadGraph: async (id) => {
    try {
      const graph = await apiClient.getGraph(id);
      get().setGraph(graph);
    } catch (error) {
      console.error('Failed to load graph:', error);
      throw error;
    }
  },

  saveGraph: async () => {
    const { graph, nodes, edges } = get();
    if (!graph) return;

    set({ isSaving: true });

    try {
      // Convert React Flow nodes/edges to graph format
      const graphNodes: NodeData[] = nodes.map((node) => ({
        id: node.id,
        type: node.type === 'groupFrame' ? '__groupFrame' : node.data.type,
        position: node.position,
        data: { ...node.data },
        ...(node.parentNode && { parentNode: node.parentNode }),
        ...(node.style && { style: node.style }),
        ...(node.zIndex !== undefined && { zIndex: node.zIndex }),
      }));

      const graphEdges: EdgeData[] = edges.map((edge) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        sourceHandle: edge.sourceHandle,
        targetHandle: edge.targetHandle,
      }));

      const currentViewport = useUIStore.getState().viewport;
      const updatedGraph: Graph = {
        ...graph,
        nodes: graphNodes,
        edges: graphEdges,
        settings: {
          ...graph.settings,
          ...(currentViewport && { viewport: currentViewport }),
        },
      };

      await apiClient.updateGraph(graph.id, updatedGraph);
      set({ graph: updatedGraph, isDirty: false });
    } catch (error) {
      console.error('Failed to save graph:', error);
      throw error;
    } finally {
      set({ isSaving: false });
    }
  },

  addNode: (node) => {
    set((state) => ({
      nodes: [...state.nodes, node],
      isDirty: true,
    }));
  },

  updateNodeData: (id, data) => {
    set((state) => ({
      nodes: state.nodes.map((node) =>
        node.id === id ? { ...node, data: { ...node.data, ...data } } : node
      ),
      isDirty: true,
    }));
  },

  markErrorEdges: (nodeId) => {
    if (!nodeId) return;
    set((state) => ({
      edges: state.edges.map((edge) =>
        edge.source === nodeId || edge.target === nodeId
          ? { ...edge, style: { stroke: '#ef4444', strokeWidth: 3 }, animated: true }
          : edge
      ),
    }));
  },

  clearErrorEdges: () => {
    set((state) => ({
      edges: state.edges.map((edge) =>
        edge.style?.stroke === '#ef4444'
          ? { ...edge, style: { stroke: '#666', strokeWidth: 2 }, animated: false }
          : edge
      ),
    }));
  },

  deleteNode: (id) => {
    set((state) => ({
      nodes: state.nodes.filter((node) => node.id !== id),
      edges: state.edges.filter((edge) => edge.source !== id && edge.target !== id),
      isDirty: true,
    }));
  },

  duplicateNodes: (ids) => {
    const state = get();
    const idMap = new Map<string, string>();
    const newNodes = ids.map((id) => {
      const node = state.nodes.find((n) => n.id === id);
      if (!node) return null;
      const newId = `node-${crypto.randomUUID()}`;
      idMap.set(id, newId);
      return {
        ...node,
        id: newId,
        position: { x: node.position.x + 30, y: node.position.y + 30 },
        selected: false,
        data: { ...node.data, name: node.data.name ? node.data.name + '_copy' : '' },
      };
    }).filter(Boolean) as Node[];
    // Duplicate internal edges between selected nodes
    const newEdges = state.edges
      .filter((e) => ids.includes(e.source) && ids.includes(e.target))
      .map((e) => ({
        ...e,
        id: `edge-${crypto.randomUUID()}`,
        source: idMap.get(e.source) || e.source,
        target: idMap.get(e.target) || e.target,
      }));
    set({
      nodes: [...state.nodes, ...newNodes],
      edges: [...state.edges, ...newEdges],
      isDirty: true,
    });
  },

  onNodesChange: (changes) => {
    set((state) => ({
      nodes: applyNodeChanges(changes, state.nodes),
      isDirty: true,
    }));
  },

  onEdgesChange: (changes) => {
    set((state) => ({
      edges: applyEdgeChanges(changes, state.edges),
      isDirty: true,
    }));
  },

  onConnect: (connection) => {
    set((state) => {
      // Remove any existing edge connected to the same target handle
      const existingEdgeIndex = state.edges.findIndex(
        (edge) =>
          edge.target === connection.target &&
          edge.targetHandle === connection.targetHandle
      );

      let edges = state.edges;
      if (existingEdgeIndex !== -1) {
        // Remove the old connection
        edges = edges.filter((_, index) => index !== existingEdgeIndex);
      }

      // Add the new connection
      return {
        edges: addEdge(connection, edges),
        isDirty: true,
      };
    });
  },

  clearGraph: () => {
    set({
      nodes: [],
      edges: [],
      isDirty: true,
    });
  },

  renameGraph: (name: string) => {
    const { graph } = get();
    if (graph) {
      set({ graph: { ...graph, name }, isDirty: true });
    }
  },
}));
