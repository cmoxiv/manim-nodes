import { useState, useEffect } from 'react';
import { Plus } from 'lucide-react';
import { apiClient } from '../../api/client';
import { NodeDefinition } from '../../types/graph';
import { useGraphStore } from '../../store/useGraphStore';

export default function NodePalette() {
  const [nodes, setNodes] = useState<NodeDefinition[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const addNode = useGraphStore((state) => state.addNode);
  const existingNodes = useGraphStore((state) => state.nodes);

  useEffect(() => {
    loadNodes();
  }, []);

  const loadNodes = async () => {
    try {
      const nodeList = await apiClient.listNodes();
      setNodes(nodeList);
    } catch (error) {
      console.error('Failed to load nodes:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateNodeName = (nodeType: string) => {
    const baseName = nodeType.toLowerCase().replace(/[^a-z0-9]/g, '_');
    const count = existingNodes.filter(n => n.data.type === nodeType).length;
    return `${baseName}_${count + 1}`;
  };

  const handleAddNode = (nodeDef: NodeDefinition) => {
    // Get max order from existing nodes
    const maxOrder = existingNodes.reduce((max, node) => {
      const nodeOrder = node.data.order;
      return typeof nodeOrder === 'number' && nodeOrder > max ? nodeOrder : max;
    }, -1);

    // Auto-increment order for shape nodes (nodes with 'order' field in schema)
    const hasOrderField = nodeDef.schema?.properties?.order !== undefined;
    const nextOrder = hasOrderField ? maxOrder + 1 : 0;

    const defaultValues = getDefaultValues(nodeDef.schema);

    const newNode = {
      id: `node-${crypto.randomUUID()}`,
      type: 'custom',
      position: { x: 250, y: 250 },
      data: {
        type: nodeDef.type,
        category: nodeDef.category,  // Add category for styling
        inputs: nodeDef.inputs,
        outputs: nodeDef.outputs,
        name: generateNodeName(nodeDef.type),
        // Initialize with default values from schema
        ...defaultValues,
        // Override order with auto-incremented value for shape nodes
        ...(hasOrderField && { order: nextOrder }),
      },
    };

    addNode(newNode);
  };

  const getDefaultValues = (schema: any): Record<string, any> => {
    const defaults: Record<string, any> = {};
    if (schema?.properties) {
      Object.entries(schema.properties).forEach(([key, prop]: [string, any]) => {
        if (prop.default !== undefined) {
          defaults[key] = prop.default;
        }
      });
    }
    return defaults;
  };

  // Category order
  const categoryOrder = [
    "Shapes 3D",
    "Shapes 2D",
    "Text & Math",
    "Animations",
    "Camera",
    "Flow",
    "Math Ops",
    "Utilities",
  ];

  // Group nodes by category
  const groupedNodes = nodes.reduce((acc, node) => {
    const category = node.category || 'Uncategorized';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(node);
    return acc;
  }, {} as Record<string, NodeDefinition[]>);

  // Filter nodes
  const filteredGroups = Object.entries(groupedNodes).reduce((acc, [category, categoryNodes]) => {
    const filtered = categoryNodes.filter((node) =>
      node.displayName.toLowerCase().includes(searchTerm.toLowerCase())
    );
    if (filtered.length > 0) {
      acc[category] = filtered;
    }
    return acc;
  }, {} as Record<string, NodeDefinition[]>);

  // Sort categories by defined order
  const sortedCategories = Object.keys(filteredGroups).sort((a, b) => {
    const indexA = categoryOrder.indexOf(a);
    const indexB = categoryOrder.indexOf(b);

    // If both in order list, use that order
    if (indexA !== -1 && indexB !== -1) return indexA - indexB;
    // If only A is in list, it comes first
    if (indexA !== -1) return -1;
    // If only B is in list, it comes first
    if (indexB !== -1) return 1;
    // Otherwise alphabetical
    return a.localeCompare(b);
  });

  if (loading) {
    return (
      <div className="p-4 text-gray-400">
        Loading nodes...
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-lg font-semibold text-white mb-3">Nodes</h2>
        <input
          type="text"
          placeholder="Search nodes..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded text-white text-sm focus:outline-none focus:border-blue-500"
        />
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {sortedCategories.map((category) => {
          const categoryNodes = filteredGroups[category];

          return (
            <div key={category}>
              <h3 className="text-sm font-semibold mb-2 text-gray-400">
                {category}
              </h3>
              <div className="space-y-1">
                {categoryNodes.map((node) => (
                  <button
                    key={node.type}
                    onClick={() => handleAddNode(node)}
                    className="w-full flex items-center gap-2 px-3 py-2 rounded text-left text-sm text-white transition-colors bg-gray-700 hover:bg-gray-600"
                  >
                    <Plus size={16} />
                    <span>{node.displayName}</span>
                  </button>
                ))}
              </div>
            </div>
          );
        })}

        {sortedCategories.length === 0 && (
          <div className="text-center text-gray-500 py-8">
            No nodes found
          </div>
        )}
      </div>
    </div>
  );
}
