import { useUIStore } from '../../store/useUIStore';
import { useGraphStore } from '../../store/useGraphStore';
import { Settings } from 'lucide-react';
import { useState, useEffect } from 'react';
import { apiClient } from '../../api/client';
import { NodeDefinition } from '../../types/graph';

export default function PropertyInspector() {
  const selectedNodeId = useUIStore((state) => state.selectedNodeId);
  const { nodes, updateNodeData } = useGraphStore();
  const [nodeSchema, setNodeSchema] = useState<NodeDefinition | null>(null);

  const selectedNode = nodes.find((n) => n.id === selectedNodeId);

  // Fetch node schema when node is selected
  useEffect(() => {
    if (selectedNode?.data.type) {
      apiClient.getNodeInfo(selectedNode.data.type)
        .then(setNodeSchema)
        .catch((err) => console.error('Failed to load node schema:', err));
    } else {
      setNodeSchema(null);
    }
  }, [selectedNode?.data.type]);

  if (!selectedNode) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-gray-500 p-4">
        <Settings size={48} className="mb-4 opacity-50" />
        <p>Select a node to edit its properties</p>
      </div>
    );
  }

  const handleChange = (key: string, value: any) => {
    updateNodeData(selectedNodeId!, { [key]: value });
  };

  const renderProperties = () => {
    if (!selectedNode) return null;

    // Check for matrix grid metadata
    const matrixGrid = nodeSchema?.schema?.matrixGrid;
    const matrixFields = new Set(matrixGrid?.fields || []);
    const renderedFields = new Set<string>();

    const properties = [];

    // Render matrix grid if present
    if (matrixGrid && matrixGrid.rows && matrixGrid.cols) {
      properties.push(
        <div key="matrix-grid">
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Transformation Matrix
          </label>
          <div
            className="grid gap-2"
            style={{
              gridTemplateColumns: `repeat(${matrixGrid.cols}, 1fr)`,
            }}
          >
            {matrixGrid.fields.map((fieldName: string) => {
              renderedFields.add(fieldName);
              const value = selectedNode.data[fieldName] ?? '0';
              return (
                <input
                  key={fieldName}
                  type="text"
                  value={value}
                  onChange={(e) => {
                    handleChange(fieldName, e.target.value);
                  }}
                  className="w-10 px-1 py-1 bg-gray-900 border border-gray-700 rounded text-white text-sm text-center font-mono focus:outline-none focus:border-blue-500"
                  placeholder="0"
                />
              );
            })}
          </div>
        </div>
      );
    }

    // Render name field first
    if (selectedNode.data.name !== undefined) {
      properties.push(
        <div key="__name__">
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Name
          </label>
          <input
            type="text"
            value={selectedNode.data.name || ''}
            onChange={(e) => handleChange('name', e.target.value)}
            className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded text-white text-sm font-mono focus:outline-none focus:border-blue-500"
          />
        </div>
      );
    }

    // Render other properties - iterate through schema to show all available properties
    const schemaProperties = nodeSchema?.schema?.properties || {};
    const propertiesToRender = new Map<string, any>();

    // First, collect all properties from schema with their defaults
    Object.keys(schemaProperties).forEach(key => {
      if (!['type', 'inputs', 'outputs', 'category', 'name'].includes(key) && !matrixFields.has(key)) {
        const propSchema = schemaProperties[key];
        propertiesToRender.set(key, selectedNode.data[key] ?? propSchema.default);
      }
    });

    // Then add any properties in data that aren't in schema (for backward compatibility)
    Object.keys(selectedNode.data).forEach(key => {
      if (!['type', 'inputs', 'outputs', 'category', 'name'].includes(key) &&
          !matrixFields.has(key) &&
          !propertiesToRender.has(key)) {
        propertiesToRender.set(key, selectedNode.data[key]);
      }
    });

    // Render all properties
    propertiesToRender.forEach((value, key) => {
      renderedFields.add(key);

      // Get property schema if available
      const propSchema = schemaProperties[key];
      const enumValues = propSchema?.enum;

      properties.push(
        <div key={key}>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            {propSchema?.description || key.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
          </label>

          {/* Enum dropdown */}
          {enumValues ? (
            <select
              value={value as string}
              onChange={(e) => handleChange(key, e.target.value)}
              className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
            >
              {enumValues.map((opt: string) => (
                <option key={opt} value={opt}>
                  {opt}
                </option>
              ))}
            </select>
          ) : /* Boolean checkbox */
          typeof value === 'boolean' ? (
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={value}
                onChange={(e) => handleChange(key, e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-gray-400">
                {value ? 'Enabled' : 'Disabled'}
              </span>
            </label>
          ) : /* Color input */
          typeof value === 'string' && key.includes('color') ? (
            <div className="flex gap-2">
              <input
                type="color"
                value={value}
                onChange={(e) => handleChange(key, e.target.value)}
                className="w-12 h-10 rounded cursor-pointer"
              />
              <input
                type="text"
                value={value}
                onChange={(e) => handleChange(key, e.target.value)}
                className="flex-1 px-3 py-2 bg-gray-900 border border-gray-700 rounded text-white text-sm font-mono focus:outline-none focus:border-blue-500"
              />
            </div>
          ) : /* Text input (handles numbers, expressions, positions) */
          (
            <input
              type="text"
              value={value as string}
              onChange={(e) => handleChange(key, e.target.value)}
              className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded text-white text-sm font-mono focus:outline-none focus:border-blue-500"
            />
          )}
        </div>
      );
    });

    return properties;
  };

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-lg font-semibold text-white">Properties</h2>
        <p className="text-sm text-gray-400 mt-1">{selectedNode.data.type}</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {renderProperties()}
      </div>
    </div>
  );
}
