import { useEffect } from 'react';
import { ReactFlowProvider } from 'reactflow';
import NodeEditor from './components/NodeEditor/NodeEditor';
import NodePalette from './components/NodePalette/NodePalette';
import AnimationPreview from './components/AnimationPreview/Preview';
import PropertyInspector from './components/PropertyInspector/Inspector';
import CodeViewer from './components/CodeViewer/CodeViewer';
import JsonViewer from './components/JsonViewer/JsonViewer';
import ErrorPanel from './components/ErrorPanel/ErrorPanel';
import DebugPanel from './components/DebugPanel/DebugPanel';
import TopBar from './components/TopBar/TopBar';
import { useGraphStore } from './store/useGraphStore';
import { useUIStore } from './store/useUIStore';
import 'reactflow/dist/style.css';

function App() {
  const createNewGraph = useGraphStore((state) => state.createNewGraph);
  const showNodePalette = useUIStore((state) => state.showNodePalette);
  const showPreview = useUIStore((state) => state.showPreview);
  const showPropertyInspector = useUIStore((state) => state.showPropertyInspector);
  const mainView = useUIStore((state) => state.mainView);
  const showDebugPanel = useUIStore((state) => state.showDebugPanel);

  useEffect(() => {
    // Create a new graph on mount
    createNewGraph();
  }, [createNewGraph]);

  return (
    <ReactFlowProvider>
      <div className="flex flex-col h-screen w-screen bg-gray-900">
        <TopBar />

        <div className="flex flex-1 overflow-hidden">
          {/* Node Palette - only shown on canvas view */}
          {showNodePalette && mainView === 'canvas' && (
            <div className="w-64 border-r border-gray-700 bg-gray-800">
              <NodePalette />
            </div>
          )}

          {/* Main Editor / Code Viewer */}
          <div className="flex-1 relative flex flex-col min-w-0">
            <div className="flex-1 relative min-h-0 min-w-0">
              {/* Keep NodeEditor always mounted to preserve viewport state */}
              <div className={`absolute inset-0 ${mainView === 'canvas' ? 'z-10' : 'z-0 opacity-0 pointer-events-none'}`}>
                <NodeEditor />
              </div>
              {mainView !== 'canvas' && (
                <div className="absolute inset-0 z-20">
                  {mainView === 'code' && <CodeViewer />}
                  {mainView === 'json' && <JsonViewer />}
                  {mainView === 'error' && <ErrorPanel />}
                </div>
              )}
            </div>
            {showDebugPanel && <DebugPanel />}
          </div>

          {/* Right Sidebar - hidden when viewing Code/JSON/Errors */}
          {mainView === 'canvas' && (
            <div className="w-96 border-l border-gray-700 bg-gray-800 flex flex-col">
              {/* Property Inspector */}
              {showPropertyInspector && (
                <div className="flex-1 border-b border-gray-700 overflow-y-auto">
                  <PropertyInspector />
                </div>
              )}

              {/* Preview */}
              {showPreview && (
                <div className="h-80 overflow-hidden">
                  <AnimationPreview />
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </ReactFlowProvider>
  );
}

export default App;
