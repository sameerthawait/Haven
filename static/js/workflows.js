// Minimal UI stub for Actionable Workflows (MVP)
export function initWorkflows(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const input = document.createElement('input');
  input.placeholder = 'Describe the task (e.g. "schedule meeting")';
  const planBtn = document.createElement('button');
  planBtn.textContent = 'Generate Plan';
  const execBtn = document.createElement('button');
  execBtn.textContent = 'Execute (approve)';
  const out = document.createElement('pre');

  planBtn.addEventListener('click', async () => {
    const task = input.value || 'quick task';
    const res = await fetch('/api/workflows/plan', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({task})});
    const json = await res.json();
    out.textContent = JSON.stringify(json, null, 2);
  });

  execBtn.addEventListener('click', async () => {
    const res = await fetch('/api/workflows/execute', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({approved:true})});
    const json = await res.json();
    out.textContent = JSON.stringify(json, null, 2);
  });

  container.appendChild(input);
  container.appendChild(planBtn);
  container.appendChild(execBtn);
  container.appendChild(out);
}
