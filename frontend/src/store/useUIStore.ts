import { create } from 'zustand';

interface UIStore {
  // State
  selectedNodeId: string | null;
  showNodePalette: boolean;
  showPreview: boolean;
  showPropertyInspector: boolean;
  mainView: 'canvas' | 'code' | 'json' | 'error';

  // Actions
  setSelectedNode: (id: string | null) => void;
  toggleNodePalette: () => void;
  togglePreview: () => void;
  togglePropertyInspector: () => void;
  setShowNodePalette: (show: boolean) => void;
  setShowPreview: (show: boolean) => void;
  setShowPropertyInspector: (show: boolean) => void;
  setMainView: (view: 'canvas' | 'code' | 'json' | 'error') => void;
  toggleMainView: () => void;
}

export const useUIStore = create<UIStore>((set) => ({
  selectedNodeId: null,
  showNodePalette: true,
  showPreview: true,
  showPropertyInspector: true,
  mainView: 'canvas',

  setSelectedNode: (id) => set({ selectedNodeId: id }),
  toggleNodePalette: () => set((state) => ({ showNodePalette: !state.showNodePalette })),
  togglePreview: () => set((state) => ({ showPreview: !state.showPreview })),
  togglePropertyInspector: () =>
    set((state) => ({ showPropertyInspector: !state.showPropertyInspector })),
  setShowNodePalette: (show) => set({ showNodePalette: show }),
  setShowPreview: (show) => set({ showPreview: show }),
  setShowPropertyInspector: (show) => set({ showPropertyInspector: show }),
  setMainView: (view) => set({ mainView: view }),
  toggleMainView: () => set((state) => ({ mainView: state.mainView === 'canvas' ? 'code' : 'canvas' })),
}));
