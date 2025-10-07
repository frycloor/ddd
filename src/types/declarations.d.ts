declare module 'vite' {
  export function defineConfig(config: any): any;
  export function loadEnv(mode: string, root: string, prefix?: string): any;
}

declare module '@vitejs/plugin-react' {
  const plugin: any;
  export default plugin;
}

declare module 'react' {
  import type { ComponentType } from 'react';
  const React: any;
  export default React;
  export const useState: any;
  export const useEffect: any;
  export const useCallback: any;
  export const useRef: any;
  export const Suspense: any;
  export type FC<T = {}> = ComponentType<T>;
}

declare module 'react/jsx-runtime' {
  export function jsx(...args: any[]): any;
  export function jsxs(...args: any[]): any;
  export function jsxDEV(...args: any[]): any;
}

declare module 'path' {
  export function resolve(...parts: string[]): string;
}
