// Dashboard page logic
// Requires: window.categoryOptions, window.csrfToken (set inline by template)

function csrfHeaders() {
  return window.csrfToken ? { 'X-CSRFToken': window.csrfToken } : {};
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text || '';
  return div.innerHTML;
}

function statusBadge(status) {
  const map = { queued: '', preparing: 'badge-info', uploading: 'badge-info', success: 'badge-success', failed: 'badge-error', duplicate: 'badge-warning' };
  return `<span class="badge ${map[status] || ''}">${escapeHtml(status)}</span>`;
}

function categorySelect(mediaType, value) {
  const options = window.categoryOptions[mediaType]
    .map(o => `<option value="${o.id}" ${o.id === value ? 'selected' : ''}>${o.label}</option>`)
    .join('');
  return `<select data-field="category">${options}</select>`;
}

async function updateQueueRow(id, row) {
  const releaseName = row.querySelector('input[data-field="release_name"]').value;
  const category = row.querySelector('select[data-field="category"]').value;
  const tags = row.querySelector('input[data-field="tags"]').value;

  await fetch('/api/queue/update', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...csrfHeaders() },
    body: JSON.stringify({ id, release_name: releaseName, category, tags })
  });
  await loadQueue();
}

async function deleteQueueRow(id) {
  await fetch('/api/queue/delete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...csrfHeaders() },
    body: JSON.stringify({ id })
  });
  await loadQueue();
}

async function loadQueue() {
  const res = await fetch('/api/queue');
  const rows = await res.json();
  const tbody = document.querySelector('#queue-table tbody');
  tbody.innerHTML = '';
  rows.forEach(item => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${escapeHtml(String(item.id))}</td>
      <td>${escapeHtml(item.media_type)}</td>
      <td><input data-field="release_name" value="${escapeHtml(item.release_name)}" /></td>
      <td>${categorySelect(item.media_type, item.category)}</td>
      <td><input data-field="tags" value="${escapeHtml(item.tags || '')}" placeholder="tag1,tag2" /></td>
      <td>${statusBadge(item.status)}</td>
      <td>${escapeHtml(item.message || '')}</td>
      <td class="table-actions">
        <button class="btn btn-ghost btn-sm" data-action="save">Save</button>
        <button class="btn btn-ghost btn-sm" data-action="delete">Del</button>
      </td>
    `;
    tr.querySelector('button[data-action="save"]').onclick = () => updateQueueRow(item.id, tr);
    tr.querySelector('button[data-action="delete"]').onclick = () => deleteQueueRow(item.id);
    tbody.appendChild(tr);
  });
}

async function loadStats() {
  try {
    const res = await fetch('/api/stats');
    const data = await res.json();
    const summary = document.getElementById('stats-summary');

    summary.innerHTML = `
      <div class="grid grid-cols-3 gap-6">
        <div class="card stat-card">
          <div class="stat-label">Queue</div>
          <div class="stat-value">${data.queue_total}</div>
          <div class="text-muted text-sm">${data.queue_pending} pending</div>
        </div>
        <div class="card stat-card">
          <div class="stat-label">Automation</div>
          <div class="stat-value" style="color: ${data.auto_enabled ? 'var(--color-success-foreground)' : 'var(--color-text-muted)'}">
            ${data.auto_enabled ? 'On' : 'Off'}
          </div>
          <div class="text-muted text-sm">Interval: ${data.auto_interval}m</div>
        </div>
        <div class="card stat-card">
          <div class="stat-label">Last Music Scan</div>
          <div class="stat-value" style="font-size: var(--font-size-lg);">${data.last_music_scan || 'Never'}</div>
        </div>
      </div>
    `;
  } catch (err) {
    console.error('Failed to load stats:', err);
  }
}

async function checkActivityHealth() {
  try {
    const res = await fetch('/api/activity/health');
    const h = await res.json();
    const banner = document.getElementById('activity-banner');
    const text = document.getElementById('activity-banner-text');
    if (h.critical) {
      let msg = `Projected uploads: ${h.projected} / ${h.minimum}. Need ${h.needed} more in ${h.days_remaining} days.`;
      if (h.pace !== null) msg += ` Pace: ${h.pace}/day.`;
      text.textContent = msg;
      banner.style.display = 'block';
    } else {
      banner.style.display = 'none';
    }
  } catch (err) {
    console.error('Activity health check failed:', err);
  }
}

async function renderMonthlyChart() {
  try {
    const res = await fetch('/api/activity/history?months=6');
    const data = await res.json();
    const container = document.getElementById('chart-bars');
    const chartCard = document.getElementById('monthly-chart');
    if (!data || data.length === 0) return;
    chartCard.style.display = 'block';
    const maxCount = Math.max(...data.map(d => d.count), 1);
    container.innerHTML = data.map(d => {
      const pct = Math.max((d.count / maxCount) * 100, 4);
      const label = d.month.slice(5);
      return `<div style="flex:1; text-align:center;">
        <div style="background:var(--color-accent); height:${pct}%; min-height:4px; border-radius:var(--radius-sm) var(--radius-sm) 0 0;"></div>
        <div class="text-muted text-sm" style="margin-top:var(--space-1);">${d.count}</div>
        <div class="text-muted text-sm">${label}</div>
      </div>`;
    }).join('');
  } catch (err) {
    console.error('Monthly chart failed:', err);
  }
}

document.getElementById('reload-queue').onclick = loadQueue;

loadQueue();
loadStats();
checkActivityHealth();
renderMonthlyChart();
setInterval(loadStats, 30000);
setInterval(checkActivityHealth, 60000);
