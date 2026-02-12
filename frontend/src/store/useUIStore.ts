import { create } from 'zustand';

interface Viewport {
  x: number;
  y: number;
  zoom: number;
}

interface UIStore {
  // State
  selectedNodeId: string | null;
  showNodePalette: boolean;
  showPreview: boolean;
  showPropertyInspector: boolean;
  showDebugPanel: boolean;
  mainView: 'canvas' | 'code' | 'json' | 'error';
  viewport: Viewport | null;
  scrollToNodeId: string | null;

  // Actions
  setSelectedNode: (id: string | null) => void;
  toggleNodePalette: () => void;
  togglePreview: () => void;
  togglePropertyInspector: () => void;
  toggleDebugPanel: () => void;
  setShowNodePalette: (show: boolean) => void;
  setShowPreview: (show: boolean) => void;
  setShowPropertyInspector: (show: boolean) => void;
  setMainView: (view: 'canvas' | 'code' | 'json' | 'error') => void;
  toggleMainView: () => void;
  setViewport: (viewport: Viewport | null) => void;
  setScrollToNodeId: (id: string | null) => void;
}

export const useUIStore = create<UIStore>((set) => ({
  selectedNodeId: null,
  showNodePalette: true,
  showPreview: true,
  showPropertyInspector: true,
  showDebugPanel: false,
  mainView: 'canvas',
  viewport: null,
  scrollToNodeId: null,

  setSelectedNode: (id) => set({ selectedNodeId: id }),
  toggleNodePalette: () => set((state) => ({ showNodePalette: !state.showNodePalette })),
  togglePreview: () => set((state) => ({ showPreview: !state.showPreview })),
  togglePropertyInspector: () =>
    set((state) => ({ showPropertyInspector: !state.showPropertyInspector })),
  toggleDebugPanel: () =>
    set((state) => ({ showDebugPanel: !state.showDebugPanel })),
  setShowNodePalette: (show) => set({ showNodePalette: show }),
  setShowPreview: (show) => set({ showPreview: show }),
  setShowPropertyInspector: (show) => set({ showPropertyInspector: show }),
  setMainView: (view) => set({ mainView: view }),
  toggleMainView: () => set((state) => ({ mainView: state.mainView === 'canvas' ? 'code' : 'canvas' })),
  setViewport: (viewport) => set({ viewport }),
  setScrollToNodeId: (id) => set({ scrollToNodeId: id }),
}));
