// API client using Vite runtime env (import.meta.env.VITE_API_URL).
// If VITE_API_URL is unset the client will use relative paths which work with
// the dev proxy (vite) or when the frontend is served from the same origin
// as the backend in production.
const API_BASE = (import.meta.env.VITE_API_URL as string) || '';

async function request(method: string, path: string, body?: any) {
  const url = API_BASE ? `${API_BASE}${path}` : path;
  const opts: RequestInit = { method, headers: { 'Content-Type': 'application/json' } };
  if (body !== undefined) opts.body = JSON.stringify(body);
  const res = await fetch(url, opts);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export function runSimulation(scenario?: object) {
  return request('POST', '/simulate/run', scenario || {});
}

export function generatePatch(attackLog: any, currentRule: any) {
  return request('POST', '/ai/blue_team', { attack_log: attackLog, current_rule: currentRule });
}

export function applyPatch(patch: any) {
  return request('POST', '/simulate/apply_patch', patch);
}

export function getLogs() {
  return request('GET', '/simulate/logs');
}
