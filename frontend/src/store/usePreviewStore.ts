import { create } from 'zustand';

interface PreviewStore {
  // State
  isRendering: boolean;
  videoUrl: string | null;
  error: string | null;
  log: string[];
  generatedCode: string | null;

  // Playback state
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  playbackSpeed: number;

  // Actions
  setRendering: (rendering: boolean) => void;
  setVideoUrl: (url: string | null) => void;
  setError: (error: string | null) => void;
  addLog: (message: string) => void;
  clearLog: () => void;
  setGeneratedCode: (code: string | null) => void;
  setPlaying: (playing: boolean) => void;
  setCurrentTime: (time: number) => void;
  setDuration: (duration: number) => void;
  setPlaybackSpeed: (speed: number) => void;
  reset: () => void;
}

export const usePreviewStore = create<PreviewStore>((set) => ({
  isRendering: false,
  videoUrl: null,
  error: null,
  log: [],
  generatedCode: null,
  isPlaying: false,
  currentTime: 0,
  duration: 0,
  playbackSpeed: 1.0,

  setRendering: (rendering) => set({ isRendering: rendering }),
  setVideoUrl: (url) => set({ videoUrl: url }),
  setError: (error) => set({ error }),
  addLog: (message) => set((state) => ({ log: [...state.log, message] })),
  clearLog: () => set({ log: [] }),
  setGeneratedCode: (code) => set({ generatedCode: code }),
  setPlaying: (playing) => set({ isPlaying: playing }),
  setCurrentTime: (time) => set({ currentTime: time }),
  setDuration: (duration) => set({ duration }),
  setPlaybackSpeed: (speed) => set({ playbackSpeed: speed }),
  reset: () =>
    set({
      isRendering: false,
      videoUrl: null,
      error: null,
      log: [],
      generatedCode: null,
      isPlaying: false,
      currentTime: 0,
    }),
}));
