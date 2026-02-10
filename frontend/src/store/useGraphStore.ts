import { create } from 'zustand';
import { Node, Edge, Connection, addEdge, applyNodeChanges, applyEdgeChanges } from 'reactflow';
import { Graph, NodeData, EdgeData } from '../types/graph';
import { apiClient } from '../api/client';

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
  deleteNode: (id: string) => void;
  onNodesChange: (changes: any) => void;
  onEdgesChange: (changes: any) => void;
  onConnect: (connection: Connection) => void;
  clearGraph: () => void;
}

export const useGraphStore = create<GraphStore>((set, get) => ({
  graph: null,
  nodes: [],
  edges: [],
  isDirty: false,
  isSaving: false,

  setGraph: (graph) => {
    // Convert graph nodes/edges to React Flow format
    const nodes: Node[] = graph.nodes.map((node) => ({
      id: node.id,
      type: 'custom',
      position: node.position,
      data: {
        ...node.data,
        type: node.type,
      },
    }));

    const edges: Edge[] = graph.edges.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      sourceHandle: edge.sourceHandle,
      targetHandle: edge.targetHandle,
    }));

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
        type: node.data.type,
        position: node.position,
        data: { ...node.data },
      }));

      const graphEdges: EdgeData[] = edges.map((edge) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        sourceHandle: edge.sourceHandle,
        targetHandle: edge.targetHandle,
      }));

      const updatedGraph: Graph = {
        ...graph,
        nodes: graphNodes,
        edges: graphEdges,
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

  deleteNode: (id) => {
    set((state) => ({
      nodes: state.nodes.filter((node) => node.id !== id),
      edges: state.edges.filter((edge) => edge.source !== id && edge.target !== id),
      isDirty: true,
    }));
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
}));
