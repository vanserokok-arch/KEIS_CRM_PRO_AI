import axios from "axios";

// Resolve API base URL in this order:
// 1) runtime window.__ENV__.API_BASE (from /env.js)
// 2) Vite build-time env (VITE_API_BASE)
// 3) fallback to "/api"
const runtimeBase =
  (globalThis as any)?.__ENV__?.API_BASE as string | undefined;

// Vite injects import.meta.env at build time
const viteBase = (
  typeof import.meta !== "undefined" &&
  (import.meta as any)?.env?.VITE_API_BASE
) as string | undefined;

const rawBase = runtimeBase || viteBase || "/api";
// Avoid double "/api" if requests already start with "/api"
const baseURL = rawBase === "/api" ? "" : rawBase;

export const api = axios.create({ baseURL });