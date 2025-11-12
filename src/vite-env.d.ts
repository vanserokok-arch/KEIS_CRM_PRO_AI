/// <reference types="vite/client" />

// Vite build-time env typing
interface ImportMetaEnv {
  readonly VITE_API_BASE?: string;
}
interface ImportMeta {
  readonly env: ImportMetaEnv;
}

// Runtime config from /env.js
declare global {
  interface Window {
    __ENV__?: {
      API_BASE?: string;
    };
  }
}

export {};