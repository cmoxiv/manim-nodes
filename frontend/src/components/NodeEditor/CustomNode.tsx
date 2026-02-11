import { memo, useState, useEffect } from 'react';
import { Handle, Position, NodeProps, useReactFlow, useUpdateNodeInternals } from 'reactflow';
import { ChevronDown, ChevronUp } from 'lucide-react';

// Helper function to get handle style based on type
function getHandleStyle(type: string, isSource: boolean = false) {
  const baseStyle = {
    width: '12px',
    height: '12px',
    border: '2px solid #1e293b',
  };

  // Shape/Mobject types - Circle (same color for input/output)
  if (type === 'Mobject' || type === 'shape' || type === 'mobject' || type === 'group') {
    return {
      ...baseStyle,
      background: '#3B82F6', // Blue for both input and output
      borderRadius: '50%', // Circle
    };
  }

  // Sequence types - Square
  if (type === 'Sequence') {
    return {
      ...baseStyle,
      background: '#F59E0B',
      borderRadius: '2px', // Square
      width: '14px',
      height: '14px',
    };
  }

  // Animation types - Triangle pointing sideways (play button style)
  if (type === 'Animation' || type === 'animation') {
    return {
      ...baseStyle,
      background: '#A855F7', // Purple for both
      borderRadius: '0',
      border: 'none',
      // Triangle pointing right for output, left for input
      clipPath: isSource
        ? 'polygon(0% 0%, 0% 100%, 100% 50%)'  // Right-pointing triangle
        : 'polygon(100% 0%, 0% 50%, 100% 100%)', // Left-pointing triangle
      width: '12px',
      height: '14px',
    };
  }

  // Number type - Small diamond
  if (type === 'Number') {
    return {
      ...baseStyle,
      background: '#14B8A6', // Teal
      transform: 'rotate(45deg)',
      borderRadius: '2px',
      width: '10px',
      height: '10px',
    };
  }

  // Vec3 type - Teal triangle
  if (type === 'Vec3') {
    return {
      ...baseStyle,
      background: '#14B8A6',
      borderRadius: '0',
      border: 'none',
      clipPath: isSource
        ? 'polygon(0% 0%, 0% 100%, 100% 50%)'
        : 'polygon(100% 0%, 0% 50%, 100% 100%)',
      width: '12px',
      height: '14px',
    };
  }

  // Vec2 type - Pentagon (star-like)
  if (type === 'Vec2') {
    return {
      ...baseStyle,
      background: '#8B5CF6', // Violet
      borderRadius: '2px',
      clipPath: 'polygon(50% 0%, 100% 40%, 80% 100%, 20% 100%, 0% 40%)', // Pentagon
      width: '14px',
      height: '14px',
    };
  }

  // Matrix type - Larger diamond
  if (type === 'Matrix') {
    return {
      ...baseStyle,
      background: '#14B8A6', // Teal
      transform: 'rotate(45deg)',
      borderRadius: '2px',
      width: '12px',
      height: '12px',
    };
  }

  // Color type - Pink circle
  if (type === 'Color') {
    return {
      ...baseStyle,
      background: '#EC4899', // Pink
      borderRadius: '50%',
    };
  }

  // Default - Circle
  return {
    ...baseStyle,
    background: isSource ? '#10B981' : '#3B82F6',
    borderRadius: '50%',
  };
}

function CustomNode({ data, selected, id }: NodeProps) {
  const { setNodes, getNodes, getEdges } = useReactFlow();
  const updateNodeInternals = useUpdateNodeInternals();
  const hasInputs = data.inputs && Object.keys(data.inputs).length > 0;

  const [showParams, setShowParams] = useState(false); // Collapsed by default
  const [editingName, setEditingName] = useState(false);
  const [nameInput, setNameInput] = useState(data.name || '');

  // Check if node has parameters to show
  const parameters = Object.entries(data).filter(([key]) =>
    !['type', 'category', 'inputs', 'outputs', 'error', 'label', 'name', 'copy', 'animate', 'write_label'].includes(key)
  );
  const hasParameters = parameters.length > 0;

  // Get effective color for Color node (from connected Vec3 or fallback to color_value)
  const getColorPreview = (): string => {
    if (data.type !== 'Color') return data.color_value || '#FFFFFF';
    const edges = getEdges();
    const rgbEdge = edges.find((e: any) => e.target === id && e.targetHandle === 'param_rgb');
    if (rgbEdge) {
      const nodes = getNodes();
      const sourceNode = nodes.find((n: any) => n.id === rgbEdge.source);
      if (sourceNode?.data?.values) {
        const raw = String(sourceNode.data.values).replace(/[\[\]()]/g, '');
        const vals = raw.split(',').map((s: string) => parseFloat(s.trim()));
        if (vals.length >= 3 && vals.every((v: number) => !isNaN(v))) {
          let [r, g, b] = vals;
          if (r > 1 || g > 1 || b > 1) { r /= 255; g /= 255; b /= 255; }
          const h = (v: number) => Math.round(Math.min(1, Math.max(0, v)) * 255).toString(16).padStart(2, '0');
          return `#${h(r)}${h(g)}${h(b)}`;
        }
      }
    }
    return data.color_value || '#FFFFFF';
  };

  const colorPreview = data.type === 'Color' ? getColorPreview() : '';

  // For ExposeParameters: only show selected param outputs + shape passthrough
  const getVisibleOutputs = (): Record<string, string> => {
    if (data.type !== 'ExposeParameters' || !data.outputs) return data.outputs;

    const selected = new Set(
      [data.param_1, data.param_2, data.param_3].filter((p: string) => p && p !== 'none')
    );

    const filtered: Record<string, string> = { shape: data.outputs.shape };
    for (const key of selected) {
      if (data.outputs[key]) filtered[key] = data.outputs[key];
    }
    return filtered;
  };

  const visibleOutputs = getVisibleOutputs();
  const hasOutputs = visibleOutputs && Object.keys(visibleOutputs).length > 0;

  // Notify React Flow when handles change (needed for dynamic outputs like ExposeParameters)
  const outputKeys = Object.keys(visibleOutputs || {}).join(',');
  const inputKeys = Object.keys(data.inputs || {}).join(',');
  useEffect(() => {
    updateNodeInternals(id);
  }, [outputKeys, inputKeys, id, updateNodeInternals]);

  // Get summary info to display in header
  const getSummaryInfo = () => {
    const type = data.type;

    // Vec3: Show expression as-is
    if (type === 'Vec3') {
      return data.values || '0, 0, 0';
    }

    // Number: Show value
    if (type === 'Number') {
      const value = data.value ?? '0';
      return `= ${value}`;
    }

    // Color: Show value
    if (type === 'Color') {
      return data.color_value || '#FFFFFF';
    }

    // Shapes: Show position
    if (['Circle', 'Square', 'Rectangle', 'Triangle', 'Sphere', 'Cube', 'Cone', 'Cylinder', 'Torus'].includes(type)) {
      return data.position || '[0, 0, 0]';
    }

    // Line/Arrow: Show start → end
    if (['Line', 'Arrow'].includes(type)) {
      const start = data.start || '[-2, 0, 0]';
      const end = data.end || '[2, 0, 0]';
      return `${start} → ${end}`;
    }

    // Text nodes: Show text content
    if (type === 'Text' || type === 'MathTex') {
      const text = data.text || data.tex || '';
      return text.length > 20 ? `"${text.substring(0, 20)}..."` : `"${text}"`;
    }

    // Animations: Show run_time
    if (['FadeIn', 'FadeOut', 'Create', 'Write', 'Rotate', 'Scale', 'MoveTo', 'Morph', 'SquareFromEdge'].includes(type)) {
      const runTime = data.run_time ?? '1.0';
      return `${runTime}s`;
    }

    return '';
  };

  const summaryInfo = getSummaryInfo();

  // Update node data
  const updateNodeData = (key: string, value: any) => {
    setNodes((nodes) =>
      nodes.map((node) => {
        if (node.id === id) {
          return {
            ...node,
            data: {
              ...node.data,
              [key]: value,
            },
          };
        }
        return node;
      })
    );
  };

  // Determine node category for styling
  const nodeCategory = data.category || 'default';
  const isShapes2D = nodeCategory === 'Shapes 2D';
  const isShapes3D = nodeCategory === 'Shapes 3D';
  const isTextMath = nodeCategory === 'Text & Math';
  const isAnimation = nodeCategory === 'Animations';
  const isCamera = nodeCategory === 'Camera';

  // Nodes that need double height (many handles)
  const tallNodeTypes = ['AnimationGroup', 'Sequence'];
  const isTallNode = tallNodeTypes.includes(data.type);

  // Color scheme based on category
  const bgColor = isShapes2D ? 'bg-blue-900' :
                  isShapes3D ? 'bg-cyan-900' :
                  isTextMath ? 'bg-green-900' :
                  isAnimation ? 'bg-violet-900' :
                  isCamera ? 'bg-orange-900' :
                  'bg-gray-800';
  const borderColor = selected ? 'border-blue-400' :
                      isShapes2D ? 'border-blue-600' :
                      isShapes3D ? 'border-cyan-600' :
                      isTextMath ? 'border-green-600' :
                      isAnimation ? 'border-violet-600' :
                      isCamera ? 'border-orange-600' :
                      'border-gray-600';

  return (
    <div
      className={`
        px-4 py-3 rounded-lg border-2 ${bgColor}
        ${borderColor}
        ${data.error ? 'border-red-500' : ''}
        min-w-[150px]
        ${isTallNode ? 'min-h-[160px]' : data.type === 'TransformInPlace' ? 'min-h-[100px]' : ''}
      `}
    >
      {/* Input handles */}
      {hasInputs &&
        Object.entries(data.inputs).map(([name, type], index) => {
          // Special handling for Sequence animation inputs - use triangle shape like animation nodes
          const isSequenceAnimInput = data.type === 'Sequence' && (type === 'Animation' || type === 'animation');
          const handleStyle = isSequenceAnimInput
            ? {
                background: '#A855F7',  // Purple like animation connectors
                width: '12px',
                height: '14px',
                borderRadius: '0',
                border: 'none',
                clipPath: 'polygon(100% 0%, 0% 50%, 100% 100%)',  // Left-pointing triangle (input)
              }
            : getHandleStyle(type as string, false);

          // Regular input handles (left side)
          const topPosition = ((index + 1) / (Object.keys(data.inputs).length + 1)) * 100;

          return (
            <div key={name} style={{ position: 'absolute', left: '-8px', top: `${topPosition}%`, transform: 'translateY(-50%)' }}>
              <Handle
                type="target"
                position={Position.Left}
                id={name}
                style={{
                  ...handleStyle,
                  position: 'relative',
                  left: 0,
                  top: 0,
                  transform: 'none',
                }}
                title={`${name} (${type})`}
              />
              {/* Parameter name label */}
              {name.startsWith('param_') && (
                <div
                  className="text-[9px] text-gray-400 absolute whitespace-nowrap"
                  style={{
                    right: '18px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    pointerEvents: 'none',
                  }}
                >
                  {name.replace('param_', '')}
                </div>
              )}
            </div>
          );
        })}

      {/* Node header */}
      <div className="flex items-center justify-between gap-2">
        <div className="flex-1 min-w-0">
          {editingName ? (
            <input
              type="text"
              value={nameInput}
              onChange={(e) => setNameInput(e.target.value)}
              onBlur={() => {
                updateNodeData('name', nameInput || data.type.toLowerCase());
                setEditingName(false);
              }}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  updateNodeData('name', nameInput || data.type.toLowerCase());
                  setEditingName(false);
                }
                if (e.key === 'Escape') {
                  setNameInput(data.name || '');
                  setEditingName(false);
                }
              }}
              autoFocus
              className="text-sm font-semibold text-white bg-gray-700 border border-gray-500 rounded px-1 py-0 w-full font-mono outline-none"
            />
          ) : (
            <div
              className="text-sm font-semibold text-white truncate cursor-pointer font-mono"
              onDoubleClick={() => {
                setNameInput(data.name || '');
                setEditingName(true);
              }}
              title="Double-click to rename"
            >
              {data.name || data.type}
            </div>
          )}
          <div className="text-[10px] text-gray-500 truncate">{data.type}</div>
          {/* Summary info - always visible */}
          {summaryInfo && (
            <div className="text-xs text-gray-400 truncate mt-0.5 flex items-center gap-1.5">
              {data.type === 'Color' && (
                <input
                  type="color"
                  value={colorPreview}
                  onChange={(e) => updateNodeData('color_value', e.target.value)}
                  className="w-5 h-5 rounded border border-gray-600 flex-shrink-0 cursor-pointer p-0"
                  style={{ background: colorPreview }}
                  title="Click to pick color"
                />
              )}
              {summaryInfo}
            </div>
          )}
        </div>
        <div className="flex items-center gap-1 flex-shrink-0">
          {/* Animate toggle for animation nodes */}
          {isAnimation && data.animate !== undefined && (
            <label className="flex items-center gap-0.5 cursor-pointer" title="Animate (True) or apply instantly (False)">
              <input type="checkbox" checked={data.animate ?? true}
                onChange={(e) => updateNodeData('animate', e.target.checked)} className="w-3 h-3" />
              <span className="text-[10px] text-gray-400">anim</span>
            </label>
          )}
          {/* Copy toggle for animation nodes */}
          {isAnimation && data.copy !== undefined && (
            <label className="flex items-center gap-0.5 cursor-pointer" title="Animate a copy (preserves original)">
              <input type="checkbox" checked={data.copy || false}
                onChange={(e) => updateNodeData('copy', e.target.checked)} className="w-3 h-3" />
              <span className="text-[10px] text-gray-400">cp</span>
            </label>
          )}
          {/* Write-label toggle for nodes with labels */}
          {data.write_label !== undefined && (
            <label className="flex items-center gap-0.5 cursor-pointer" title="Auto-add label to scene">
              <input type="checkbox" checked={data.write_label || false}
                onChange={(e) => updateNodeData('write_label', e.target.checked)} className="w-3 h-3" />
              <span className="text-[10px] text-gray-400">lbl</span>
            </label>
          )}
          {/* Show creation order badge if exists */}
          {data.order !== undefined && data.order !== 0 && (
            <div className="px-2 py-0.5 bg-blue-500 text-white text-xs font-bold rounded-full" title="Creation order">
              #{data.order}
            </div>
          )}
          {/* Toggle button for parameters */}
          {hasParameters && (
            <button
              onClick={() => setShowParams(!showParams)}
              className="p-1 hover:bg-gray-700 rounded transition-colors"
              title={showParams ? "Hide parameters" : "Show parameters"}
            >
              {showParams ? (
                <ChevronUp size={16} className="text-gray-400" />
              ) : (
                <ChevronDown size={16} className="text-gray-400" />
              )}
            </button>
          )}
        </div>
      </div>

      {/* Error indicator */}
      {data.error && (
        <div className="text-xs text-red-400 mt-2">
          Error: {data.error}
        </div>
      )}

      {/* Node parameters */}
      {showParams && (
        <div className="mt-2 space-y-2">
          {/* Special rendering for Matrix nodes */}
          {data.type === 'Matrix' && (
            <div className="mb-3">
              <label className="text-xs text-gray-400 mb-1 block">Matrix 4x4</label>
              <div className="grid grid-cols-4 gap-1">
                {['m11', 'm12', 'm13', 'm14',
                  'm21', 'm22', 'm23', 'm24',
                  'm31', 'm32', 'm33', 'm34',
                  'm41', 'm42', 'm43', 'm44'].map((key) => (
                  <input
                    key={key}
                    type="text"
                    value={data[key] ?? '0'}
                    onChange={(e) => {
                      updateNodeData(key, e.target.value);
                    }}
                    className="w-10 px-1 py-0.5 text-xs bg-gray-700 border border-gray-600 rounded text-white text-center font-mono"
                  />
                ))}
              </div>
            </div>
          )}

          {/* Regular parameters (skip matrix fields if Matrix node) */}
          {Object.entries(data).map(([key, value]) => {
            // Skip internal properties and name (shown in header)
            if (['type', 'category', 'inputs', 'outputs', 'error', 'label', 'name', 'copy', 'animate', 'write_label'].includes(key)) {
              return null;
            }

            // Skip matrix fields for Matrix node (already rendered as grid)
            if (data.type === 'Matrix' && key.startsWith('m') && key.length === 3) {
              return null;
            }
            // Skip matrix fields for Transform node
            if (data.type === 'Transform' && key.startsWith('m') && key.length === 3) {
              return null;
            }
            // Skip param selectors for ExposeParameters (use Inspector dropdowns)
            if (data.type === 'ExposeParameters' && key.startsWith('param_')) {
              return null;
            }

            const isBoolean = typeof value === 'boolean';
            const isColor = key.includes('color') || key.includes('Color');

            return (
              <div key={key} className="flex items-center gap-2">
                <label className="text-xs text-gray-400 capitalize whitespace-nowrap w-16 text-right flex-shrink-0">
                  {key.replace(/_/g, ' ')}
                </label>
                {isBoolean ? (
                  <input
                    type="checkbox"
                    checked={value as boolean}
                    onChange={(e) => {
                      updateNodeData(key, e.target.checked);
                    }}
                    className="w-4 h-4"
                  />
                ) : isColor ? (
                  <input
                    type="color"
                    value={value as string}
                    onChange={(e) => {
                      updateNodeData(key, e.target.value);
                    }}
                    className="w-full h-6 rounded border border-gray-600 bg-gray-700"
                  />
                ) : (
                  <input
                    type="text"
                    value={value as string}
                    onChange={(e) => {
                      updateNodeData(key, e.target.value);
                    }}
                    className="flex-1 min-w-0 px-2 py-1 text-xs bg-gray-700 border border-gray-600 rounded text-white font-mono"
                  />
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Output handles */}
      {hasOutputs &&
        Object.entries(visibleOutputs).map(([name, type], index) => {
          // Regular output handles (right side)
          const topPosition = ((index + 1) / (Object.keys(visibleOutputs).length + 1)) * 100;

          return (
            <div key={name} style={{ position: 'absolute', right: '-8px', top: `${topPosition}%`, transform: 'translateY(-50%)' }}>
              <Handle
                type="source"
                position={Position.Right}
                id={name}
                style={{
                  ...getHandleStyle(type as string, true),
                  position: 'relative',
                  right: 0,
                  top: 0,
                  transform: 'none',
                }}
                title={`${name} (${type})`}
              />
              {/* Output name label */}
              <div
                className="text-[9px] text-gray-400 absolute whitespace-nowrap"
                style={{
                  left: '18px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  pointerEvents: 'none',
                }}
              >
                {name}
              </div>
            </div>
          );
        })}
    </div>
  );
}

export default memo(CustomNode);
