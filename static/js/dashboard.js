// Dashboard page logic
// Requires: window.categoryOptions, window.csrfToken (set inline by template)

const mediaTypeSelect = document.getElementById('media-type');
const fileList = document.getElementById('file-list');
const breadcrumb = document.getElementById('breadcrumb');
const selectedCount = document.getElementById('selected-count');
const selected = new Map();

let currentPath = '';
let currentDefaultCategory = null;

function csrfHeaders() {
  return window.csrfToken ? { 'X-CSRFToken': window.csrfToken } : {};
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text || '';
  return div.innerHTML;
}

function clearSelections() {
  selected.clear();
  selectedCount.textContent = '0 selected';
}

function updateSelectedCount() {
  selectedCount.textContent = `${selected.size} selected`;
}

function makeBreadcrumb(root, path, parent) {
  breadcrumb.innerHTML = '';
  const rootBtn = document.createElement('button');
  rootBtn.className = 'btn btn-ghost btn-sm';
  rootBtn.textContent = root.split('/').pop() || root;
  rootBtn.onclick = () => browse('');
  breadcrumb.appendChild(rootBtn);

  if (parent) {
    const upBtn = document.createElement('button');
    upBtn.className = 'btn btn-ghost btn-sm';
    upBtn.textContent = '.. (up)';
    upBtn.onclick = () => browse(parent);
    breadcrumb.appendChild(upBtn);
  }

  const pathBadge = document.createElement('span');
  pathBadge.className = 'badge';
  pathBadge.textContent = path;
  breadcrumb.appendChild(pathBadge);
}

async function browse(path = '') {
  clearSelections();
  const mediaType = mediaTypeSelect.value;
  const response = await fetch(`/api/browse?media_type=${encodeURIComponent(mediaType)}&path=${encodeURIComponent(path)}`);
  const data = await response.json();
  if (data.error) {
    alert(data.error);
    return;
  }
  currentPath = data.path;
  currentDefaultCategory = data.default_category;
  makeBreadcrumb(data.root || data.path, data.path, data.parent);
  fileList.innerHTML = '';
  data.items.forEach(item => {
    const row = document.createElement('div');
    row.className = 'file-item';
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.onchange = () => {
      if (checkbox.checked) {
        selected.set(item.path, item);
      } else {
        selected.delete(item.path);
      }
      updateSelectedCount();
    };
    const name = document.createElement('div');
    name.className = 'file-name-text';
    name.textContent = item.name;
    name.title = item.path;
    name.onclick = () => {
      if (item.is_dir) {
        browse(item.path);
      }
    };
    const size = document.createElement('div');
    size.className = 'text-muted text-sm';
    size.textContent = item.size;
    row.appendChild(checkbox);
    row.appendChild(name);
    row.appendChild(size);
    fileList.appendChild(row);
  });
}

async function addQueue() {
  if (!selected.size) return;
  const mediaType = mediaTypeSelect.value;
  const items = Array.from(selected.values()).map(item => {
    const defaultCategory = currentDefaultCategory || window.categoryOptions[mediaType][0].id;
    return {
      media_type: mediaType,
      path: item.path,
      category: defaultCategory,
    };
  });

  const res = await fetch('/api/queue/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...csrfHeaders() },
    body: JSON.stringify({ items })
  });
  const data = await res.json();
  if (!data.success) {
    alert(data.error || 'Failed to add queue');
    return;
  }
  clearSelections();
  await loadQueue();
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

document.getElementById('refresh').onclick = () => browse(currentPath);
document.getElementById('add-queue').onclick = addQueue;
document.getElementById('reload-queue').onclick = loadQueue;
mediaTypeSelect.onchange = () => browse('');

browse('');
loadQueue();
loadStats();
checkActivityHealth();
renderMonthlyChart();
setInterval(loadStats, 30000);
setInterval(checkActivityHealth, 60000);
