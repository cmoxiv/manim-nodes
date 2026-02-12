import { memo, useState, useEffect, useRef, useCallback, useMemo } from 'react';
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

// Parse a Python function definition to extract parameter names and return dict keys
function parseFunctionCode(code: string): { params: string[]; outputs: string[] } {
  const params: string[] = [];
  const outputs: string[] = [];

  const defMatch = code.match(/def\s+\w+\(([^)]*)\)/);
  if (defMatch) {
    defMatch[1].split(',').forEach((p) => {
      const name = p.trim().split('=')[0].trim();
      if (name && name !== 'self') params.push(name);
    });
  }

  const returnMatch = code.match(/return\s*\{(.+?)\}/s);
  if (returnMatch) {
    const matches = returnMatch[1].matchAll(/['"](\w+)['"]\s*:/g);
    for (const m of matches) outputs.push(m[1]);
  }

  return { params, outputs };
}

function CustomNode({ data, selected, id }: NodeProps) {
  const { setNodes, getNodes, getEdges } = useReactFlow();
  const updateNodeInternals = useUpdateNodeInternals();
  // 3-state view: 'collapsed' (one-liner), 'normal' (default), 'expanded' (with params)
  const alwaysCollapsed = useMemo(() => ['RIGHT', 'LEFT', 'UP', 'DOWN', 'OUT', 'IN'].includes(data.type), [data.type]);
  const viewMode: 'collapsed' | 'normal' | 'expanded' = data.viewMode || (alwaysCollapsed ? 'collapsed' : 'normal');
  const nodeRef = useRef<HTMLDivElement>(null);

  // When switching view mode, adjust y position so the node shrinks/grows symmetrically
  const changeViewMode = useCallback((newMode: 'collapsed' | 'normal' | 'expanded') => {
    const el = nodeRef.current;
    if (el) {
      const oldH = el.getBoundingClientRect().height;
      // Persist viewMode into node.data so it survives unmounts
      setNodes((nodes) =>
        nodes.map((n) =>
          n.id === id ? { ...n, data: { ...n.data, viewMode: newMode } } : n
        )
      );
      // After React re-renders, measure new height and shift node
      requestAnimationFrame(() => {
        const newH = el.getBoundingClientRect().height;
        const delta = (oldH - newH) / 2;
        if (Math.abs(delta) > 1) {
          setNodes((nodes) =>
            nodes.map((n) =>
              n.id === id ? { ...n, position: { x: n.position.x, y: n.position.y + delta } } : n
            )
          );
        }
      });
    } else {
      setNodes((nodes) =>
        nodes.map((n) =>
          n.id === id ? { ...n, data: { ...n.data, viewMode: newMode } } : n
        )
      );
    }
  }, [id, setNodes]);
  const [editingName, setEditingName] = useState(false);
  const [nameInput, setNameInput] = useState(data.name || '');

  // Check if node has parameters to show
  const parameters = Object.entries(data).filter(([key]) =>
    !['type', 'category', 'inputs', 'outputs', 'error', 'label', 'name', 'copy', 'animate', 'write_label', 'present', 'present_run_time', 'viewMode', 'debugOutput'].includes(key)
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

  // For FunctionCall: find matching FunctionDef and parse its code
  const funcCallParsed = useMemo(() => {
    if (data.type !== 'FunctionCall') return null;
    const allNodes = getNodes();
    const funcDef = allNodes.find(
      (n: any) => n.data.type === 'FunctionDef' && n.data.func_name === data.func_name
    );
    if (!funcDef?.data.code) return null;
    return parseFunctionCode(funcDef.data.code);
  }, [data.type, data.func_name, getNodes]);

  // For FunctionCall: only show inputs matching function parameters
  const getVisibleInputs = (): Record<string, string> => {
    if (data.type !== 'FunctionCall' || !funcCallParsed || !data.inputs) return data.inputs;
    const filtered: Record<string, string> = {};
    funcCallParsed.params.forEach((_, i) => {
      const key = `arg_${i + 1}`;
      if (data.inputs[key]) filtered[key] = data.inputs[key];
    });
    return filtered;
  };

  const visibleInputs = getVisibleInputs();
  const hasVisibleInputs = visibleInputs && Object.keys(visibleInputs).length > 0;

  // For FunctionCall: label map (arg_1 → param name, out_1 → output key)
  const funcCallLabels = useMemo(() => {
    if (!funcCallParsed) return null;
    const labels: Record<string, string> = {};
    funcCallParsed.params.forEach((name, i) => { labels[`arg_${i + 1}`] = name; });
    funcCallParsed.outputs.forEach((name, i) => { labels[`out_${i + 1}`] = name; });
    return labels;
  }, [funcCallParsed]);

  // For ExposeParameters: only show selected param outputs + shape passthrough
  const getVisibleOutputs = (): Record<string, string> => {
    if (data.type === 'FunctionCall' && funcCallParsed && data.outputs) {
      const filtered: Record<string, string> = {};
      funcCallParsed.outputs.forEach((_, i) => {
        const key = `out_${i + 1}`;
        if (data.outputs[key]) filtered[key] = data.outputs[key];
      });
      return filtered;
    }
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

  // Notify React Flow when handles change (needed for dynamic outputs like ExposeParameters, FunctionCall)
  const outputKeys = Object.keys(visibleOutputs || {}).join(',');
  const inputKeys = Object.keys(visibleInputs || {}).join(',');
  useEffect(() => {
    updateNodeInternals(id);
  }, [outputKeys, inputKeys, id, updateNodeInternals]);

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
  const isShape = isShapes2D || isShapes3D || isTextMath;

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

  // Node color (for shapes/text with a color field)
  const nodeColor = data.color || null;
  const hasColorField = nodeColor && data.type !== 'Color';

  // Present mode
  const presentMode = data.present || null;
  const hasPresentField = presentMode !== null && presentMode !== undefined;

  // Get the one-liner summary for collapsed view
  const getCollapsedSummary = (): string => {
    if (data.type === 'RIGHT') return '1, 0, 0';
    if (data.type === 'LEFT') return '-1, 0, 0';
    if (data.type === 'UP') return '0, 1, 0';
    if (data.type === 'DOWN') return '0, -1, 0';
    if (data.type === 'OUT') return '0, 0, 1';
    if (data.type === 'IN') return '0, 0, -1';
    if (data.type === 'Vec3') return data.values || '0, 0, 0';
    if (data.type === 'Number') return `= ${data.value ?? '0'}`;
    if (data.type === 'Color') return colorPreview;
    if (data.type === 'Text') { const t = data.text || ''; return t.length > 18 ? `"${t.substring(0, 18)}…"` : `"${t}"`; }
    if (data.type === 'MathTex') { const t = data.tex || ''; return t.length > 18 ? `"${t.substring(0, 18)}…"` : `"${t}"`; }
    if (data.type === 'Sequence') return `wait ${data.wait_time ?? '0.5'}s`;
    if (data.type === 'AnimationGroup') return `lag:${data.lag_ratio ?? '0'} ${data.run_time ?? '1.0'}s`;
    if (['Line', 'Arrow'].includes(data.type)) return `${data.start || '[-2,0,0]'}→${data.end || '[2,0,0]'}`;
    if (isAnimation && data.run_time) return `${data.run_time}s`;
    if (isCamera && data.run_time) return `${data.run_time}s`;
    if (isShape && data.position) return data.position;
    return data.type;
  };

  // Render handles (shared between collapsed and normal/expanded)
  const renderInputHandles = () =>
    hasVisibleInputs &&
    Object.entries(visibleInputs).map(([name, type], index) => {
      const isSequenceAnimInput = data.type === 'Sequence' && (type === 'Animation' || type === 'animation');
      const handleStyle = isSequenceAnimInput
        ? {
            background: '#A855F7',
            width: '12px',
            height: '14px',
            borderRadius: '0',
            border: 'none',
            clipPath: 'polygon(100% 0%, 0% 50%, 100% 100%)',
          }
        : getHandleStyle(type as string, false);
      const topPosition = ((index + 1) / (Object.keys(visibleInputs).length + 1)) * 100;
      const label = funcCallLabels?.[name] || (name.startsWith('param_') ? name.replace('param_', '') : null);
      return (
        <div key={name} style={{ position: 'absolute', left: '-8px', top: `${topPosition}%`, transform: 'translateY(-50%)' }}>
          <Handle
            type="target"
            position={Position.Left}
            id={name}
            style={{ ...handleStyle, position: 'relative', left: 0, top: 0, transform: 'none' }}
            title={`${label || name} (${type})`}
          />
          {viewMode !== 'collapsed' && label && (
            <div
              className="text-[9px] text-gray-400 absolute whitespace-nowrap"
              style={{ right: '18px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none' }}
            >
              {label}
            </div>
          )}
        </div>
      );
    });

  const renderOutputHandles = () =>
    hasOutputs &&
    Object.entries(visibleOutputs).map(([name, type], index) => {
      const topPosition = ((index + 1) / (Object.keys(visibleOutputs).length + 1)) * 100;
      const outLabel = funcCallLabels?.[name] || name;
      return (
        <div key={name} style={{ position: 'absolute', right: '-8px', top: `${topPosition}%`, transform: 'translateY(-50%)' }}>
          <Handle
            type="source"
            position={Position.Right}
            id={name}
            style={{ ...getHandleStyle(type as string, true), position: 'relative', right: 0, top: 0, transform: 'none' }}
            title={`${outLabel} (${type})`}
          />
          {viewMode !== 'collapsed' && (
            <div
              className="text-[9px] text-gray-400 absolute whitespace-nowrap"
              style={{ left: '18px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none' }}
            >
              {outLabel}
            </div>
          )}
        </div>
      );
    });

  // ── Junction: tiny circle pass-through ──
  if (data.type === 'Junction') {
    const outEdges = getEdges().filter((e: any) => e.source === id);
    const outCount = outEdges.length;
    return (
      <div
        className={`
          w-6 h-6 rounded-full bg-gray-600 border-2
          ${data.error ? 'border-red-500' : selected ? 'border-blue-400' : 'border-gray-500'}
          flex items-center justify-center relative
        `}
        title={`Junction (${outCount} out)`}
      >
        <Handle
          type="target"
          position={Position.Left}
          id="in"
          style={{
            width: '8px', height: '8px', background: '#9CA3AF',
            borderRadius: '50%', border: '1.5px solid #1e293b',
            left: '-5px', top: '50%',
          }}
        />
        <Handle
          type="source"
          position={Position.Right}
          id="out"
          style={{
            width: '8px', height: '8px', background: '#9CA3AF',
            borderRadius: '50%', border: '1.5px solid #1e293b',
            right: '-5px', top: '50%',
          }}
        />
        {outCount > 1 && (
          <div
            className="absolute -top-2.5 -right-2.5 bg-blue-500 text-white text-[8px] font-bold rounded-full w-3.5 h-3.5 flex items-center justify-center"
            style={{ pointerEvents: 'none' }}
          >
            {outCount}
          </div>
        )}
      </div>
    );
  }

  return (
    <div
      ref={nodeRef}
      className={`
        px-3 py-2 rounded-lg border-2 ${bgColor}
        ${data.error ? 'border-red-500 ring-2 ring-red-500/50' : borderColor}
        w-[210px] ${viewMode === 'collapsed' ? '' : 'min-h-[105px]'} flex flex-col
      `}
    >
      {renderInputHandles()}

      {viewMode === 'collapsed' ? (
        /* ── Collapsed: single line ── */
        <div className="flex items-center gap-1.5">
          {hasColorField && (
            <div className="w-3 h-3 rounded-sm flex-shrink-0 border border-gray-600" style={{ background: nodeColor }} />
          )}
          {data.type === 'Color' && (
            <div className="w-3 h-3 rounded-sm flex-shrink-0 border border-gray-600" style={{ background: colorPreview }} />
          )}
          <span className="text-[10px] font-semibold text-white truncate font-mono flex-1 min-w-0">
            {data.name || data.type}
          </span>
          <span className="text-[9px] text-gray-400 truncate flex-shrink-0 max-w-[80px] font-mono">
            {getCollapsedSummary()}
          </span>
          <button
            onClick={() => changeViewMode('normal')}
            className="p-0.5 hover:bg-gray-700 rounded transition-colors flex-shrink-0"
            title="Expand"
          >
            <ChevronDown size={12} className="text-gray-400" />
          </button>
        </div>
      ) : (
        /* ── Normal / Expanded view ── */
        <>
          {/* Row 1: Name + type */}
          <div className="flex items-center justify-between gap-1">
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
                  className="text-xs font-semibold text-white bg-gray-700 border border-gray-500 rounded px-1 py-0 w-full font-mono outline-none"
                />
              ) : (
                <div
                  className="text-xs font-semibold text-white truncate cursor-pointer font-mono"
                  onDoubleClick={() => {
                    setNameInput(data.name || '');
                    setEditingName(true);
                  }}
                  title="Double-click to rename"
                >
                  {data.name || data.type}
                </div>
              )}
            </div>
            <span className="text-[9px] text-gray-500 flex-shrink-0">{data.type}</span>
          </div>

          {/* Row 2: Quick info strip */}
          <div className="flex items-center gap-1.5 mt-1">
            {hasColorField && (
              <input
                type="color"
                value={nodeColor}
                onChange={(e) => updateNodeData('color', e.target.value)}
                onMouseDown={(e) => e.stopPropagation()}
                onPointerDown={(e) => e.stopPropagation()}
                className="w-5 h-5 rounded border border-gray-600 flex-shrink-0 cursor-pointer p-0"
                style={{ background: nodeColor }}
                title="Color"
              />
            )}

            {data.type === 'Color' && (
              <input
                type="color"
                value={colorPreview}
                onChange={(e) => updateNodeData('color_value', e.target.value)}
                onMouseDown={(e) => e.stopPropagation()}
                onPointerDown={(e) => e.stopPropagation()}
                className="w-5 h-5 rounded border border-gray-600 flex-shrink-0 cursor-pointer p-0"
                style={{ background: colorPreview }}
                title="Color value"
              />
            )}

            {hasPresentField && presentMode !== 'none' && (
              <span className="text-[9px] text-purple-300 bg-purple-900/40 px-1 rounded" title="Presentation mode">
                {presentMode}
              </span>
            )}

            {isAnimation && data.animate !== undefined && (
              <label className="flex items-center gap-0.5 cursor-pointer" title="Animate or apply instantly">
                <input type="checkbox" checked={data.animate ?? true}
                  onChange={(e) => updateNodeData('animate', e.target.checked)} className="w-3 h-3" />
                <span className="text-[9px] text-gray-400">anim</span>
              </label>
            )}
            {isAnimation && data.copy !== undefined && (
              <label className="flex items-center gap-0.5 cursor-pointer" title="Animate a copy">
                <input type="checkbox" checked={data.copy || false}
                  onChange={(e) => updateNodeData('copy', e.target.checked)} className="w-3 h-3" />
                <span className="text-[9px] text-gray-400">cp</span>
              </label>
            )}

            {data.write_label !== undefined && (
              <label className="flex items-center gap-0.5 cursor-pointer" title="Auto-add label to scene">
                <input type="checkbox" checked={data.write_label || false}
                  onChange={(e) => updateNodeData('write_label', e.target.checked)} className="w-3 h-3" />
                <span className="text-[9px] text-gray-400">lbl</span>
              </label>
            )}

            {data.order !== undefined && data.order !== 0 && (
              <div className="px-1.5 py-0 bg-blue-500/60 text-white text-[9px] font-bold rounded-full" title="Creation order">
                #{data.order}
              </div>
            )}

            <div className="flex-1" />

            {/* Collapse to one-liner */}
            <button
              onClick={() => changeViewMode('collapsed')}
              className="p-0.5 hover:bg-gray-700 rounded transition-colors"
              title="Collapse to one line"
            >
              <ChevronUp size={14} className="text-gray-400" />
            </button>

            {/* Expand/collapse params */}
            {hasParameters && (
              <button
                onClick={() => changeViewMode(viewMode === 'expanded' ? 'normal' : 'expanded')}
                className="p-0.5 hover:bg-gray-700 rounded transition-colors"
                title={viewMode === 'expanded' ? "Hide parameters" : "Show parameters"}
              >
                {viewMode === 'expanded' ? (
                  <ChevronUp size={14} className="text-gray-500" />
                ) : (
                  <ChevronDown size={14} className="text-gray-400" />
                )}
              </button>
            )}
          </div>

          {/* Row 3: Key info line */}
          <div className="text-[10px] text-gray-400 truncate mt-1">
            {isShape && data.position && (
              <span title="Position">{data.position}</span>
            )}
            {['Line', 'Arrow'].includes(data.type) && (
              <span title="Start → End">{data.start || '[-2,0,0]'} → {data.end || '[2,0,0]'}</span>
            )}
            {(data.type === 'Text' || data.type === 'MathTex') && (
              <span className="italic" title={data.text || data.tex || ''}>
                {(() => {
                  const t = data.text || data.tex || '';
                  return t.length > 25 ? `"${t.substring(0, 25)}…"` : `"${t}"`;
                })()}
              </span>
            )}
            {isAnimation && data.run_time && (
              <span>{data.run_time}s</span>
            )}
            {isCamera && data.run_time && (
              <span>{data.run_time}s</span>
            )}
            {data.type === 'Vec3' && (
              <span className="font-mono">{data.values || '0, 0, 0'}</span>
            )}
            {data.type === 'Number' && (
              <span className="font-mono">= {data.value ?? '0'}</span>
            )}
            {data.type === 'Color' && (
              <span className="font-mono">{colorPreview}</span>
            )}
            {data.type === 'Sequence' && (
              <span>wait: {data.wait_time ?? '0.5'}s</span>
            )}
            {data.type === 'AnimationGroup' && (
              <span>lag: {data.lag_ratio ?? '0'}, {data.run_time ?? '1.0'}s</span>
            )}
          </div>

          {/* Error indicator */}
          {data.error && (
            <div className="text-[10px] text-red-400 mt-0.5 truncate" title={data.error}>
              Error
            </div>
          )}

          {/* Debug output */}
          {data.debugOutput && (
            <div className="text-[10px] text-yellow-400 mt-0.5 truncate font-mono bg-yellow-900/20 px-1 rounded" title={data.debugOutput}>
              {data.debugOutput}
            </div>
          )}

          {/* Expandable parameters */}
          {viewMode === 'expanded' && (
            <div className="mt-1.5 space-y-1.5 border-t border-gray-700/50 pt-1.5">
              {data.type === 'Matrix' && (
                <div className="mb-2">
                  <label className="text-[9px] text-gray-400 mb-1 block">Matrix 4x4</label>
                  <div className="grid grid-cols-4 gap-1">
                    {['m11', 'm12', 'm13', 'm14',
                      'm21', 'm22', 'm23', 'm24',
                      'm31', 'm32', 'm33', 'm34',
                      'm41', 'm42', 'm43', 'm44'].map((key) => (
                      <input
                        key={key}
                        type="text"
                        value={data[key] ?? '0'}
                        onChange={(e) => updateNodeData(key, e.target.value)}
                        className="w-10 px-1 py-0.5 text-[10px] bg-gray-700 border border-gray-600 rounded text-white text-center font-mono"
                      />
                    ))}
                  </div>
                </div>
              )}

              {Object.entries(data).map(([key, value]) => {
                if (['type', 'category', 'inputs', 'outputs', 'error', 'label', 'name', 'copy', 'animate', 'write_label', 'present', 'present_run_time', 'viewMode', 'debugOutput'].includes(key)) {
                  return null;
                }
                if (data.type === 'Matrix' && key.startsWith('m') && key.length === 3) return null;
                if (data.type === 'Transform' && key.startsWith('m') && key.length === 3) return null;
                if (data.type === 'ExposeParameters' && key.startsWith('param_')) return null;

                const isBoolean = typeof value === 'boolean';
                const isColor = key.includes('color') || key.includes('Color');

                return (
                  <div key={key} className="flex items-center gap-1.5">
                    <label className="text-[9px] text-gray-400 capitalize whitespace-nowrap w-14 text-right flex-shrink-0">
                      {key.replace(/_/g, ' ')}
                    </label>
                    {isBoolean ? (
                      <input
                        type="checkbox"
                        checked={value as boolean}
                        onChange={(e) => updateNodeData(key, e.target.checked)}
                        className="w-3.5 h-3.5"
                      />
                    ) : isColor ? (
                      <input
                        type="color"
                        value={value as string}
                        onChange={(e) => updateNodeData(key, e.target.value)}
                        className="w-full h-5 rounded border border-gray-600 bg-gray-700"
                      />
                    ) : (
                      <input
                        type="text"
                        value={value as string}
                        onChange={(e) => updateNodeData(key, e.target.value)}
                        className="flex-1 min-w-0 px-1.5 py-0.5 text-[10px] bg-gray-700 border border-gray-600 rounded text-white font-mono"
                      />
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </>
      )}

      {renderOutputHandles()}
    </div>
  );
}

export default memo(CustomNode);
