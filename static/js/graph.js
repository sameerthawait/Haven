// Minimal UI stub for Concept Graph (MVP)
export function initConceptGraph(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const btn = document.createElement('button');
  btn.textContent = 'Load Concept Graph';
  btn.addEventListener('click', async () => {
    btn.disabled = true;
    btn.textContent = 'Loading...';
    try {
      const r = await fetch('/api/graph/concepts');
      const data = await r.json();
      container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    } catch (e) {
      container.textContent = 'Failed to load graph: ' + e;
    } finally {
      btn.disabled = false;
      btn.textContent = 'Load Concept Graph';
    }
  });
  container.appendChild(btn);
}
