// Minimal UI stub for Collaboration (MVP)
export function initCollab(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const createBtn = document.createElement('button');
  createBtn.textContent = 'Create Collab Session';
  const out = document.createElement('pre');

  createBtn.addEventListener('click', async () => {
    createBtn.disabled = true;
    const res = await fetch('/api/collab/session', {method:'POST'});
    const json = await res.json();
    out.textContent = JSON.stringify(json, null, 2);
    createBtn.disabled = false;
  });

  container.appendChild(createBtn);
  container.appendChild(out);
}
