import { Node, Edge } from 'reactflow';

export interface NodeData {
  id: string;
  type: string;
  position: { x: number; y: number };
  data: Record<string, any>;
}

export interface EdgeData {
  id: string;
  source: string;
  target: string;
  sourceHandle?: string | null;
  targetHandle?: string | null;
}

export interface Graph {
  id: string;
  name: string;
  nodes: NodeData[];
  edges: EdgeData[];
  settings: Record<string, any>;
}

export interface NodeDefinition {
  type: string;
  displayName: string;
  category: string;
  inputs: Record<string, string>;
  outputs: Record<string, string>;
  schema: any;
}

export interface ExportRequest {
  graph: Graph;
  quality: '480p' | '720p' | '1080p' | '1440p' | '2160p';
  fps: number;
}

export interface ExportStatus {
  job_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  error?: string;
  download_url?: string;
  log: string[];
}

// React Flow types
export type FlowNode = Node<any>;
export type FlowEdge = Edge<any>;
