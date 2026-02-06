// History page logic
// Requires: window.csrfToken, window.categoryOptions (set inline by template)

let currentTab = 'uploads';
let historyData = [];
let selectedItemId = null;

function csrfHeaders() {
  return window.csrfToken ? { 'X-CSRFToken': window.csrfToken } : {};
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text || '';
  return div.innerHTML;
}

function formatDate(dateStr) {
  if (!dateStr) return '--';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-CA');
}

function formatDateTime(dateStr) {
  if (!dateStr) return '--';
  const d = new Date(dateStr);
  return d.toLocaleString('en-CA', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
}

function getCategoryLabel(mediaType, categoryId) {
  const options = window.categoryOptions[mediaType] || [];
  const found = options.find(o => o.id === categoryId || o.id === String(categoryId));
  return found ? found.label : categoryId;
}

function statusBadge(status) {
  const normalized = (status || '').toLowerCase();
  const map = { success: 'badge-success', failed: 'badge-error', duplicate: 'badge-warning' };
  return `<span class="badge ${map[normalized] || ''}">${normalized || 'unknown'}</span>`;
}

function filterByDate(items, days) {
  if (days === 'all') return items;
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - parseInt(days, 10));
  return items.filter(item => {
    const itemDate = new Date(item.updated_at || item.created_at);
    return itemDate >= cutoff;
  });
}

function filterByStatus(items, status) {
  if (status === 'all') return items;
  return items.filter(item => item.status === status);
}

function filterByType(items, mediaType) {
  if (mediaType === 'all') return items;
  return items.filter(item => item.media_type === mediaType);
}

function applyFilters(items) {
  const statusFilter = document.getElementById('filter-status').value;
  const dateFilter = document.getElementById('filter-date').value;
  const typeFilter = document.getElementById('filter-type').value;

  let filtered = items;
  filtered = filterByStatus(filtered, statusFilter);
  filtered = filterByDate(filtered, dateFilter);
  filtered = filterByType(filtered, typeFilter);

  return filtered;
}

async function loadHistory() {
  try {
    const res = await fetch('/api/queue');
    const allItems = await res.json();

    historyData = allItems.filter(item =>
      ['success', 'failed', 'duplicate'].includes(item.status)
    );

    historyData.sort((a, b) => {
      const dateA = new Date(a.updated_at || a.created_at || 0);
      const dateB = new Date(b.updated_at || b.created_at || 0);
      return dateB - dateA;
    });

    renderHistory();
  } catch (err) {
    console.error('Failed to load history:', err);
  }
}

function renderHistory() {
  const tbody = document.getElementById('history-tbody');
  const emptyState = document.getElementById('empty-uploads');

  const filtered = applyFilters(historyData);

  if (filtered.length === 0) {
    tbody.innerHTML = '';
    emptyState.style.display = 'block';
    return;
  }

  emptyState.style.display = 'none';
  tbody.innerHTML = filtered.map(item => `
    <tr data-id="${item.id}" class="${selectedItemId === item.id ? 'selected' : ''}">
      <td>${formatDate(item.updated_at || item.created_at)}</td>
      <td class="release-name" title="${escapeHtml(item.release_name)}">${escapeHtml(item.release_name)}</td>
      <td>${statusBadge(item.status)}</td>
      <td class="tl-id ${item.tl_id ? '' : 'none'}">${item.tl_id ? '#' + item.tl_id : '--'}</td>
    </tr>
  `).join('');

  tbody.querySelectorAll('tr').forEach(row => {
    row.addEventListener('click', () => showDetails(parseInt(row.dataset.id, 10)));
  });
}

function showDetails(itemId) {
  const item = historyData.find(i => i.id === itemId);
  if (!item) return;

  selectedItemId = itemId;
  renderHistory();

  const panel = document.getElementById('details-panel');
  document.getElementById('details-title').textContent = item.release_name;
  document.getElementById('details-tl-id').textContent = item.tl_id ? '#' + item.tl_id : '--';
  document.getElementById('details-category').textContent = getCategoryLabel(item.media_type, item.category);
  document.getElementById('details-tags').textContent = item.tags || '--';
  document.getElementById('details-timestamp').textContent = formatDateTime(item.updated_at || item.created_at);
  document.getElementById('details-path').textContent = item.path || '--';

  const filesContainer = document.getElementById('details-files');
  const baseName = item.release_name || 'release';
  const files = [
    { name: baseName + '.torrent', status: item.status === 'success' ? 'ok' : 'missing' },
    { name: baseName + '.nfo', status: item.status === 'success' ? 'ok' : 'missing' },
    { name: baseName + '.xml', status: item.status === 'success' ? 'ok' : 'missing' }
  ];

  filesContainer.innerHTML = files.map(f => `
    <div class="file-item">
      <span class="file-status ${f.status}">${f.status.toUpperCase()}</span>
      <span>${escapeHtml(f.name)}</span>
    </div>
  `).join('');

  panel.classList.add('visible');
}

function hideDetails() {
  selectedItemId = null;
  document.getElementById('details-panel').classList.remove('visible');
  renderHistory();
}

function renderActivity() {
  const logContainer = document.getElementById('activity-log');
  const emptyState = document.getElementById('empty-activity');

  const activities = [];
  historyData.forEach(item => {
    activities.push({
      time: item.updated_at || item.created_at,
      action: item.status,
      message: item.release_name + (item.message ? ': ' + item.message : '')
    });
  });

  activities.sort((a, b) => new Date(b.time) - new Date(a.time));

  const dateFilter = document.getElementById('filter-date').value;
  const filtered = dateFilter === 'all' ? activities : activities.filter(a => {
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - parseInt(dateFilter, 10));
    return new Date(a.time) >= cutoff;
  });

  if (filtered.length === 0) {
    logContainer.innerHTML = '';
    emptyState.style.display = 'block';
    return;
  }

  emptyState.style.display = 'none';
  logContainer.innerHTML = filtered.map(a => `
    <div class="activity-item">
      <span class="activity-time">${formatDateTime(a.time)}</span>
      <span class="activity-action ${a.action}">${a.action}</span>
      <span class="activity-message">${escapeHtml(a.message)}</span>
    </div>
  `).join('');
}

function switchTab(tab) {
  currentTab = tab;

  document.querySelectorAll('.tab').forEach(btn => {
    btn.classList.toggle('is-active', btn.dataset.tab === tab);
  });

  document.getElementById('uploads-content').style.display = tab === 'uploads' ? 'block' : 'none';
  document.getElementById('activity-content').style.display = tab === 'activity' ? 'block' : 'none';

  hideDetails();

  if (tab === 'uploads') {
    renderHistory();
  } else {
    renderActivity();
  }
}

// Event listeners
document.querySelectorAll('.tab').forEach(btn => {
  btn.addEventListener('click', () => switchTab(btn.dataset.tab));
});

document.getElementById('filter-status').addEventListener('change', () => {
  if (currentTab === 'uploads') renderHistory();
});

document.getElementById('filter-date').addEventListener('change', () => {
  if (currentTab === 'uploads') {
    renderHistory();
  } else {
    renderActivity();
  }
});

document.getElementById('filter-type').addEventListener('change', () => {
  if (currentTab === 'uploads') renderHistory();
});

document.getElementById('refresh').addEventListener('click', loadHistory);

document.addEventListener('click', (e) => {
  const panel = document.getElementById('details-panel');
  const table = document.querySelector('.table');
  if (panel.classList.contains('visible') &&
      !panel.contains(e.target) &&
      !table.contains(e.target)) {
    hideDetails();
  }
});

// Initial load
loadHistory();

// Theme toggle
document.getElementById('theme-toggle').onclick = () => {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
};
