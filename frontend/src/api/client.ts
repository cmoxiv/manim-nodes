import { Graph, NodeDefinition, ExportRequest, ExportStatus } from '../types/graph';

const API_BASE = '/api';

class ApiClient {
  // Graphs
  async createGraph(graph: Graph): Promise<Graph> {
    const response = await fetch(`${API_BASE}/graphs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(graph),
    });
    if (!response.ok) throw new Error('Failed to create graph');
    return response.json();
  }

  async listGraphs(): Promise<Array<{ id: string; name: string; modified: string }>> {
    const response = await fetch(`${API_BASE}/graphs`);
    if (!response.ok) throw new Error('Failed to list graphs');
    return response.json();
  }

  async getGraph(id: string): Promise<Graph> {
    const response = await fetch(`${API_BASE}/graphs/${id}`);
    if (!response.ok) throw new Error('Failed to get graph');
    return response.json();
  }

  async updateGraph(id: string, graph: Graph): Promise<Graph> {
    const response = await fetch(`${API_BASE}/graphs/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(graph),
    });
    if (!response.ok) throw new Error('Failed to update graph');
    return response.json();
  }

  async deleteGraph(id: string): Promise<void> {
    const response = await fetch(`${API_BASE}/graphs/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete graph');
  }

  async getGraphObjects(id: string): Promise<Array<{ name: string; type: string; node_id: string }>> {
    const response = await fetch(`${API_BASE}/graphs/${id}/objects`);
    if (!response.ok) throw new Error('Failed to get graph objects');
    return response.json();
  }

  async validateGraph(graph: Graph): Promise<{ valid: boolean; code?: string; error?: string }> {
    const response = await fetch(`${API_BASE}/graphs/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(graph),
    });
    if (!response.ok) throw new Error('Failed to validate graph');
    return response.json();
  }

  // Nodes
  async listNodes(): Promise<NodeDefinition[]> {
    const response = await fetch(`${API_BASE}/nodes`);
    if (!response.ok) throw new Error('Failed to list nodes');
    return response.json();
  }

  async getNodeInfo(type: string): Promise<NodeDefinition> {
    const response = await fetch(`${API_BASE}/nodes/${type}`);
    if (!response.ok) throw new Error('Failed to get node info');
    return response.json();
  }

  // Export
  async startExport(request: ExportRequest): Promise<{ job_id: string; status: string }> {
    const response = await fetch(`${API_BASE}/export`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });
    if (!response.ok) throw new Error('Failed to start export');
    return response.json();
  }

  async getExportStatus(jobId: string): Promise<ExportStatus> {
    const response = await fetch(`${API_BASE}/export/${jobId}`);
    if (!response.ok) throw new Error('Failed to get export status');
    return response.json();
  }

  getExportDownloadUrl(jobId: string): string {
    return `${API_BASE}/export/${jobId}/download`;
  }

  // Examples
  async listExamples(): Promise<Array<{ id: string; name: string; description: string }>> {
    const response = await fetch(`${API_BASE}/examples`);
    if (!response.ok) throw new Error('Failed to list examples');
    return response.json();
  }

  async getExample(id: string): Promise<any> {
    const response = await fetch(`${API_BASE}/examples/${id}`);
    if (!response.ok) throw new Error('Failed to get example');
    return response.json();
  }
}

export const apiClient = new ApiClient();
