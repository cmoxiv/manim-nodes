import { memo, useState, useCallback, useRef } from 'react';
import { NodeProps, useReactFlow } from 'reactflow';

function GroupFrameNode({ data, id, selected }: NodeProps) {
  const { setNodes } = useReactFlow();
  const [editingTitle, setEditingTitle] = useState(false);
  const [titleInput, setTitleInput] = useState(data.label || 'Frame');
  const resizingRef = useRef(false);
  const startRef = useRef({ x: 0, y: 0, w: 0, h: 0 });

  const updateLabel = useCallback(
    (value: string) => {
      setNodes((nodes) =>
        nodes.map((n) =>
          n.id === id ? { ...n, data: { ...n.data, label: value || 'Frame' } } : n
        )
      );
    },
    [id, setNodes]
  );

  const handleResizeStart = useCallback(
    (e: React.MouseEvent) => {
      e.stopPropagation();
      e.preventDefault();
      resizingRef.current = true;
      const w = data.width || 400;
      const h = data.height || 300;
      startRef.current = { x: e.clientX, y: e.clientY, w, h };

      const handleMouseMove = (ev: MouseEvent) => {
        if (!resizingRef.current) return;
        const dx = ev.clientX - startRef.current.x;
        const dy = ev.clientY - startRef.current.y;
        const snap = 15;
        const newW = Math.max(200, Math.round((startRef.current.w + dx) / snap) * snap);
        const newH = Math.max(150, Math.round((startRef.current.h + dy) / snap) * snap);
        setNodes((nodes) =>
          nodes.map((n) =>
            n.id === id
              ? {
                  ...n,
                  style: { ...n.style, width: newW, height: newH },
                  data: { ...n.data, width: newW, height: newH },
                }
              : n
          )
        );
      };

      const handleMouseUp = () => {
        resizingRef.current = false;
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };

      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    },
    [id, data.width, data.height, setNodes]
  );

  return (
    <div
      className="relative w-full h-full"
      style={{ minWidth: 200, minHeight: 150 }}
    >
      <div
        className={`w-full h-full rounded-lg border-2 border-dashed ${
          selected ? 'border-blue-400 bg-blue-500/10' : 'border-gray-600 bg-gray-800/30'
        }`}
      >
        {/* Title bar */}
        <div className="px-3 py-1.5 border-b border-dashed border-inherit">
          {editingTitle ? (
            <input
              type="text"
              value={titleInput}
              onChange={(e) => setTitleInput(e.target.value)}
              onBlur={() => {
                updateLabel(titleInput);
                setEditingTitle(false);
              }}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  updateLabel(titleInput);
                  setEditingTitle(false);
                }
                if (e.key === 'Escape') {
                  setTitleInput(data.label || 'Frame');
                  setEditingTitle(false);
                }
              }}
              autoFocus
              className="text-sm font-semibold text-white bg-gray-700 border border-gray-500 rounded px-1 py-0 w-full outline-none"
            />
          ) : (
            <div
              className="text-sm font-semibold text-gray-300 cursor-pointer select-none"
              onDoubleClick={() => {
                setTitleInput(data.label || 'Frame');
                setEditingTitle(true);
              }}
              title="Double-click to rename"
            >
              {data.label || 'Frame'}
            </div>
          )}
        </div>
      </div>

      {/* Resize handle */}
      <div
        className="nodrag absolute bottom-0 right-0 w-4 h-4 cursor-nwse-resize"
        onMouseDown={handleResizeStart}
      >
        <svg
          width="12"
          height="12"
          viewBox="0 0 12 12"
          className="text-gray-500 absolute bottom-0.5 right-0.5"
        >
          <path d="M11 1L1 11M11 5L5 11M11 9L9 11" stroke="currentColor" strokeWidth="1.5" />
        </svg>
      </div>
    </div>
  );
}

export default memo(GroupFrameNode);
