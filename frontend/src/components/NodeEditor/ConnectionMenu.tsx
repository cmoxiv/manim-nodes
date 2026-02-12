import { useEffect, useState } from 'react';
import { NodeDefinition } from '../../types/graph';
import { apiClient } from '../../api/client';

interface ConnectionMenuProps {
  position: { x: number; y: number };
  sourceType?: string;
  targetType?: string;
  onSelect: (nodeType: string) => void;
  onClose: () => void;
}

export default function ConnectionMenu({
  position,
  sourceType,
  targetType,
  onSelect,
  onClose,
}: ConnectionMenuProps) {
  const [nodes, setNodes] = useState<NodeDefinition[]>([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    // Fetch available node types
    apiClient.listNodes().then((nodeList: NodeDefinition[]) => {
      // Filter nodes based on compatibility
      let filteredNodes = nodeList;

      if (sourceType) {
        // User dragged FROM a node - filter by compatible inputs
        filteredNodes = nodeList.filter((node: NodeDefinition) => {
          const inputs = Object.values(node.inputs || {});
          return inputs.some((inputType: string) => isCompatible(sourceType, inputType));
        });
      } else if (targetType) {
        // User dragged TO empty space from a target handle - filter by compatible outputs
        filteredNodes = nodeList.filter((node: NodeDefinition) => {
          const outputs = Object.values(node.outputs || {});
          return outputs.some((outputType: string) => isCompatible(outputType, targetType));
        });
      }

      setNodes(filteredNodes);
    });

    // Close menu on escape
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [sourceType, targetType, onClose]);

  // Type compatibility check
  const isCompatible = (outputType: string, inputType: string): boolean => {
    // Exact match
    if (outputType === inputType) return true;

    // "Any" is universally compatible (e.g. Junction pass-through)
    if (outputType === 'Any' || inputType === 'Any') return true;

    // Type hierarchy
    const typeHierarchy: Record<string, string[]> = {
      'Mobject': ['Mobject', 'shape', 'mobject', 'group', 'text', 'axes', 'plane', 'tex', 'vector', 'dot', 'arrow'],
      'Animation': ['Animation'],
      'Color': ['Color'],
    };

    // Check if output type is compatible with input type
    for (const [baseType, subtypes] of Object.entries(typeHierarchy)) {
      if (inputType === baseType && subtypes.includes(outputType)) {
        return true;
      }
    }

    // Legacy compatibility
    if (inputType === 'Mobject' && (outputType === 'shape' || outputType === 'mobject' || outputType === 'group')) return true;
    if (outputType === 'Mobject' && (inputType === 'shape' || inputType === 'mobject' || inputType === 'group')) return true;

    return false;
  };

  const filteredNodes = nodes.filter((node) =>
    node.displayName.toLowerCase().includes(filter.toLowerCase()) ||
    node.category.toLowerCase().includes(filter.toLowerCase())
  );

  // Group by category
  const groupedNodes = filteredNodes.reduce((acc, node) => {
    const category = node.category || 'Other';
    if (!acc[category]) acc[category] = [];
    acc[category].push(node);
    return acc;
  }, {} as Record<string, NodeDefinition[]>);

  return (
    <>
      {/* Backdrop to close menu */}
      <div
        className="fixed inset-0 z-40"
        onClick={onClose}
      />

      {/* Menu */}
      <div
        className="fixed z-50 bg-gray-800 border border-gray-600 rounded-lg shadow-xl max-h-96 overflow-hidden flex flex-col"
        style={{
          left: `${position.x}px`,
          top: `${position.y}px`,
          width: '280px',
        }}
      >
        {/* Search */}
        <div className="p-2 border-b border-gray-700">
          <input
            type="text"
            placeholder="Search nodes..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            autoFocus
            className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
          />
        </div>

        {/* Node list */}
        <div className="overflow-y-auto">
          {Object.entries(groupedNodes).length === 0 ? (
            <div className="p-4 text-center text-gray-500 text-sm">
              No compatible nodes found
            </div>
          ) : (
            Object.entries(groupedNodes).map(([category, categoryNodes]) => (
              <div key={category}>
                <div className="px-3 py-2 text-xs font-semibold text-gray-400 bg-gray-900">
                  {category}
                </div>
                {categoryNodes.map((node) => (
                  <button
                    key={node.type}
                    onClick={() => onSelect(node.type)}
                    className="w-full px-4 py-2 text-left text-sm text-white hover:bg-gray-700 transition-colors flex items-center justify-between"
                  >
                    <span>{node.displayName}</span>
                    <span className="text-xs text-gray-500">{node.type}</span>
                  </button>
                ))}
              </div>
            ))
          )}
        </div>
      </div>
    </>
  );
}
